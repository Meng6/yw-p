import antlr4, geist
from yesworkflow.parse.YWLexer import YWLexer
from yesworkflow.parse.YWParser import YWParser
from yesworkflow.parse.YWListener import YWListener

def process_text(text):
    text = text.replace("\\n", "\\\\n")
    return text

def parse_block(block, triples, blockId, portId, maxBlockId, absBlockPath, flag):
    for blockChild in block.getChildren():
        if isinstance(blockChild, YWParser.BeginContext):
            currBlockName = blockChild.blockName().getText()
            absBlockPath = '{}.{}'.format(absBlockPath, currBlockName) if absBlockPath else currBlockName
            triples.append('<https://www.openskope.org/yesworkflow/block/{blockId}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://www.openskope.org/yesworkflow/Block> .'.format(blockId=blockId))
            triples.append('<https://www.openskope.org/yesworkflow/block/{blockId}> <https://www.openskope.org/yesworkflow/hasName> "{blockName}" .'.format(blockId=blockId, blockName=currBlockName))
        elif isinstance(blockChild, YWParser.BlockAttributeContext):
            triples.append('<https://www.openskope.org/yesworkflow/block/{blockId}> <http://www.w3.org/2000/01/rdf-schema#comment> "{blockDesc}" .'.format(blockId=blockId, blockDesc=process_text(blockChild.blockDesc().description().getText())))
        elif isinstance(blockChild, YWParser.IoContext):
            port = blockChild.port()
            portName = port.portName()[0].getText()
            triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <https://www.openskope.org/yesworkflow/hasName> "{portName}" .'.format(portId=portId, portName=portName))
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
                    portDesc = process_text(portAttribute.portDesc().getText())
                    triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <http://www.w3.org/2000/01/rdf-schema#comment> "{portDesc}" .'.format(portId=portId, portDesc=portDesc))
                if portAttribute.alias():
                    portName = portAttribute.alias().dataName().getText()
                    triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <https://www.openskope.org/yesworkflow/hasAlias> "{alias}" .'.format(portId=portId, alias=portName))
                if portAttribute.resource():
                    if portAttribute.resource().uri():
                        triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <https://www.openskope.org/yesworkflow/hasResourceUri> "{uri}" .'.format(portId=portId, uri=portAttribute.resource().uri().uriTemplate().getText()))
                    elif portAttribute.resource().file():
                        triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <https://www.openskope.org/yesworkflow/hasResourceFile> "{file}" .'.format(portId=portId, file=portAttribute.resource().file().pathTemplate().getText()))
            triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <https://www.openskope.org/yesworkflow/hasDataName> "{dataName}" .'.format(portId=portId, dataName=portName))
            triples.append('<https://www.openskope.org/yesworkflow/port/{portId}> <https://www.openskope.org/yesworkflow/hasQualifiedName> "{path}.{portName}" .'.format(portId=portId, path=".".join(absBlockPath.split(".")[:-1]), portName=portName))
            portId = portId + 1
        elif isinstance(blockChild, YWParser.NestedBlocksContext):
            currBlockId = blockId
            currAbsBlockPath = absBlockPath
            for block in blockChild.block():
                blockId = maxBlockId + 1
                maxBlockId = blockId
                triples.append('<https://www.openskope.org/yesworkflow/block/{blockId}> <https://www.openskope.org/yesworkflow/hasNestedBlock> <https://www.openskope.org/yesworkflow/block/{nestedBlockId}> .'.format(blockId=currBlockId, nestedBlockId=blockId))
                (triples, blockId, portId, maxBlockId, absBlockPath) = parse_block(block, triples, blockId, portId, maxBlockId, currAbsBlockPath, False)
            blockId = currBlockId
    
    if flag: # If the block is not a nested block
        blockId = maxBlockId + 1
        maxBlockId = blockId
    return (triples, blockId, portId, maxBlockId, absBlockPath)

class YW2Model(YWListener):
    def __init__(self):
        self.triples = []
        self.blockId = 1 # Block ID starts from 1
        self.portId = 1 # Port ID starts from 1
        self.maxBlockId = 1 # Max Block ID starts from 1
        self.absBlockPath = None # Absolute block name starts from None. This field is used to get qualified names of ports

    def enterScript(self, ctx:YWParser.ScriptContext):
        for block in ctx.block():
            (self.triples, self.blockId, self.portId, self.maxBlockId, self.absBlockPath) = parse_block(block, self.triples, self.blockId, self.portId, self.maxBlockId, None, True)
        return self.triples

def create_model(script, workflow):
    
    # Create an input stream from the script
    input_stream = antlr4.InputStream(script)
    
    # Instantiate the lexer and parser
    lexer = YWLexer(input_stream)
    token_stream = antlr4.CommonTokenStream(lexer)
    parser = YWParser(token_stream)
    
    # Parse the script
    tree = parser.script()

    walker = antlr4.ParseTreeWalker()
    model = YW2Model()
    walker.walk(model, tree)

    # Find top-level workflow
    workflow = workflow if workflow else "DEFAULT_WORKFLOW"
    model_triples = "\n".join(model.triples)
    # Create a yw dataset: (1) add Data and Channel entities, and their relationships; (2)specify the workflow
    geist.report(inputfile="./src/yesworkflow/parse/expand_triples.geist", isinputpath=True, args={"workflow": workflow, "model_triples": model_triples})

    return
