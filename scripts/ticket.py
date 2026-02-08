#!/usr/bin/env python3
import json
import sys
import re
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()

def clean_math(text):
    """Converts LaTeX math to readable terminal Unicode."""
    if not text: return ""
    
    # Mapping LaTeX to Unicode/Readable text
    replacements = {
        r"\Delta": "Δ",
        r"\theta": "θ",
        r"\text": "",
        r"\times": "×",
        r"\log": "log",
        r"\frac": "",
        r"\sum": "Σ",
        r"\cdot": "·",
        r"\times": "×",
        r"\log": "log",
        r"\frac": "", # We'll just strip the command and keep the {a}{b}
        r"\text": "",
        r"\infty": "∞",
        r"\pm": "±"
    }
    
    for lat, uni in replacements.items():
        text = text.replace(lat, uni)
    
    # Clean up fractions: \frac{N}{df} -> (N/df)
    text = re.sub(r"\{(\w+)\}\{(\w+)\}", r"(\1/\2)", text)
    # Remove remaining curly braces and dollar signs
    text = re.sub(r"[\${}]", "", text)
    # Clean up subscript formatting (optional: use unicode subscripts if desired)
    text = text.replace("_", "") 
    
    return text.replace("\\", "")

def find_ticket(ticket_id):
    """Search for the ticket in the centralized Stoneburner-Knowledge-Base."""
    kb_base = Path("/Users/seanstoneburner/Repos/Stoneburner-Knowledge-Base")
    # Recursively find the JSON file
    for path in kb_base.rglob(f"{ticket_id}.json"):
        return path
    return None

def view_ticket(ticket_id):
    path = find_ticket(ticket_id)
    if not path:
        console.print(f"[red]Error: Ticket {ticket_id} not found.[/red]")
        return

    with open(path, "r") as f:
        data = json.load(f)

    # Header
    table = Table(show_header=False, expand=True, box=None)
    table.add_column("Key", style="cyan", width=15)
    table.add_column("Value", style="white")
    table.add_row("🎫 Ticket ID", f"[bold green]{data['id']}[/bold green] ({data['state']})")
    table.add_row("📂 Subsystem", f"{data['Subsystem']} -> {data['Component']}")
    table.add_row("⏱️ Estimation", data.get('fields', {}).get('estimation', 'N/A'))

    console.print(Panel(table, title=f"[bold]{data['title']}[/bold]", border_style="blue"))

    # Overview
    if data.get('overview'):
        console.print("\n[bold cyan]📖 Overview / Deep Dive[/bold cyan]")
        console.print(Markdown(data['overview']))

    # Math - Using the updated cleaner
    if data.get('mathematical_context'):
        console.print("\n[bold magenta]📐 Mathematical Context[/bold magenta]")
        console.print(clean_math(data['mathematical_context']))

    # Lists
    for label, key, color in [("✅ Acceptance Criteria", "acceptance_criteria", "yellow"), 
                              ("🧪 Testing Scenarios", "testing_scenarios", "blue")]:
        items = data.get(key, [])
        if items:
            console.print(f"\n[bold {color}]{label}[/bold {color}]")
            for item in items:
                console.print(f"  [green]•[/green] {item}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[yellow]Usage: ticket <TICKET-ID>[/yellow]")
    else:
        view_ticket(sys.argv[1])