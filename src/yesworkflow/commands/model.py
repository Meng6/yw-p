from yesworkflow.parse.parse import create_model
from yesworkflow.commands.extract import extract_annotations
import click

@click.command(help='Builds workflow model from identified YW comments') # Implicitly performs *extract* command first
@click.argument('sources', nargs=-1)  # Accepts zero or more arguments
@click.pass_context
def model(ctx, sources):
    # Fetch properties
    properties = ctx.obj['properties']
    # Extract annotations
    annotations = extract_annotations(properties, sources)
    # Get name of top-level workflow
    if 'model.workflow' in properties:
        workflow = properties['model.workflow']
    else:
        workflow = None
    # Create model
    create_model('\n'.join(annotations), workflow)
    return
