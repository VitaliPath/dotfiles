#!/usr/bin/env python3
import json
import sys
import os
import subprocess
from pathlib import Path

def find_ticket_in_manifests(ticket_id, kb_path):
    """Searches through all .json files for the specific Ticket ID."""
    for path in kb_path.rglob("*.json"):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for ticket in data:
                        if ticket.get("Id") == ticket_id:
                            return ticket
        except (json.JSONDecodeError, OSError):
            continue
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: ticket <TICKET-ID>")
        return

    ticket_id = sys.argv[1].upper()
    # Path to your Knowledge Base repo
    kb_base = Path(os.getenv("KB_PATH", os.path.expanduser("~/Repos/Stoneburner-Knowledge-Base")))
    
    ticket = find_ticket_in_manifests(ticket_id, kb_base)
    
    if not ticket:
        print(f"Error: Ticket {ticket_id} not found.")
        sys.exit(1)

    # Create a temporary markdown file to render the ticket
    temp_path = Path(f"/tmp/{ticket_id}.md")
    
    with open(temp_path, "w") as f:
        f.write(f"# {ticket['Id']}: {ticket['Summary']}\n\n")
        f.write(f"**Status:** {ticket.get('State', 'N/A')} | **Complexity:** {ticket.get('Complexity', 'N/A')}\n\n")
        f.write("---\n\n")
        f.write(ticket.get("Description", "No description provided."))

    # Open in VS Code. The '-r' flag opens it in the last active window if possible.
    subprocess.run(["code", str(temp_path)])
    print(f"Opening {ticket_id} in VS Code...")

if __name__ == "__main__":
    main()