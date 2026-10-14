from rich.align import Align
from rich.panel import Panel
from rich.text import Text


def render_header(console, subtitle):
    title = Text("Tuscan", style="bold cyan")
    title.append(" — ", style="dim")
    title.append(subtitle, style="bold")

    console.print(
        Panel(
            Align.center(title),
            border_style="cyan",
            padding=(1, 2),
        )
    )
    console.print()