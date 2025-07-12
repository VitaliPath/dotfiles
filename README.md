# Command-Line Utilities

This repository is a collection of custom command-line scripts designed to streamline common development tasks.

-----

## Available Utilities

### `concat.py`

A powerful Python script to find and concatenate the contents of files matching a specific pattern within a directory and its subdirectories.

**Features:**

  * Recursively searches through the entire directory tree from your specified starting point.
  * Filters files by a given pattern (e.g., `*.py`, `*.md`, `*.txt`).
  * Outputs the combined content to the console, saves it to a file (`-o`), or copies it directly to the clipboard (`-c`).
  * Intelligently excludes common directories like `.git`, `node_modules`, and `__pycache__`.

-----

## One-Time Setup

To run these scripts from anywhere on your system simply by typing their name, you need to perform this one-time setup.

### Step 1: Add this Directory to your PATH

Your terminal finds commands by looking in a list of directories defined in your `PATH` variable. You need to add this `Utilities` folder to that list.

1.  **Open your shell configuration file.** If you're on a modern Mac, you're likely using the Zsh shell. This command will open the correct file in a simple editor:

    ```bash
    vim ~/.zshrc
    ```

2.  **Add the `Utilities` directory to your `PATH`**. Go to the very bottom of the file and add the following line. This tells your shell to add your utilities folder to the list of places it looks for commands.

    ```bash
    export PATH="$PATH:/Users/seanstoneburner/Repos/Utilities"
    ```

3.  **Save and close the file**. Press `Ctrl + X`, then `Y` to confirm saving, and finally `Enter`.

4.  **Apply the changes**. Your terminal needs to reload its configuration. You can either open a new terminal window or run this command in your existing one:

    ```bash
    source ~/.zshrc
    ```

### Step 2: Make Scripts Executable

For the system to recognize a script as a runnable command, you must give it "execute" permissions. You'll need to do this for each new script you add.

Run the following command from within your `Utilities` directory:

```bash
chmod +x concat.py
```

### Step 3: Check for Dependencies

Some scripts may require external Python libraries. `concat.py`, for example, needs `pyperclip` for its clipboard functionality.

Install it using this command:

```bash
pip3 install --break-system-packages pyperclip
```

-----

## Usage

After completing the setup, you can run any executable script from this folder from **anywhere** on your computer.

**Example for `concat.py`:**

1.  Navigate to any project directory you want to work in.
    ```bash
    cd /path/to/your/project
    ```
2.  Run the script. Here, we're combining all Markdown files and copying the result to the clipboard.
    ```bash
    concat.py . -c
    ```
3.  The script will then prompt you to enter the file pattern you're looking for.
    ```
    Enter the file pattern to search for (e.g., *.md, *.py, *.*): *.md
    ```

The combined content is now on your clipboard, ready to be pasted\!