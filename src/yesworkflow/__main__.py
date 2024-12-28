#!/usr/bin/env python3

from yesworkflow.commands.cli import cli
from yesworkflow.commands.extract import extract
from yesworkflow.commands.model import model
from yesworkflow.commands.graph import graph

# Add commands
cli.add_command(extract)
cli.add_command(model)
cli.add_command(graph)

if __name__ == '__main__':
    cli()
