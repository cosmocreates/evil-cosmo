import tkinter as tk
from tkinter import font
from bot_process import start_bot, stop_bot
from utils import rgb_to_hex

def create_ui(root):
    icon = tk.PhotoImage(file='assets/images/evil-cosmo.png')
    root.iconphoto(False, icon)
    root.title("Bot Controller")
    root.configure(bg='#1e1e1e')
    root.geometry("500x400")

    try:
        ui_font = font.Font(family="JetBrains Mono", size=10)
        output_font = font.Font(family="JetBrains Mono", size=9)
    except:  # noqa: E722
        ui_font = font.Font(family="Courier", size=10)
        output_font = font.Font(family="Courier", size=9)

    top_frame = tk.Frame(root, bg='#1e1e1e')
    top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    left_info_frame = tk.Frame(top_frame, bg='#1e1e1e')
    left_info_frame.pack(side=tk.LEFT, anchor='w')

    tk.Label(
        left_info_frame,
        text="Bot Control",
        bg='#1e1e1e',
        fg='white',
        font=(ui_font.actual('family'), 14, 'bold')
    ).pack(anchor='w')

    tk.Label(
        left_info_frame,
        text="Easy access to starting/stopping the bot, refreshing commands, and more.",
        bg='#1e1e1e',
        fg='#cccccc',
        font=(ui_font.actual('family'), 9),
        wraplength=350,
        justify='left'
    ).pack(anchor='w')

    button_frame = tk.Frame(top_frame, bg='#1e1e1e')
    button_frame.pack(side=tk.RIGHT, anchor='ne', padx=5)

    style = {
        "bg": "#3c3c3c",
        "fg": "white",
        "font": ui_font,
        "padx": 6,
        "pady": 4,
        "bd": 0,
        "highlightthickness": 0
    }

    output_box = tk.Text(
        root,
        bg="#1e1e1e",
        fg="white",
        insertbackground="white",
        font=output_font,
        wrap=tk.WORD
    )
    output_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    tk.Button(button_frame, text="Start Bot", command=lambda: start_bot(output_box), **style).pack(
        side='top', anchor='e', pady=(0, 5), padx=5
    )
    tk.Button(button_frame, text="Stop Bot", command=stop_bot, **style).pack(
        side='top', anchor='e', pady=(0, 5), padx=5
    )
    tk.Button(button_frame, text="Refresh Commands", command=stop_bot, **style).pack(
        side='top', anchor='e', padx=5
    )

    output_box.tag_config("js", foreground=rgb_to_hex(100, 180, 255))
    output_box.tag_config("py", foreground=rgb_to_hex(90, 245, 90))

    root.protocol("WM_DELETE_WINDOW", lambda: (stop_bot(), root.destroy()))
    return output_box
