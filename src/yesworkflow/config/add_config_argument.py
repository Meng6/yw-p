import click

def add_a_configuration_option(help_message, name, value):
    return '{}\n{} {}'.format(help_message, click.style(name, fg='bright_white'), value)

def get_configuration_options():
    configuration_options = 'Configuration Options:'
    configuration_options = add_a_configuration_option(configuration_options, 'extract.comment', 'Single-line comment delimiter in source files')
    configuration_options = add_a_configuration_option(configuration_options, 'extract.factsfile', 'File for storing prolog facts about scripts')
    configuration_options = add_a_configuration_option(configuration_options, 'extract.language', 'Language used in source files')
    configuration_options = add_a_configuration_option(configuration_options, 'extract.listfile', 'File for storing flat list of extracted YW markup')
    configuration_options = add_a_configuration_option(configuration_options, 'extract.skeletonfile', 'File for storing YW-markup skeleton of source files')
    configuration_options = add_a_configuration_option(configuration_options, 'extract.sources', 'List of source files to analyze')
    configuration_options = add_a_configuration_option(configuration_options, '', '')
    configuration_options = add_a_configuration_option(configuration_options, 'model.factsfile', 'File for storing prolog facts describing model')
    configuration_options = add_a_configuration_option(configuration_options, 'model.workflow', 'Name of top-level workflow in model')
    configuration_options = add_a_configuration_option(configuration_options, '', '')
    configuration_options = add_a_configuration_option(configuration_options, 'recon.factsfile', 'File for storing reconstructed facts about a run')
    configuration_options = add_a_configuration_option(configuration_options, '', '')
    configuration_options = add_a_configuration_option(configuration_options, 'graph.datalabel', 'Info to display in data nodes: NAME, URI, or BOTH')
    configuration_options = add_a_configuration_option(configuration_options, 'graph.dotcomments', 'Include comments in dot file (ON or OFF)')
    configuration_options = add_a_configuration_option(configuration_options, 'graph.dotfile', 'Name of GraphViz DOT file to write graph to')
    configuration_options = add_a_configuration_option(configuration_options, 'graph.edgelabels', 'SHOW or HIDE labels on edges in process and data views')
    configuration_options = add_a_configuration_option(configuration_options, 'graph.layout', 'Direction of graph layout: TB, LR, RL, or BT')
    configuration_options = add_a_configuration_option(configuration_options, 'graph.params', 'SHOW, HIDE, or REDUCE visibility of parameters')
    configuration_options = add_a_configuration_option(configuration_options, 'graph.portlayout', 'Layout mode for workflow ports: HIDE, RELAX or GROUP')
    configuration_options = add_a_configuration_option(configuration_options, 'graph.programlabel', 'Info to display in program nodes: NAME, DESCRIPTION, or BOTH')
    configuration_options = add_a_configuration_option(configuration_options, 'graph.subworkflow', 'Qualified name of (sub)workflow to render')
    configuration_options = add_a_configuration_option(configuration_options, 'graph.title', 'Graph title (defaults to workflow name)')
    configuration_options = add_a_configuration_option(configuration_options, 'graph.titleposition', 'Where to place graph title: TOP, BOTTOM, or HIDE')
    configuration_options = add_a_configuration_option(configuration_options, 'graph.view', 'Workflow view to render: PROCESS, DATA or COMBINED')
    configuration_options = add_a_configuration_option(configuration_options, 'graph.workflowbox', 'SHOW or HIDE box around nodes internal to workflow')
    return configuration_options

def parse_config_argument(properties, config_argument):
    # Extract the configuration options from the config_argument
    # And update the global variable, properties, accordingly
    for option in config_argument:
        if '=' in option:
            name, value = option.split('=')
        else:
            name, value = option, True
        properties[name] = value
    return properties
