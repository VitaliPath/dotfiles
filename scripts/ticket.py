#!/usr/bin/env python3
import json
import sys
import re # <-- Add this
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()

# --- ADD THIS FUNCTION ---
def clean_math(text):
    """Converts basic LaTeX math to readable terminal Unicode."""
    if not text: return ""
    
    # Replace symbols
    text = text.replace(r"\sum", "Σ").replace(r"\cdot", "·").replace(r"\max", "max")
    
    # Remove LaTeX formatting noise
    text = re.sub(r"[\${}]", "", text) # Removes $, {, and }
    
    # Clean up leftover backslashes
    text = text.replace("\\", "")
    return text
# -------------------------

def find_ticket(ticket_id, base_dir="."):
    """Search for the ticket in the standard Forge directory structure."""
    dirs = ["tickets/in_progress", "tickets/open", "tickets/closed"]
    for d in dirs:
        path = Path(base_dir) / d / f"{ticket_id}.json"
        if path.exists():
            return path
    return None

def view_ticket(ticket_id):
    path = find_ticket(ticket_id)
    if not path:
        console.print(f"[red]Error: Ticket {ticket_id} not found in the current directory tree.[/red]")
        return

    with open(path, "r") as f:
        data = json.load(f)

    # 1. Header Table
    table = Table(show_header=False, expand=True, box=None)
    table.add_column("Key", style="cyan", width=15)
    table.add_column("Value", style="white", justify="left")
    table.add_row("🎫 Ticket ID", f"[bold green]{data['id']}[/bold green] ({data['state']})")
    table.add_row("📂 Subsystem", f"{data['Subsystem']} -> {data['Component']}")
    table.add_row("⏱️ Estimation", data['fields']['estimation'])

    console.print(Panel(table, title=f"[bold]{data['title']}[/bold]", border_style="blue"))

    # 2. Render the Deep Dive
    console.print("\n[bold cyan]📖 Overview / Deep Dive[/bold cyan]")
    # Wrap data['overview']
    console.print(Markdown(clean_math(data['overview'])))

    # 3. Render Mathematical Context
    console.print("\n[bold magenta]📐 Mathematical Context[/bold magenta]")
    # Wrap data['mathematical_context']
    console.print(Markdown(clean_math(data['mathematical_context'])))

    # 4. Acceptance Criteria
    console.print("\n[bold yellow]✅ Acceptance Criteria[/bold yellow]")
    for item in data['acceptance_criteria']:
        console.print(f"  [green]•[/green] {item}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[yellow]Usage: ticket <TICKET-ID>[/yellow]")
    else:
        view_ticket(sys.argv[1])