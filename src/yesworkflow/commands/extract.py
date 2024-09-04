from yesworkflow.language.infer_language import load_language_config, infer_language
import click, os, io

# Definitions of the standard keyword for the each tag.
STANDARD_AS_KEYWORD     = "@as"
STANDARD_BEGIN_KEYWORD  = "@begin"
STANDARD_CALL_KEYWORD   = "@call"
STANDARD_DESC_KEYWORD   = "@desc"
STANDARD_END_KEYWORD    = "@end"
STANDARD_FILE_KEYWORD   = "@file"
STANDARD_IN_KEYWORD     = "@in"
STANDARD_LOG_KEYWORD    = "@log"
STANDARD_OUT_KEYWORD    = "@out"
STANDARD_PARAM_KEYWORD  = "@param"
STANDARD_RETURN_KEYWORD = "@return"
STANDARD_URI_KEYWORD    = "@uri"

KEYWORDS = [
    STANDARD_AS_KEYWORD,
    STANDARD_BEGIN_KEYWORD,
    STANDARD_CALL_KEYWORD,
    STANDARD_DESC_KEYWORD,
    STANDARD_END_KEYWORD, 
    STANDARD_FILE_KEYWORD,
    STANDARD_IN_KEYWORD,
    STANDARD_LOG_KEYWORD,
    STANDARD_OUT_KEYWORD,
    STANDARD_PARAM_KEYWORD,
    STANDARD_RETURN_KEYWORD,
    STANDARD_URI_KEYWORD
]

def get_delimiters(config_language, language):
    singleDelimiter, delimiterPair = None, None
    if language in config_language:
        singleDelimiter = config_language[language].get('singleDelimiter', None)
        delimiterPair = config_language[language].get('delimiterPair', None)
    return singleDelimiter, delimiterPair

def match_comments(source, singleDelimiter, delimiterPair, isString=False):
    comments = []
    if isString:
        f = io.StringIO(source)
    else:
        f = open(source, 'r')
    
    with f:
        lines = f.readlines()
        comment, right, line2check = '', False, False
        for line in lines:
            # Check block comments
            if right:
                idxr = line.find(right)
                if idxr != -1:
                    comments.append('{} {}'.format(comment, line[:idxr].strip()))
                    comment, right = '', False
                else:
                    comment = '{} {}'.format(comment, line.strip())
            else:
                if delimiterPair:
                    for dp in delimiterPair:
                        left, right = dp[0], dp[1]
                        lenl = len(left)
                        idxl = line.find(left)
                        if idxl != -1:
                            idxr = line.find(right)
                            if idxr != -1:
                                comments.append(line[idxl+lenl:idxr].strip())
                                right = False
                            else:
                                comment = line[idxl+lenl:].strip()
                            break
                        else:
                            right = False
                            line2check = True
                else:
                    line2check = True
            if line2check and singleDelimiter:
                # Check single-line comments
                idxs = line.find(singleDelimiter)
                if idxs != -1:
                    comments.append(line[idxs+len(singleDelimiter):].strip())
                line2check = False
    return comments


def match_keywords(comments, keywords):
    annotations = []
    for comment in comments:
        idx = -1
        for keyword in keywords:
            idxk = comment.lower().find(keyword)
            if idxk != -1:
                idx = min(idx, idxk) if idx != -1 else idxk
        if idx != -1:
            annotations.append(comment[idx:])
    return annotations

@click.command(help='Identify YW comments in script source file(s)')
@click.argument('sources', nargs=-1)  # Accepts zero or more arguments
@click.pass_context
def extract(ctx, sources):

    # Fetch properties
    properties = ctx.obj['properties']

    # Language config
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_language_path = os.path.join(script_dir, '../language/language.yaml')
    config_language = load_language_config(config_language_path)

    annotations = []
    if len(sources) == 0:
        source = properties['extract.sources']
        if source:
            sources = [source]
        else:
            click.echo("No script source file paths provided. Please provide at least one file path.")

    for source in sources:
        singleDelimiter = properties['extract.comment']
        if singleDelimiter:
            comments = match_comments(source, singleDelimiter, None)
        else:
            language = properties['extract.language']
            if not language:
                language = infer_language(source, config_language)
            singleDelimiter, delimiterPair = get_delimiters(config_language, language)
            comments = match_comments(source, singleDelimiter, delimiterPair)
        annotations.extend(match_keywords(comments, KEYWORDS))
    
    listfile = properties['extract.listfile']
    if listfile:
        if isinstance(listfile, bool):
            for annotation in annotations:
                click.echo(annotation)
        else:
            with open(properties['extract.listfile'], 'w') as f:
                for annotation in annotations:
                    f.write('{}\n'.format(annotation))
                    click.echo(annotation)
