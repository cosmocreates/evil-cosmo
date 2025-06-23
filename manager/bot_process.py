import subprocess
import signal
import threading

bot_process = None
main_file = 'index.js'

def read_output(pipe, text_widget, tag):
    for line in iter(pipe.readline, b''):
        text_widget.insert('end', line.decode(errors='ignore'), tag)
        text_widget.see('end')
    pipe.close()

def start_bot(output_widget):
    global bot_process
    if bot_process is None:
        bot_process = subprocess.Popen(
            ['node', main_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
        threading.Thread(
            target=read_output,
            args=(bot_process.stdout, output_widget, "js"),
            daemon=True
        ).start()

def stop_bot():
    global bot_process
    if bot_process is not None:
        try:
            bot_process.send_signal(signal.CTRL_BREAK_EVENT)
        except:  # noqa: E722
            pass
        bot_process = None
