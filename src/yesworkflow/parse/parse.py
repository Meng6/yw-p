from antlr4 import *
from yesworkflow.parse.YWLexer import YWLexer
from yesworkflow.parse.YWParser import YWParser
from yesworkflow.parse.YWListener import YWListener
from geist.commands.report import report
import io, subprocess

def parse_block(block, triples, blockId, portId, maxBlockId, flag):
    for blockChild in block.getChildren():
        if isinstance(blockChild, YWParser.BeginContext):
            triples.append('<https://www.openskope.org/yesworkflow/block/{blockId}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://www.openskope.org/yesworkflow/Block> .'.format(blockId=blockId))
            triples.append('<https://www.openskope.org/yesworkflow/block/{blockId}> <https://www.openskope.org/yesworkflow/hasName> "{blockName}" .'.format(blockId=blockId, blockName=blockChild.blockName().getText()))
        elif isinstance(blockChild, YWParser.BlockAttributeContext):
            triples.append('<https://www.openskope.org/yesworkflow/block/{blockId}> <http://www.w3.org/2000/01/rdf-schema#comment> "{blockDesc}" .'.format(blockId=blockId, blockDesc=blockChild.blockDesc().description().getText()))
        elif isinstance(blockChild, YWParser.IoContext):
            port = blockChild.port()
            triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <https://www.openskope.org/yesworkflow/hasName> "{portName}" .'.format(portId=portId, portName=port.portName()[0].getText()))
            if port.portKeyword().inputKeyword(): # INPUT PORT
                triples.append('<https://www.openskope.org/yesworkflow/block/{blockId}> <https://www.openskope.org/yesworkflow/hasInput> <https://www.openskope.org/yesworkflow/port/{portId}> .'.format(blockId=blockId, portId=portId))
                if port.portKeyword().inputKeyword().InKeyword(): # IN
                    triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://www.openskope.org/yesworkflow/PortIn> .'.format(portId=portId))
                else: # PARAM
                    triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://www.openskope.org/yesworkflow/PortParam> .'.format(portId=portId))
            else: # OUTPUT PORT
                triples.append('<https://www.openskope.org/yesworkflow/block/{blockId}> <https://www.openskope.org/yesworkflow/hasOutput> <https://www.openskope.org/yesworkflow/port/{portId}> .'.format(blockId=blockId, portId=portId))
                triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://www.openskope.org/yesworkflow/PortOut> .'.format(portId=portId))
            for portAttribute in blockChild.portAttribute():
                if portAttribute.portDesc():
                    portDesc = portAttribute.portDesc().getText()
                    triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <http://www.w3.org/2000/01/rdf-schema#comment> "{portDesc}" .'.format(portId=portId, portDesc=portDesc))
                if portAttribute.alias():
                    triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <https://www.openskope.org/yesworkflow/hasAlias> "{alias}" .'.format(portId=portId, alias=portAttribute.alias().dataName().getText()))
                if portAttribute.resource():
                    if portAttribute.resource().uri():
                        triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <https://www.openskope.org/yesworkflow/hasResourceUri> "{uri}" .'.format(portId=portId, uri=portAttribute.resource().uri().uriTemplate().getText()))
                    elif portAttribute.resource().file():
                        triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <https://www.openskope.org/yesworkflow/hasResourceFile> "{file}" .'.format(portId=portId, file=portAttribute.resource().file().pathTemplate().getText()))
            portId = portId + 1
        elif isinstance(blockChild, YWParser.NestedBlocksContext):
            currBlockId = blockId
            for block in blockChild.block():
                blockId = maxBlockId + 1
                maxBlockId = blockId
                triples.append('<https://www.openskope.org/yesworkflow/block/{blockId}> <https://www.openskope.org/yesworkflow/hasNestedBlock> <https://www.openskope.org/yesworkflow/block/{nestedBlockId}> .'.format(blockId=currBlockId, nestedBlockId=blockId))
                (triples, blockId, portId, maxBlockId) = parse_block(block, triples, blockId, portId, maxBlockId, False)
            blockId = currBlockId
    
    if flag: # If the block is not a nested block
        blockId = maxBlockId + 1
        maxBlockId = blockId
    return (triples, blockId, portId, maxBlockId)

class YW2Model(YWListener):
    def __init__(self):
        self.triples = []
        self.blockid = 1 # Block ID starts from 1
        self.portid = 1 # Port ID starts from 1
        self.maxBlockId = 1 # Max Block ID starts from 1

    def enterScript(self, ctx:YWParser.ScriptContext):
        for block in ctx.block():
            (self.triples, self.blockid, self.portid, self.maxBlockId) = parse_block(block, self.triples, self.blockid, self.portid, self.maxBlockId, True)
        return self.triples

def create_model(script, workflow):
    
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
    
    # Find top-level workflow
    workflow = workflow if workflow else "DEFAULT_WORKFLOW"
    model_triples = "\n".join(model.triples)
    # Expand triples
    with open('./src/yesworkflow/parse/model.geist', 'r') as model_file:
        model_template = model_file.read().replace("{{ workflow }}", workflow).replace("{{ model_triples }}", model_triples)
    report.callback(file=io.StringIO(model_template), outputroot="./", suppressoutput=True)
    # Visualize the workflow
    subprocess.run(["geist", "report", "--file", "./src/yesworkflow/parse/graph.geist", "--outputroot", "./", "--suppressoutput", "False"])

    return
