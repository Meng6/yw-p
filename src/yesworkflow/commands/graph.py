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
    workflow = properties['model.workflow'] if ('model.workflow' in properties and properties['model.workflow']) else "DEFAULT_WORKFLOW"
    layout = properties['graph.layout'] if ('graph.layout' in properties and properties['graph.layout']) else "TB"
    # Create model
    create_model('\n'.join(annotations), workflow)
    # Visualize the workflow
    geist.report(inputfile='./src/yesworkflow/parse/graph.geist', isinputpath=True, suppressoutput=False, args={'layout': layout})
    return
