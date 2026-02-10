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
    
    # Map common LaTeX commands to Unicode for terminal clarity
    subs = {
        r"\max": "max",
        r"\log": "log",
        r"\frac": "", 
        r"\times": "×",
        r"\partial": "∂",
        r"\dots": "...",
        r"\beta": "β",
        r"\epsilon": "ε",
        r"\sum": "Σ",
        r"\Delta": "Δ",
        r"\left(": "(",
        r"\right)": ")",
    }
    
    for lat, uni in subs.items():
        text = text.replace(lat, uni)
    
    # Handle \frac{a}{b} -> (a/b) - handles alphanumeric and underscores
    text = re.sub(r"\{([\w_]+)\}\{([\w_]+)\}", r"(\1/\2)", text)
    
    # Remove remaining curly braces and dollar signs
    text = re.sub(r"[\${}]", "", text)
    
    return text.strip()

def find_and_load_ticket(ticket_id):
    """Search inside all JSON files for a ticket with the matching 'Id'."""
    kb_base = Path("/Users/seanstoneburner/Repos/Stoneburner-Knowledge-Base")
    
    # 1. Iterate through all .json files in the repo
    for path in kb_base.rglob("*.json"):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                
                # 2. Since your JSON files contain lists of tickets:
                if isinstance(data, list):
                    for ticket in data:
                        if ticket.get("Id") == ticket_id:
                            return ticket
                # 3. Handle case where JSON is a single ticket object
                elif isinstance(data, dict):
                    if data.get("Id") == ticket_id:
                        return data
        except (json.JSONDecodeError, OSError):
            continue 
            
    return None

def view_ticket(ticket_id):
    # Call the new search function that returns the data directly
    data = find_and_load_ticket(ticket_id)
    
    if not data:
        console.print(f"[red]Error: Ticket {ticket_id} not found in any knowledge base files.[/red]")
        return

    # Header Panel - Updated to PascalCase Keys
    table = Table(show_header=False, expand=True, box=None)
    table.add_column("Key", style="cyan", width=15)
    table.add_column("Value", style="white")
    
    # Note the .get('Key') changes below
    t_id = data.get('Id', 'N/A')
    t_state = data.get('State', 'N/A')
    t_subsystem = data.get('Subsystem', 'N/A')
    t_component = data.get('Component', 'N/A')
    t_complexity = data.get('Complexity', 'N/A')
    t_estimation = data.get('Estimation', 'N/A')
    t_summary = data.get('Summary', 'No Title')

    table.add_row("🎫 Ticket ID", f"[bold green]{t_id}[/bold green] ({t_state})")
    table.add_row("📂 Subsystem", f"{t_subsystem} -> {t_component}")
    table.add_row("📊 Complexity", f"[yellow]{t_complexity}[/yellow]")
    table.add_row("⏱️ Estimation", t_estimation)

    console.print(Panel(table, title=f"[bold]{t_summary}[/bold]", border_style="blue"))

    # Description Rendering - Updated to PascalCase Key
    description = data.get('Description')
    if description:
        # STEP 1: Process LaTeX before the Markdown parser sees it
        def math_replacer(match):
            return clean_math(match.group(1))

        # Replace $$block$$ first, then $inline$
        description = re.sub(r"\$\$(.*?)\$\$", math_replacer, description, flags=re.DOTALL)
        description = re.sub(r"\$(.*?)\$", math_replacer, description)

        # STEP 2: Render as Markdown
        console.print(Markdown(description))
    
    # Legacy fallbacks for older JSON formats
    elif data.get('overview'):
        console.print("\n[bold cyan]📖 Overview[/bold cyan]")
        console.print(Markdown(data['overview']))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[yellow]Usage: ticket <TICKET-ID>[/yellow]")
    else:
        view_ticket(sys.argv[1])