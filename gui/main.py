from ui import create_ui
from bot_process import stop_bot
import tkinter as tk
import atexit

root = tk.Tk()
output_box = create_ui(root)

atexit.register(stop_bot)
root.mainloop()