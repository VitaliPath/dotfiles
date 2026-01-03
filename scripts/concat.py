#!/usr/bin/env python3
import os
import fnmatch
import argparse
import sys

# Try to import pyperclip, which is needed for clipboard functionality.
# Provide a helpful message if it's not installed.
try:
    import pyperclip
except ImportError:
    pyperclip = None

# --- Configuration (Hardcoded Exclusions) ---
# Add any directory names you want to skip to this set.
# This is case-sensitive.
EXCLUDE_DIRS = {
    'node_modules', 
    'bin', 
    'obj', 
    '.git', 
    '__pycache__', 
    '.idea',
    'workbench',
    '.venv'
}

def concatenate_files(root_dir, file_patterns, script_name, dynamic_exclusions):
    """
    Walks through a directory tree and concatenates the content of files 
    matching any of the given patterns, while applying dynamic exclusions.

    Args:
        root_dir (str): The path to the root directory to start searching from.
        file_patterns (list): A list of patterns for files to match (e.g., ['*.py', '*.md']).
        script_name (str): The name of this script, to avoid adding itself.
        dynamic_exclusions (set): A set of strings (paths or filenames) to exclude.

    Returns:
        str: A single string containing the concatenated content of all found files.
    """
    concatenated_content = []
    print(f"\nStarting search in: {os.path.abspath(root_dir)}")
    print(f"Searching for patterns: {', '.join(file_patterns)}")
    print(f"Hardcoded excluded directories: {', '.join(EXCLUDE_DIRS)}")
    if dynamic_exclusions:
        print(f"Dynamically excluded items: {', '.join(dynamic_exclusions)}")
    
    # Use the absolute path for root to handle path comparisons correctly
    abs_root_dir = os.path.abspath(root_dir)

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        
        # --- 1. Hardcoded Directory Exclusion ---
        # We modify 'dirnames' in-place to prevent os.walk from descending
        # into the directories we want to skip.
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        # --- 2. Dynamic Directory Exclusion ---
        # Exclude directories if they are specified in the dynamic_exclusions set.
        # This checks the full relative path to the root.
        dirnames[:] = [
            d for d in dirnames 
            if os.path.relpath(os.path.join(dirpath, d), abs_root_dir) not in dynamic_exclusions
        ]

        # --- Find and read matching files ---
        for filename in filenames:
            
            filepath = os.path.join(dirpath, filename)
            rel_filepath = os.path.relpath(filepath, abs_root_dir)

            # Check if the filename matches ANY of the provided patterns
            if any(fnmatch.fnmatch(filename, pattern) for pattern in file_patterns):
                
                # --- 3. Skip the script file itself (existing logic) ---
                if os.path.basename(filename) == script_name and dirpath == os.path.dirname(os.path.abspath(sys.argv[0])):
                    continue

                # --- 4. Dynamic File Exclusion ---
                # Check against the full relative path OR just the filename
                if rel_filepath in dynamic_exclusions or filename in dynamic_exclusions:
                    print(f"  - Skipping (Excluded): {rel_filepath}")
                    continue

                # We add a header to separate the content of each file
                header = f"\n# --- START: {rel_filepath} ---\n"
                footer = f"\n# --- END: {rel_filepath} ---\n"
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        concatenated_content.append(header + content + footer)
                        print(f"  + Added: {rel_filepath}")
                except Exception as e:
                    print(f"  ! Error reading file {filepath}: {e}")
                    
    return "".join(concatenated_content)

def main():
    """
    Main function to parse arguments and run the script.
    """
    # --- Set up command-line argument parsing ---
    parser = argparse.ArgumentParser(
        description="A script to find and concatenate files of specific types within a directory tree.",
        formatter_class=argparse.RawTextHelpFormatter # For better help text formatting
    )
    
    parser.add_argument(
        'directory',
        nargs='?', # Makes the argument optional
        default=os.getcwd(), # Defaults to the current working directory
        help="The root directory to search in.\nDefaults to the current directory if not provided."
    )
    
    parser.add_argument(
        '-o', '--output',
        help="Optional: The name of the file to save the output to."
    )
    
    parser.add_argument(
        '-c', '--copy',
        action='store_true', # Makes this a flag, e.g., -c
        help="Optional: Copy the output to the clipboard instead of printing it.\nRequires the 'pyperclip' library."
    )
    
    parser.add_argument( # <--- NEW ARGUMENT ---
        '-e', '--exclude',
        type=str,
        default='',
        help="Optional: Comma-separated list of paths or filenames to exclude.\nExcludes are relative to the 'directory' argument.\nExample: 'tests/config.yaml,README.md'"
    ) # <--- END NEW ARGUMENT ---

    args = parser.parse_args()

    # --- Check for pyperclip if -c is used ---
    if args.copy and not pyperclip:
        print("\n❌ Error: The 'pyperclip' library is required for clipboard functionality.")
        print("Please install it by running: pip install pyperclip")
        return

    # --- Process Exclusions ---
    # Convert comma-separated string into a set of unique, stripped strings for fast lookup
    dynamic_exclusions = {p.strip() for p in args.exclude.split(',') if p.strip()}

    # --- Get user input for the file patterns ---
    try:
        patterns_input = input("Enter file patterns, separated by commas (e.g., *.md, *.sln, *.csproj): ")
        # Split the input string by commas and strip any whitespace from each pattern.
        file_patterns = [p.strip() for p in patterns_input.split(',') if p.strip()]
        
        if not file_patterns:
            print("Error: File pattern list cannot be empty.")
            return
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return

    # --- Run the main logic ---
    script_name = os.path.basename(sys.argv[0])
    full_content = concatenate_files(args.directory, file_patterns, script_name, dynamic_exclusions)

    if not full_content:
        print(f"\nNo files matching any of these patterns '{patterns_input}' were found in '{os.path.abspath(args.directory)}'.")
        return

    # --- Handle the output ---
    # The order of priority is: File > Clipboard > Console
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(full_content)
            print(f"\n✅ Success! All content has been written to '{args.output}'.")
        except IOError as e:
            print(f"\n❌ Error: Could not write to output file '{args.output}'. Reason: {e}")
    elif args.copy:
        try:
            pyperclip.copy(full_content)
            print("\n✅ Success! Content has been copied to the clipboard.")
        except pyperclip.PyperclipException as e:
            print(f"\n❌ Error: Could not copy to clipboard. Reason: {e}")
    else:
        print("\n--- CONCATENATED CONTENT ---\n")
        print(full_content)


if __name__ == "__main__":
    main()