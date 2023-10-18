# utils.py
import sys
import time
import threading
import subprocess

def open_in_sublime(file_path):
    # Path to the Sublime Text executable
    # Update this path according to your Sublime Text installation
    sublime_path = "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl"  # for macOS
    # sublime_path = "C:\\Program Files\\Sublime Text 3\\sublime_text.exe"  # for Windows

    # Open the file in Sublime Text
    subprocess.run([sublime_path, "--new-window", file_path])
	
def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def loading_animation(shared_state):
    spinner = spinning_cursor()
    while not shared_state.get('stop_loading', False):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
    sys.stdout.write(' \r')  # Reset the cursor position

def start_loading_animation():
    shared_state = {'stop_loading': False}
    loading_thread = threading.Thread(target=loading_animation, args=(shared_state,))
    loading_thread.start()
    return loading_thread, lambda: shared_state.update({'stop_loading': True})