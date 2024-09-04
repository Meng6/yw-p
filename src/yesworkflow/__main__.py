#!/usr/bin/env python3

from yesworkflow.commands.cli import cli
from yesworkflow.commands.extract import extract

# Add commands
cli.add_command(extract)

if __name__ == '__main__':
    cli()
