from antlr4 import *
from YWLexer import YWLexer
from YWParser import YWParser
from YWListener import YWListener

def parse_block(block, triples):
    for blockChild in block.getChildren():
        print("***"*30)
        print(type(blockChild))
        if isinstance(blockChild, YWParser.BeginContext):
            blockName = blockChild.blockName().getText()
            triples.append('<http://yesworkflow.com/block/{blockName}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://yesworkflow.com/block> .'.format(blockName=blockName))
        elif isinstance(blockChild, YWParser.NaContext):
            na = blockChild.getText()
        elif isinstance(blockChild, YWParser.BlockAttributeContext):
            blockDesc = blockChild.description().getText()
            triples.append('<http://yesworkflow.com/block/{blockName}> <http://www.w3.org/2000/01/rdf-schema#comment> "{blockDesc}" .'.format(blockName=blockName, blockDesc=blockDesc))
        elif isinstance(blockChild, YWParser.IoContext):
            port = blockChild.port()
            if port.portKeyword().inputKeyword(): # INPUT PORT
                portName = port.portName()[0].getText()
                triples.append('<http://yesworkflow.com/block/{blockName}> <http://yesworkflow.com/hasInput> <http://yesworkflow.com/port/{portName}> .'.format(blockName=blockName, portName=portName))
            else: # OUTPUT PORT
                portName = port.portName()[0].getText()
                triples.append('<http://yesworkflow.com/block/{blockName}> <http://yesworkflow.com/hasOutput> <http://yesworkflow.com/port/{portName}> .'.format(blockName=blockName, portName=portName))
            triples.append('<http://yesworkflow.com/port/{portName}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://yesworkflow.com/port> .'.format(portName=portName))
            triples.append('<http://yesworkflow.com/port/{portName}> <http://www.w3.org/2000/01/rdf-schema#label> "{portName}" .'.format(portName=portName))
            for portAttribute in blockChild.portAttribute():
                if portAttribute.portDesc():
                    portDesc = portAttribute.portDesc().getText()
                    triples.append('<http://yesworkflow.com/port/{portName}> <http://www.w3.org/2000/01/rdf-schema#comment> "{portDesc}" .'.format(portName=portName, portDesc=portDesc))
                if portAttribute.alias():
                    alias = portAttribute.alias().getText()
                    triples.append('<http://yesworkflow.com/port/{portName}> <http://yesworkflow.com/hasAlias> "{alias}" .'.format(portName=portName, alias=alias))
                if portAttribute.resource():
                    if portAttribute.resource().uri():
                        uri = portAttribute.resource().uri().uriTemplate().getText()
                        triples.append('<http://yesworkflow.com/port/{portName}> <http://yesworkflow.com/hasResource/uri> "{uri}" .'.format(portName=portName, uri=uri))
                    elif portAttribute.resource().file():
                        file = portAttribute.resource().file().pathTemplate().getText()
                        triples.append('<http://yesworkflow.com/port/{portName}> <http://yesworkflow.com/hasResource/file> "{file}" .'.format(portName=portName, file=file))
        elif isinstance(blockChild, YWParser.NestedBlocksContext):
            for block in blockChild.block():
                triples.append('<http://yesworkflow.com/block/{blockName}> <http://yesworkflow.com/hasNestedBlock> <http://yesworkflow.com/block/{nestedBlockName}> .'.format(blockName=blockName, nestedBlockName=block.begin().blockName().getText()))
                parse_block(block, triples)
    return triples

class YW2Model(YWListener):
    def __init__(self):
        self.triples = []

    def enterScript(self, ctx:YWParser.ScriptContext):
        for block in ctx.block():
            self.triples = parse_block(block, self.triples)
        return self.triples


# for x in inspect.getmembers(child):
#     print(x)

def main():
    script = """

import netCDF4
import numpy as np
from netCDF4 import ma
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# @BEGIN main
# @PARAM db_pth
# @PARAM fmodel
# @IN input_mask_file  @URI file:{db_pth}/land_water_mask/LandWaterMask_Global_CRUNCEP.nc
# @IN input_data_file  @URI file:{db_pth}/NEE_first_year.nc
# @OUT result_NEE_pdf  @URI file:result_NEE.pdf

def main(db_pth = '.', fmodel = 'clm'):

    # @BEGIN fetch_mask
    # @PARAM db_pth
    # @IN g  @AS input_mask_file  @URI file:{db_pth}/land_water_mask/LandWaterMask_Global_CRUNCEP.nc
    # @OUT mask  @AS land_water_mask
    g = netCDF4.Dataset(db_pth+'/land_water_mask/LandWaterMask_Global_CRUNCEP.nc', 'r')
    mask = g.variables['land_water_mask']
    mask = mask[:].swapaxes(0,1)
    # @END fetch_mask
    
    
    # @BEGIN load_data
    # @PARAM db_pth
    # @IN input_data_file  @URI file:{db_pth}/NEE_first_year.nc
    # @OUT data  @AS NEE_data
    f = netCDF4.Dataset(db_pth+'/NEE_first_year.nc', 'r')
    data = f.variables['NEE']
    data = data[:]
    data = data.swapaxes(0,2)
    adj = 60*60*24*(365/12)*1000
    data = data*adj
    # @END load_data


    # @BEGIN standardize_with_mask
    # @IN data @AS NEE_data
    # @IN mask @AS land_water_mask
    # @OUT data @AS standardized_NEE_data
    native = data.mean(2)
    latShape = mask.shape[0]
    logShape = mask.shape[1]
    for x in range(latShape):
        for y in range(logShape):
            if mask[x,y] == 1 and ma.getmask(native[x,y]) == 1:
                for index in range(data.shape[2]):
                    data[x,y,index] = 0
    # @END standardize_with_mask
    

    # @BEGIN simple_diagnose
    # @PARAM fmodel
    # @IN data @AS standardized_NEE_data
    # @OUT pp  @AS result_NEE_pdf  @URI file:result_NEE.pdf
    plt.imshow(np.mean(data,2))
    plt.xlabel("Mean 1982-2010 NEE [gC/m2/mon]")
    plt.title(fmodel + ":BG1")
    pp = PdfPages('result_NEE.pdf')
    pp.savefig()
    pp.close()    
    # @END simple_diagnose

# @END main
"""
    
    # Create an input stream from the script
    input_stream = InputStream(script)
    
    # Instantiate the lexer and parser
    lexer = YWLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = YWParser(token_stream)
    
    # Parse the script
    tree = parser.script()

    walker = ParseTreeWalker()
    model = YW2Model()
    walker.walk(model, tree)

if __name__ == '__main__':
    main()
