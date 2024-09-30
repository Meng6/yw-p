from yesworkflow.commands.extract import match_comments, match_keywords, KEYWORDS

def check_match_comments(source, singleDelimiter, delimiterPair, expected_comments):
    comments = match_comments(source, singleDelimiter, delimiterPair, isString=True)
    assert len(comments) == len(expected_comments)
    assert all([c == e for c, e in zip(comments, expected_comments)])
    return comments

def check_match_keywords(comments, keywords, expected_annotations):
    annotations = match_keywords(comments, keywords)
    assert len(annotations) == len(expected_annotations)
    assert all([a == e for a, e in zip(annotations, expected_annotations)])
    return annotations

def test_extract_blankComment():
    source = ''
    singleDelimiter, delimiterPair = '#', None
    expected_comments, expected_annotations = [], []
    comments = check_match_comments(source, singleDelimiter, delimiterPair, expected_comments)
    check_match_keywords(comments, KEYWORDS, expected_annotations)

def test_extract_nonComment():
    source = 'not a comment'
    singleDelimiter, delimiterPair = '#', None
    expected_comments, expected_annotations = [], []
    comments = check_match_comments(source, singleDelimiter, delimiterPair, expected_comments)
    check_match_keywords(comments, KEYWORDS, expected_annotations)

def test_extract_nonYWComment():
    source = '# a comment'
    singleDelimiter, delimiterPair = '#', None
    expected_comments, expected_annotations = ['a comment'], []
    comments = check_match_comments(source, singleDelimiter, delimiterPair, expected_comments)
    check_match_keywords(comments, KEYWORDS, expected_annotations)

def test_extract_nonYWComment_withAtSymbol():
    source = '# a comment with an @ symbol in it'
    singleDelimiter, delimiterPair = '#', None
    expected_comments, expected_annotations = ['a comment with an @ symbol in it'], []
    comments = check_match_comments(source, singleDelimiter, delimiterPair, expected_comments)
    check_match_keywords(comments, KEYWORDS, expected_annotations)

def test_extract_multipleComments_hash():
    lines = [
        '## @begin step   ',
        '  some code ',
        '   # @in x  ',
        '     more code',
        '     more code',
        ' #    @out y',
        '     more code',
        '     more code',
        ' ##    @end step'
    ]
    source = '\n'.join(lines)
    singleDelimiter, delimiterPair = '#', None
    expected_comments = [
        '# @begin step',
        '@in x',
        '@out y',
        '#    @end step'
    ]
    expected_annotations = [
        '@begin step',
        '@in x',
        '@out y',
        '@end step'
    ]
    comments = check_match_comments(source, singleDelimiter, delimiterPair, expected_comments)
    check_match_keywords(comments, KEYWORDS, expected_annotations)

def test_extract_multipleComments_slash():
    lines = [
        '// @begin step   ',
        '  some code ',
        '   // @in x  ',
        '     more code',
        '     more code',
        ' //    @out y',
        '     more code',
        '     more code',
        ' //    @end step'
    ]
    source = '\n'.join(lines)
    singleDelimiter, delimiterPair = '//', None
    expected_comments = [
        '@begin step',
        '@in x',
        '@out y',
        '@end step'
    ]
    expected_annotations = [
        '@begin step',
        '@in x',
        '@out y',
        '@end step'
    ]
    comments = check_match_comments(source, singleDelimiter, delimiterPair, expected_comments)
    check_match_keywords(comments, KEYWORDS, expected_annotations)

def test_extract_multipleComments_withAliasesOnSameLines():
    lines = [
        '## @begin step   ',
        '  some code ',
        '   # @in x @as horiz ',
        '     more code',
        '     more code',
        ' #    @param y @as vert',
        '     more code',
        '     more code',
        '    #  @end step']
    source = '\n'.join(lines)
    singleDelimiter, delimiterPair = '#', None

    expected_comments = [
        '# @begin step',
        '@in x @as horiz',
        '@param y @as vert',
        '@end step'
    ]
    expected_annotations = [
        '@begin step',
        '@in x @as horiz',
        '@param y @as vert',
        '@end step'
    ]
    comments = check_match_comments(source, singleDelimiter, delimiterPair, expected_comments)
    check_match_keywords(comments, KEYWORDS, expected_annotations)

def test_extract_multipleComments_withAliasesOnDifferentLines():
    lines = [
        '## @begin step   ',
        '  some code ',
        '   # @in x',
        '    # @as horiz ',
        '     more code',
        '     more code',
        ' #    @param y ',
        '  #@as vert',
        '     more code',
        '     more code',
        '    #  @end step']
    source = '\n'.join(lines)
    print(source)
    singleDelimiter, delimiterPair = '#', None

    expected_comments = [
        '# @begin step',
        '@in x',
        '@as horiz',
        '@param y',
        '@as vert',
        '@end step'
    ]
    expected_annotations = [
        '@begin step',
        '@in x',
        '@as horiz',
        '@param y',
        '@as vert',
        '@end step'
    ]
    comments = check_match_comments(source, singleDelimiter, delimiterPair, expected_comments)
    check_match_keywords(comments, KEYWORDS, expected_annotations)

def test_extract_multipleCommentsOnOneLine():
    source = '# @begin step @in x @as horiz @param y @as vert @end step'
    singleDelimiter, delimiterPair = '#', None

    expected_comments = ['@begin step @in x @as horiz @param y @as vert @end step']
    expected_annotations = ['@begin step @in x @as horiz @param y @as vert @end step']
    comments = check_match_comments(source, singleDelimiter, delimiterPair, expected_comments)
    check_match_keywords(comments, KEYWORDS, expected_annotations)

def test_extract_blockMultipleComments_withAliasesOnDifferentLines():
    lines = [
        '""" @begin step   ',
        '  some code ',
        '   # @in x',
        '    # @as horiz """some code',
        '     more code',
        '     more code',
        ' #    @param y ',
        '  #@as vert',
        '     more code',
        '     more code',
        '    #  @end step']
    source = '\n'.join(lines)
    singleDelimiter, delimiterPair = '#', [['"""', '"""']]

    expected_comments = [
        '@begin step\nsome code\n# @in x\n# @as horiz',
        '@param y',
        '@as vert',
        '@end step'
    ]
    expected_annotations = [
        '@begin step\nsome code\n# @in x\n# @as horiz',
        '@param y',
        '@as vert',
        '@end step'
    ]
    comments = check_match_comments(source, singleDelimiter, delimiterPair, expected_comments)
    check_match_keywords(comments, KEYWORDS, expected_annotations)
