"""UI components for BND-TOOLS dashboard."""
import time
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box

from . import constants as C


def make_title_text(title, phase=0):
    """Erstellt einen farbigen Titel für das Dashboard"""
    if phase > 0:
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(phase, 1.0, 1.0)
        return Text.from_markup(f"[rgb({int(r*255)},{int(g*255)},{int(b*255)}) bold]{title}[/]")
    else:
        return Text.from_markup(f"[cyan bold]{title}[/]")


def make_card_cell(code, label, is_selected=False, phase=0):
    """Erstellt eine Karte für ein Tool"""
    if is_selected:
        style = "black on cyan bold"
    else:
        style = "white"
    
    if phase > 0:
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(phase, 1.0, 1.0)
        border = f"rgb({int(r*255)},{int(g*255)},{int(b*255)})"
    else:
        border = "cyan"
    
    content = f"[{style}]{code}  {label}[/]"
    return Panel(content, border_style=border, box=box.ROUNDED, padding=(0, 1))


def monitor_block(cat_label, n_tools, tools, username, nuker_status, badge, phase=0):
    """Erstellt den Monitor-Block in der Sidebar"""
    from rich.table import Table
    from rich.text import Text
    
    table = Table.grid(padding=(0, 1))
    table.add_column()
    
    nuker_active, nuker_webhook = nuker_status
    nuker_text = "[red]● ACTIVE[/]" if nuker_active else "[dim]○ INACTIVE[/]"
    
    table.add_row(Text.from_markup(f"[dim]User:[/] [cyan]{username}[/]"))
    table.add_row(Text.from_markup(f"[dim]Tools:[/] [white]{len(tools)}[/]"))
    table.add_row(Text.from_markup(f"[dim]Nuker:[/] {nuker_text}"))
    if badge:
        table.add_row(Text.from_markup(f"[dim]News:[/] [gold1]{badge}[/]"))
    
    return Panel(table, title="[bold white]STATUS", border_style="blue", box=box.SQUARE)