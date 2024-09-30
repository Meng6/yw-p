# Generated from YW.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .YWParser import YWParser
else:
    from YWParser import YWParser

# This class defines a complete listener for a parse tree produced by YWParser.
class YWListener(ParseTreeListener):

    # Enter a parse tree produced by YWParser#script.
    def enterScript(self, ctx:YWParser.ScriptContext):
        pass

    # Exit a parse tree produced by YWParser#script.
    def exitScript(self, ctx:YWParser.ScriptContext):
        pass


    # Enter a parse tree produced by YWParser#block.
    def enterBlock(self, ctx:YWParser.BlockContext):
        pass

    # Exit a parse tree produced by YWParser#block.
    def exitBlock(self, ctx:YWParser.BlockContext):
        pass


    # Enter a parse tree produced by YWParser#nestedBlocks.
    def enterNestedBlocks(self, ctx:YWParser.NestedBlocksContext):
        pass

    # Exit a parse tree produced by YWParser#nestedBlocks.
    def exitNestedBlocks(self, ctx:YWParser.NestedBlocksContext):
        pass


    # Enter a parse tree produced by YWParser#blockAttribute.
    def enterBlockAttribute(self, ctx:YWParser.BlockAttributeContext):
        pass

    # Exit a parse tree produced by YWParser#blockAttribute.
    def exitBlockAttribute(self, ctx:YWParser.BlockAttributeContext):
        pass


    # Enter a parse tree produced by YWParser#io.
    def enterIo(self, ctx:YWParser.IoContext):
        pass

    # Exit a parse tree produced by YWParser#io.
    def exitIo(self, ctx:YWParser.IoContext):
        pass


    # Enter a parse tree produced by YWParser#port.
    def enterPort(self, ctx:YWParser.PortContext):
        pass

    # Exit a parse tree produced by YWParser#port.
    def exitPort(self, ctx:YWParser.PortContext):
        pass


    # Enter a parse tree produced by YWParser#portAttribute.
    def enterPortAttribute(self, ctx:YWParser.PortAttributeContext):
        pass

    # Exit a parse tree produced by YWParser#portAttribute.
    def exitPortAttribute(self, ctx:YWParser.PortAttributeContext):
        pass


    # Enter a parse tree produced by YWParser#alias.
    def enterAlias(self, ctx:YWParser.AliasContext):
        pass

    # Exit a parse tree produced by YWParser#alias.
    def exitAlias(self, ctx:YWParser.AliasContext):
        pass


    # Enter a parse tree produced by YWParser#begin.
    def enterBegin(self, ctx:YWParser.BeginContext):
        pass

    # Exit a parse tree produced by YWParser#begin.
    def exitBegin(self, ctx:YWParser.BeginContext):
        pass


    # Enter a parse tree produced by YWParser#blockDesc.
    def enterBlockDesc(self, ctx:YWParser.BlockDescContext):
        pass

    # Exit a parse tree produced by YWParser#blockDesc.
    def exitBlockDesc(self, ctx:YWParser.BlockDescContext):
        pass


    # Enter a parse tree produced by YWParser#portDesc.
    def enterPortDesc(self, ctx:YWParser.PortDescContext):
        pass

    # Exit a parse tree produced by YWParser#portDesc.
    def exitPortDesc(self, ctx:YWParser.PortDescContext):
        pass


    # Enter a parse tree produced by YWParser#end.
    def enterEnd(self, ctx:YWParser.EndContext):
        pass

    # Exit a parse tree produced by YWParser#end.
    def exitEnd(self, ctx:YWParser.EndContext):
        pass


    # Enter a parse tree produced by YWParser#file.
    def enterFile(self, ctx:YWParser.FileContext):
        pass

    # Exit a parse tree produced by YWParser#file.
    def exitFile(self, ctx:YWParser.FileContext):
        pass


    # Enter a parse tree produced by YWParser#uri.
    def enterUri(self, ctx:YWParser.UriContext):
        pass

    # Exit a parse tree produced by YWParser#uri.
    def exitUri(self, ctx:YWParser.UriContext):
        pass


    # Enter a parse tree produced by YWParser#misplacedEnd.
    def enterMisplacedEnd(self, ctx:YWParser.MisplacedEndContext):
        pass

    # Exit a parse tree produced by YWParser#misplacedEnd.
    def exitMisplacedEnd(self, ctx:YWParser.MisplacedEndContext):
        pass


    # Enter a parse tree produced by YWParser#misplacedBeginChild.
    def enterMisplacedBeginChild(self, ctx:YWParser.MisplacedBeginChildContext):
        pass

    # Exit a parse tree produced by YWParser#misplacedBeginChild.
    def exitMisplacedBeginChild(self, ctx:YWParser.MisplacedBeginChildContext):
        pass


    # Enter a parse tree produced by YWParser#misplacedPortChild.
    def enterMisplacedPortChild(self, ctx:YWParser.MisplacedPortChildContext):
        pass

    # Exit a parse tree produced by YWParser#misplacedPortChild.
    def exitMisplacedPortChild(self, ctx:YWParser.MisplacedPortChildContext):
        pass


    # Enter a parse tree produced by YWParser#misplacedKeyword.
    def enterMisplacedKeyword(self, ctx:YWParser.MisplacedKeywordContext):
        pass

    # Exit a parse tree produced by YWParser#misplacedKeyword.
    def exitMisplacedKeyword(self, ctx:YWParser.MisplacedKeywordContext):
        pass


    # Enter a parse tree produced by YWParser#resource.
    def enterResource(self, ctx:YWParser.ResourceContext):
        pass

    # Exit a parse tree produced by YWParser#resource.
    def exitResource(self, ctx:YWParser.ResourceContext):
        pass


    # Enter a parse tree produced by YWParser#portKeyword.
    def enterPortKeyword(self, ctx:YWParser.PortKeywordContext):
        pass

    # Exit a parse tree produced by YWParser#portKeyword.
    def exitPortKeyword(self, ctx:YWParser.PortKeywordContext):
        pass


    # Enter a parse tree produced by YWParser#inputKeyword.
    def enterInputKeyword(self, ctx:YWParser.InputKeywordContext):
        pass

    # Exit a parse tree produced by YWParser#inputKeyword.
    def exitInputKeyword(self, ctx:YWParser.InputKeywordContext):
        pass


    # Enter a parse tree produced by YWParser#outputKeyword.
    def enterOutputKeyword(self, ctx:YWParser.OutputKeywordContext):
        pass

    # Exit a parse tree produced by YWParser#outputKeyword.
    def exitOutputKeyword(self, ctx:YWParser.OutputKeywordContext):
        pass


    # Enter a parse tree produced by YWParser#blockName.
    def enterBlockName(self, ctx:YWParser.BlockNameContext):
        pass

    # Exit a parse tree produced by YWParser#blockName.
    def exitBlockName(self, ctx:YWParser.BlockNameContext):
        pass


    # Enter a parse tree produced by YWParser#portName.
    def enterPortName(self, ctx:YWParser.PortNameContext):
        pass

    # Exit a parse tree produced by YWParser#portName.
    def exitPortName(self, ctx:YWParser.PortNameContext):
        pass


    # Enter a parse tree produced by YWParser#dataName.
    def enterDataName(self, ctx:YWParser.DataNameContext):
        pass

    # Exit a parse tree produced by YWParser#dataName.
    def exitDataName(self, ctx:YWParser.DataNameContext):
        pass


    # Enter a parse tree produced by YWParser#description.
    def enterDescription(self, ctx:YWParser.DescriptionContext):
        pass

    # Exit a parse tree produced by YWParser#description.
    def exitDescription(self, ctx:YWParser.DescriptionContext):
        pass


    # Enter a parse tree produced by YWParser#pathElement.
    def enterPathElement(self, ctx:YWParser.PathElementContext):
        pass

    # Exit a parse tree produced by YWParser#pathElement.
    def exitPathElement(self, ctx:YWParser.PathElementContext):
        pass


    # Enter a parse tree produced by YWParser#pathVariable.
    def enterPathVariable(self, ctx:YWParser.PathVariableContext):
        pass

    # Exit a parse tree produced by YWParser#pathVariable.
    def exitPathVariable(self, ctx:YWParser.PathVariableContext):
        pass


    # Enter a parse tree produced by YWParser#pathConstant.
    def enterPathConstant(self, ctx:YWParser.PathConstantContext):
        pass

    # Exit a parse tree produced by YWParser#pathConstant.
    def exitPathConstant(self, ctx:YWParser.PathConstantContext):
        pass


    # Enter a parse tree produced by YWParser#variableName.
    def enterVariableName(self, ctx:YWParser.VariableNameContext):
        pass

    # Exit a parse tree produced by YWParser#variableName.
    def exitVariableName(self, ctx:YWParser.VariableNameContext):
        pass


    # Enter a parse tree produced by YWParser#pathTemplate.
    def enterPathTemplate(self, ctx:YWParser.PathTemplateContext):
        pass

    # Exit a parse tree produced by YWParser#pathTemplate.
    def exitPathTemplate(self, ctx:YWParser.PathTemplateContext):
        pass


    # Enter a parse tree produced by YWParser#uriTemplate.
    def enterUriTemplate(self, ctx:YWParser.UriTemplateContext):
        pass

    # Exit a parse tree produced by YWParser#uriTemplate.
    def exitUriTemplate(self, ctx:YWParser.UriTemplateContext):
        pass


    # Enter a parse tree produced by YWParser#scheme.
    def enterScheme(self, ctx:YWParser.SchemeContext):
        pass

    # Exit a parse tree produced by YWParser#scheme.
    def exitScheme(self, ctx:YWParser.SchemeContext):
        pass


    # Enter a parse tree produced by YWParser#phrase.
    def enterPhrase(self, ctx:YWParser.PhraseContext):
        pass

    # Exit a parse tree produced by YWParser#phrase.
    def exitPhrase(self, ctx:YWParser.PhraseContext):
        pass


    # Enter a parse tree produced by YWParser#unquotedPhrase.
    def enterUnquotedPhrase(self, ctx:YWParser.UnquotedPhraseContext):
        pass

    # Exit a parse tree produced by YWParser#unquotedPhrase.
    def exitUnquotedPhrase(self, ctx:YWParser.UnquotedPhraseContext):
        pass


    # Enter a parse tree produced by YWParser#word.
    def enterWord(self, ctx:YWParser.WordContext):
        pass

    # Exit a parse tree produced by YWParser#word.
    def exitWord(self, ctx:YWParser.WordContext):
        pass


    # Enter a parse tree produced by YWParser#unquotedWord.
    def enterUnquotedWord(self, ctx:YWParser.UnquotedWordContext):
        pass

    # Exit a parse tree produced by YWParser#unquotedWord.
    def exitUnquotedWord(self, ctx:YWParser.UnquotedWordContext):
        pass


    # Enter a parse tree produced by YWParser#na.
    def enterNa(self, ctx:YWParser.NaContext):
        pass

    # Exit a parse tree produced by YWParser#na.
    def exitNa(self, ctx:YWParser.NaContext):
        pass



del YWParser