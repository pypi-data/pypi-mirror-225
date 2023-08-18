import collections
from typing import Optional, Mapping

from rich.box import Box
from rich.console import Console

import click
import click_aliases

from patch.cli.eap import eap_warning


def colorize(console, text, style):
    with console.capture() as capture:
        console.print(text, style=style, end='')
    return capture.get()


class PatchFormatter(click.HelpFormatter):

    def __init__(self, *args, **kwargs):
        self.console = Console()
        self.headers_color = 'yellow'
        self.options_color = 'cyan'
        super().__init__(*args, **kwargs)

    def _colorize(self, text, style):
        return colorize(self.console, text, style)

    def write_usage(self, prog, args='', prefix='Usage: '):
        prefix = self._colorize(prefix, self.headers_color)
        super(PatchFormatter, self).write_usage(prog, args, prefix=prefix)

    def write_heading(self, heading):
        colorized_heading = self._colorize(heading, style=self.headers_color)
        super(PatchFormatter, self).write_heading(colorized_heading)

    def write_dl(self, rows, **kwargs):
        colorized_rows = [(self._colorize(row[0], self.options_color), row[1]) for row in rows]
        super(PatchFormatter, self).write_dl(colorized_rows, **kwargs)


class StyledMixin:
    def get_help(self, ctx):
        if ctx.parent is None:
            eap_warning(Console())
        formatter = PatchFormatter(width=ctx.terminal_width, max_width=ctx.max_content_width)
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip('\n')


class StyledGroup(StyledMixin, click_aliases.ClickAliasedGroup):
    def __init__(self, name: Optional[str] = None, commands: Optional[Mapping[str, click.Command]] = None, **kwargs):
        super(StyledGroup, self).__init__(name, commands, **kwargs)
        self.commands = collections.OrderedDict(commands or {})

    def list_commands(self, _ctx: click.Context) -> Mapping[str, click.Command]:
        return self.commands


class StyledCommand(StyledMixin, click.Command):
    pass


NONE_BOX: Box = Box(
    """\
    
    
    
    
    
    
    
    
"""
)
