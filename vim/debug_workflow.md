# Vimspector Debugging Workflow

## 🚀 The "Jump-Mark-Return" Method
**Problem:** `F11` (Step Into) sometimes fails to jump into closed files in C#.
**Solution:** Don't wait for the tool. Go there yourself.

1.  **JUMP:** Press `Ctrl + P`, type the filename (e.g., `MyVal`), and hit `Enter`.
2.  **MARK:** Scroll to the method and press `F9` to toggle a breakpoint.
3.  **RETURN:** Press `Ctrl + ^` (swaps back to the previous buffer instantly).
4.  **RUN:** Press `F5` to let the debugger run to your new mark.

---

## 🎮 The Controls ("Human Mode")

| Key | Action | Context |
| :--- | :--- | :--- |
| **F5** | **Start / Continue** | **C#:** Checks for unsaved changes $\rightarrow$ Rebuilds $\rightarrow$ Restarts.<br>**Active:** Just Continues. |
| **F3** | **Stop / Reset** | The "Eject" button. Closes all debug windows. |
| **F9** | **Toggle Breakpoint** | Adds/Removes the red dot `●`. |
| **F10** | **Step Over** | Run line, skip entering functions. |
| **F11** | **Step Into** | Enter function (Use "Jump-Mark-Return" if file is closed). |
| **F12** | **Step Out** | Return to caller. |

## 🧭 Window Navigation
* **Move Focus:** `Ctrl+w` then `h` / `j` / `k` / `l`
* **Quick Return:** If stuck in Stack Trace, press `Ctrl+w` then `p` (Previous window) to get back to code.
