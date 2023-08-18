from rich.emoji import EMOJI
from rich.console import Console


def eap_warning(console: Console):
    cc = EMOJI.get('construction') + ' '
    console.print(f"{cc} [yellow]This is the Early Access Program version of CLI[/yellow]")
