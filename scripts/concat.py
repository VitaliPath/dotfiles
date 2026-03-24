#!/usr/bin/env python3
import os
import fnmatch
import argparse
import sys

try:
    import pyperclip
except ImportError:
    pyperclip = None

# --- Configuration (Hardcoded Exclusions) ---
EXCLUDE_DIRS = {
    'node_modules', 
    'bin', 
    'obj',
    'publish',
    '.git', 
    '__pycache__', 
    '.idea',
    'workbench',
    '.venv',
    'venv',
    '.pytest_cache'
}

def log(message):
    """Helper to print to stderr so it doesn't pollute piped output."""
    print(message, file=sys.stderr)

def concatenate_files(root_dir, file_patterns, script_name, dynamic_exclusions):
    concatenated_content = []
    log(f"\nStarting search in: {os.path.abspath(root_dir)}")
    log(f"Searching for patterns: {', '.join(file_patterns)}")
    log(f"Hardcoded excluded directories: {', '.join(EXCLUDE_DIRS)}")
    if dynamic_exclusions:
        log(f"Dynamically excluded items: {', '.join(dynamic_exclusions)}")
    
    abs_root_dir = os.path.abspath(root_dir)

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        
        allowed_dirs = []
        for d in dirnames:
            full_path = os.path.join(dirpath, d)
            rel_path = os.path.relpath(full_path, abs_root_dir)
            if d in dynamic_exclusions or rel_path in dynamic_exclusions:
                log(f"  - Skipping Directory (Excluded): {rel_path}")
            else:
                allowed_dirs.append(d)
        dirnames[:] = allowed_dirs

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            rel_filepath = os.path.relpath(filepath, abs_root_dir)

            if any(fnmatch.fnmatch(filename, pattern) for pattern in file_patterns):
                if os.path.basename(filename) == script_name and dirpath == os.path.dirname(os.path.abspath(sys.argv[0])):
                    continue

                if rel_filepath in dynamic_exclusions or filename in dynamic_exclusions:
                    log(f"  - Skipping File (Excluded): {rel_filepath}")
                    continue

                header = f"\n# --- START: {rel_filepath} ---\n"
                footer = f"\n# --- END: {rel_filepath} ---\n"
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if not content.strip():
                            content = "(empty file)"
                        concatenated_content.append(header + content + footer)
                        log(f"  + Added: {rel_filepath}")
                except Exception as e:
                    log(f"  ! Error reading file {filepath}: {e}")
                    
    return "".join(concatenated_content)

def main():
    parser = argparse.ArgumentParser(
        description="A script to find and concatenate files. Cleanly supports piping and redirection.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('directory', nargs='?', default=os.getcwd(), help="The root directory to search in.")
    parser.add_argument('-o', '--output', help="Output file name.")
    parser.add_argument('-c', '--copy', action='store_true', help="Copy output to clipboard.")
    parser.add_argument('-e', '--exclude', type=str, default='', help="Comma-separated exclusions.")

    args = parser.parse_args()

    if args.copy and not pyperclip:
        log("\n❌ Error: The 'pyperclip' library is required for clipboard functionality.")
        return

    dynamic_exclusions = {p.strip() for p in args.exclude.split(',') if p.strip()}

    try:
        # We print the prompt to stderr so it shows up even when stdout is redirected
        sys.stderr.write("Enter file patterns (e.g., *.md, *.py): ")
        sys.stderr.flush()
        patterns_input = sys.stdin.readline().strip()
        
        file_patterns = [p.strip() for p in patterns_input.split(',') if p.strip()]
        if not file_patterns:
            log("Error: File pattern list cannot be empty.")
            return
    except KeyboardInterrupt:
        log("\nOperation cancelled.")
        return

    script_name = os.path.basename(sys.argv[0])
    full_content = concatenate_files(args.directory, file_patterns, script_name, dynamic_exclusions)

    if not full_content:
        log(f"\nNo matching files found.")
        return

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(full_content)
            log(f"\n✅ Written to '{args.output}'.")
        except IOError as e:
            log(f"\n❌ Error writing file: {e}")
    elif args.copy:
        try:
            pyperclip.copy(full_content)
            log("\n✅ Copied to clipboard.")
        except pyperclip.PyperclipException as e:
            log(f"\n❌ Error copying: {e}")
    else:
        # This is the only thing that goes to Standard Output
        sys.stdout.write(full_content)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
