from yesworkflow.parse.parse import create_model
from yesworkflow.commands.extract import extract_annotations
import click, geist


@click.command(help='Graphically renders workflow model of script') # Implicitly performs *extract* and *model* commands first.
@click.argument('sources', nargs=-1)  # Accepts zero or more arguments
@click.pass_context
def graph(ctx, sources):
    # Fetch properties
    properties = ctx.obj['properties']
    # Extract annotations
    annotations = extract_annotations(properties, sources)
    # Get name of top-level workflow
    workflow = "DEFAULT_WORKFLOW" if 'model.workflow' not in properties else properties['model.workflow']
    layout = "TB" if 'graph.layout' not in properties else properties['graph.layout']
    # Create model
    create_model('\n'.join(annotations), workflow)
    # Visualize the workflow
    geist.report(inputfile='./src/yesworkflow/parse/graph.geist', isinputpath=True, suppressoutput=False, args={'layout': layout})
    return
