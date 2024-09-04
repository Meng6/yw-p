import configparser

def load_properties(file_path='yw.properties'):

    """ The yw.properties file: (consistent with the --config argument)
    [extract]
    comment            Single-line comment delimiter in source files
    factsfile          File for storing prolog facts about scripts
    language           Language used in source files
    listfile           File for storing list of extracted comments
    skeletonfile       File for storing YW-markup skeleton of source files
    sources            List of source files to analyze

    [model]
    factsfile            File for storing prolog facts describing model
    workflow             Name of top-level workflow in model

    [graph]
    datalabel            Info to display in data nodes: NAME, URI, or BOTH
    dotcomments          Include comments in dot file (ON or OFF)
    dotfile              Name of GraphViz DOT file to write graph to
    edgelabels           SHOW or HIDE labels on edges in process and data views
    layout               Direction of graph layout: TB, LR, RL, or BT
    params               SHOW, HIDE, or REDUCE visibility of parameters
    portlayout           Layout mode for workflow ports: HIDE, RELAX or GROUP
    subworkflow          Qualified name of (sub)workflow to render
    title                Graph title (defaults to workflow name)
    titleposition        Where to place graph title: TOP, BOTTOM, or HIDE
    view                 Workflow view to render: PROCESS, DATA or COMBINED
    workflowbox          SHOW or HIDE box around nodes internal to workflow
    """

    # Load the properties file
    config = configparser.ConfigParser()
    config.read(file_path)
    properties = {}

    # Create global variables for the extract section
    for extract_property in ['comment', 'factsfile', 'language', 'listfile', 'skeletonfile', 'sources']:
        properties['extract.{}'.format(extract_property)] = None
        if 'extract' in config:
            properties['extract.{}'.format(extract_property)] = config['extract'].get(extract_property, None)
    
    # Create global variables for the model section
    for model_property in ['factsfile', 'workflow']:
        properties['model.{}'.format(model_property)] = None
        if 'model' in config:
            properties['model.{}'.format(model_property)] = config['model'].get(model_property, None)

    # Create global variables for the graph section
    for graph_property in ['datalabel', 'dotcomments', 'dotfile', 'edgelabels', 'layout', 'params', 'portlayout', 'subworkflow', 'title', 'titleposition', 'view', 'workflowbox']:
        properties['graph.{}'.format(graph_property)] = None
        if 'graph' in config:
            properties['graph.{}'.format(graph_property)] = config['graph'].get(graph_property, None)
    
    return  properties
