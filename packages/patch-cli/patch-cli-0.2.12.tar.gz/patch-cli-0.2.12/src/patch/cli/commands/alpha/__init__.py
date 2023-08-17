import click

from patch.cli.styled import StyledGroup
from patch.cli.commands.alpha.package import package

@click.group(cls=StyledGroup, help='Commands at stability level alpha')
def alpha():
    pass

alpha.add_command(package)
