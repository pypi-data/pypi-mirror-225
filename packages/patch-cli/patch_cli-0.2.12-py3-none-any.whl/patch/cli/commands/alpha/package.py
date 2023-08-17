import click

from patch.cli.styled import StyledGroup, StyledCommand

@click.group(cls=StyledGroup, help='Create, publish, and evolve data packages')
def package():
    pass

@package.command(cls=StyledCommand, help='Generates a datapackage.json for a source.')
def generate_descriptor():
    pass
