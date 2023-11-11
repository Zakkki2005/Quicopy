import pyperclip
import pymsgbox
import threading
import win32gui
import win32con
import tkinter as tk
import os
import configparser

# Get the path of the INI file in the same folder as the executable
ini_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")

# Create a configparser object and read the INI file
config = configparser.ConfigParser()
config.read(ini_file)

# Get the markdown file path from the INI file
markdown_file = config.get("Settings", "MarkdownFile", fallback="D:\\TempSaved.md")

# Global variable to track the program state
is_running = False

def save_selected_text():
    # Get the text from the clipboard
    selected_text = pyperclip.paste()

    # Truncate the selected text if it exceeds 5 lines
    lines = selected_text.split("\n")
    if len(lines) > 5:
        selected_text = "\n".join(lines[:5]) + " ..."

    # Display a pop-up notification for confirmation
    message = f"您已选中以下文字：\n{selected_text}\n\n您要将以上文字粘贴至文件中吗？"
    result = pymsgbox.confirm(message, title="保存选中的文字", buttons=["是", "否"])

    # If "Yes" button is clicked, append the selected text to the markdown file
    if result == "是":
        with open(markdown_file, "a") as f:
            f.write(selected_text + "\n")

def clipboard_listener():
    previous_clipboard = pyperclip.paste()
    while is_running:
        current_clipboard = pyperclip.paste()
        if current_clipboard != previous_clipboard:
            save_selected_text()
            previous_clipboard = current_clipboard

def toggle_listener():
    global is_running
    if is_running:
        stop_listener()
    else:
        start_listener()

def start_listener():
    global is_running
    if not is_running:
        is_running = True
        listener_thread = threading.Thread(target=clipboard_listener, daemon=True)
        listener_thread.start()
        toggle_button.config(text="停止")

def stop_listener():
    global is_running
    is_running = False
    toggle_button.config(text="启动！")

def show_about():
    message = "Quicopy 缝合怪\n一个为了让只会 Ctrl+C 和 Ctrl+V 的大学牲解放 Ctrl+V 的工具\nCreated by Zakkki_ and Powered by ChatGPT"
    pymsgbox.alert(message, title="关于 Quicopy 缝合怪")

# Create the GUI window
window = tk.Tk()
window.title("Quicopy 缝合怪")
window.geometry("100x100")
window.resizable(False, False)
window.attributes("-toolwindow", 1)

# Toggle button
toggle_button = tk.Button(window, text="启动！", command=toggle_listener, width=10, height=2)
toggle_button.pack(pady=5)

# About button
about_button = tk.Button(window, text="关于", command=show_about, width=10, height=1)
about_button.pack(pady=5)

# Set the window to be on top of all windows
window.wm_attributes("-topmost", 1)

# Start the main GUI loop
window.mainloop()
