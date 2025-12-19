# Dotfiles & Utilities

This repository contains my personal development environment configuration (Vim, Vimspector) and custom command-line utilities.

## 📂 Repository Structure

* **`/scripts`**: Python command-line utilities (e.g., `concat.py`).
* **`/vim`**: Configuration for Vim and Vimspector debugging.
* **`install.sh`**: Automated setup script for macOS/Linux.
* **`install.ps1`**: Automated setup script for Windows.

-----

## 🛠 One-Time Installation

### Option A: Automatic Setup (Recommended)

**On macOS / Linux:**
Run the install script to symlink configurations and install Vim-Plug.
```bash
chmod +x install.sh
./install.sh
````

**On Windows:**
Run the PowerShell script (Administrator privileges may be required for symlinks).

```powershell
.\install.ps1
```

### Option B: Manual Setup

If you prefer to set up manually, you need to:

1.  Symlink `vim/vimrc` to `~/.vimrc` (or `~/_vimrc` on Windows).
2.  Symlink `vim/vimspector.json` to `~/.vimspector.json`.
3.  Add the `scripts` directory to your System PATH.

-----

## 🐍 Command-Line Utilities

### `concat.py`

A powerful Python script to find and concatenate files matching a specific pattern.

**Setup:**
Ensure the `scripts` folder is in your PATH.

```bash
# MacOS/Linux (in ~/.zshrc or ~/.bashrc)
export PATH="$PATH:$HOME/Repos/dotfiles/scripts"
```

**Dependencies:**

```bash
pip3 install --break-system-packages pyperclip
chmod +x scripts/concat.py
```

**Usage:**

```bash
# Copy all Markdown files in current folder to clipboard
concat.py . -c
```

-----

## 🎮 Vim & Debugging

This repo includes a "God Mode" configuration for C\# and Python debugging using **Vimspector**.

### Key Features

  * **Smart C\# F5:** Automatically checks for unsaved changes, rebuilds the project, and restarts the debugger.
  * **"Jump-Mark-Return" Workflow:** Optimized for navigating C\# code without leaving the keyboard.

### Controls Cheat Sheet

| Key | Action | Note |
| :--- | :--- | :--- |
| **F5** | **Start / Continue** | Smart Build (C\#) or Run (Python). |
| **F3** | **Reset** | Closes all debug windows. |
| **F9** | **Breakpoint** | Toggle breakpoint. |
| **F10** | **Step Over** | Next line. |
| **F11** | **Step Into** | Step into function. |

*See `vim/debug_workflow.md` for the full workflow guide.*