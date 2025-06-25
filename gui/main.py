from ui import create_ui
from bot_process import stop_bot
import tkinter as tk
import atexit

root = tk.Tk()
output_box, buttons = create_ui(root)
buttons["stop"].config(state="disabled")

atexit.register(stop_bot)
root.mainloop()