import tkinter as tk
import subprocess
import signal
import threading
import re
import time

from colors import COLOR_TAGS

ansi_escape = re.compile(r'\x1b\[([0-9;]*?)m')

refresh_cooldown = 3
stop_cooldown = 3
refresh_timeout = 5
bot_process = None
main_file = 'index.js'

def print_py(output_widget, message):
    prefix = "[PYTHON]"
    output_widget.insert('end', prefix, 'py')
    output_widget.insert('end', ' ' + message, 'pybg')
    output_widget.see('end')

def read_output(pipe, text_widget, _):
    for line in iter(pipe.readline, b''):
        decoded = line.decode(errors='ignore')

        for prefix, color_tag in COLOR_TAGS.items():
            if decoded.startswith(prefix):
                if prefix == '[PYTHON]':
                    text_widget.insert('end', prefix, 'py')
                    message = decoded[len(prefix):]
                    text_widget.insert('end', message, 'pybg')
                else:
                    text_widget.insert('end', prefix, color_tag)
                    message = decoded[len(prefix):]
                    text_widget.insert('end', message, 'white')
                break
        else:
            text_widget.insert('end', decoded, 'white')

        text_widget.see('end')
    pipe.close()

def start_bot(output_widget, start_button, stop_button, refresh_button):
    global bot_process
    if bot_process is None:
        output_widget.delete('1.0', tk.END)
        bot_process = subprocess.Popen(
            ['node', main_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        print_py(output_widget, f"Running {main_file} from subprocess/node.js...\n")

        threading.Thread(
            target=read_output,
            args=(bot_process.stdout, output_widget, "js"),
            daemon=True
        ).start()

        start_button.config(state='disabled')
        stop_button.config(state='disabled')
        refresh_button.config(state='disabled')

        output_widget.after(stop_cooldown * 1000, lambda: stop_button.config(state='normal'))


def stop_bot(output_widget, start_button, stop_button, refresh_button):
    global bot_process
    if bot_process is not None:
        try:
            bot_process.send_signal(signal.CTRL_BREAK_EVENT)
        except:  # noqa: E722
            pass
        bot_process = None

        print_py(output_widget, "Successfully stopped the bot and JavaScript subprocesses.\n")
        start_button.config(state='normal')
        stop_button.config(state='disabled')
        refresh_button.config(state='normal')

def refresh_cmds(output_widget, start_button, stop_button, refresh_button):
    start_button.config(state='disabled')
    stop_button.config(state='disabled')
    refresh_button.config(state='disabled')

    output_widget.delete('1.0', tk.END)
    refresh_process = subprocess.Popen(
        ['node', 'tools/refresh-commands.js'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )

    print_py(output_widget, "Running refresh-commands.js from subprocess/node.js...\n")

    last_output_time = [time.time()]
    time_lock = threading.Lock()
    problem_printed = threading.Event()

    def read_output_with_timer(stream, widget):
        for line in iter(stream.readline, b''):
            with time_lock:
                last_output_time[0] = time.time()
            decoded = line.decode('utf-8', errors='replace')
            for prefix, color_tag in COLOR_TAGS.items():
                if decoded.startswith(prefix):
                    if prefix == '[PYTHON]':
                        widget.insert('end', prefix, 'py')
                        message = decoded[len(prefix):]
                        widget.insert('end', message, 'pybg')
                    else:
                        widget.insert('end', prefix, color_tag)
                        message = decoded[len(prefix):]
                        widget.insert('end', message, 'white')
                    break
            else:
                widget.insert('end', decoded, 'white')
            widget.see('end')
        stream.close()

    def monitor_process(proc):
        proc.wait()
        if not problem_printed.is_set():
            print_py(output_widget, "Refreshed all commands.\n")
        start_button.config(state='normal')
        stop_button.config(state='disabled')
        output_widget.after(refresh_cooldown * 1000, lambda: refresh_button.config(state='normal'))

    def timeout_checker(proc):
        while proc.poll() is None:
            with time_lock:
                no_output_duration = time.time() - last_output_time[0]
            if no_output_duration > refresh_timeout and not problem_printed.is_set():
                print_py(output_widget, "Are you refreshing commands too fast?\n")
                print_py(output_widget, "Taking a bit longer than usual... If nothing happens soon, you should probably try refreshing commands again.\n")
                start_button.config(state='normal')
                stop_button.config(state='disabled')
                output_widget.after(refresh_cooldown * 1000, lambda: refresh_button.config(state='normal'))
                problem_printed.set()
                break
            time.sleep(1)

    threading.Thread(
        target=read_output_with_timer,
        args=(refresh_process.stdout, output_widget),
        daemon=True
    ).start()

    threading.Thread(
        target=monitor_process,
        args=(refresh_process,),
        daemon=True
    ).start()

    threading.Thread(
        target=timeout_checker,
        args=(refresh_process,),
        daemon=True
    ).start()