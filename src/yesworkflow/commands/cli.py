from yesworkflow.config.load_properties import load_properties
from yesworkflow.config.add_config_argument import get_configuration_options, parse_config_argument
import click

@click.group()
@click.option('-c', '--config', multiple=True, help='\n\b\n'+'Assign value to configuration option in the format of name=value.\n{}'.format(get_configuration_options()))
@click.pass_context
def cli(ctx, config):
    # global outputroot
    # outputroot = './'
    
    ctx.ensure_object(dict)
    # Load properties
    properties = load_properties()
    properties = parse_config_argument(properties, config)
    ctx.obj['properties'] = properties
    
    pass
