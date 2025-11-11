import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import sys
import os

# Directory containing demos (current folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# List demo files to include (filter .py demos)
DEMO_FILES = [
    f for f in os.listdir(BASE_DIR)
    if f.endswith('.py') and f not in ('launcher.py',)
]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('MediaPipe Demos Launcher')
        self.geometry('700x420')
        self.process = None

        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)

        lbl = ttk.Label(frm, text='Available demos:')
        lbl.pack(anchor=tk.W)

        self.listbox = tk.Listbox(frm, height=12)
        for f in sorted(DEMO_FILES):
            self.listbox.insert(tk.END, f)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill=tk.X, pady=8)

        run_btn = ttk.Button(btn_frame, text='Run', command=self.run_selected)
        run_btn.pack(side=tk.LEFT, padx=4)

        stop_btn = ttk.Button(btn_frame, text='Stop', command=self.stop_process)
        stop_btn.pack(side=tk.LEFT, padx=4)

        open_dir_btn = ttk.Button(btn_frame, text='Open Folder', command=self.open_folder)
        open_dir_btn.pack(side=tk.LEFT, padx=4)

        choose_btn = ttk.Button(btn_frame, text='Choose File...', command=self.choose_file)
        choose_btn.pack(side=tk.LEFT, padx=4)

        self.output_text = tk.Text(frm, height=8)
        self.output_text.pack(fill=tk.BOTH, expand=False)
        self.output_text.insert(tk.END, 'Output/Status...')

    def run_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo('Info', 'Please select a demo to run')
            return
        filename = self.listbox.get(sel[0])
        self.run_file(os.path.join(BASE_DIR, filename))

    def choose_file(self):
        path = filedialog.askopenfilename(initialdir=BASE_DIR, filetypes=[('Python files', '*.py')])
        if path:
            self.run_file(path)

    def run_file(self, path):
        if self.process:
            messagebox.showwarning('Warning', 'A demo is already running. Stop it first.')
            return
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, f'Running: {path}\n')

        # Launch as a separate Python process, using the same interpreter
        try:
            # Use creationflags to open a new console on Windows so OpenCV windows work reliably
            if sys.platform == 'win32':
                self.process = subprocess.Popen([sys.executable, path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                self.process = subprocess.Popen([sys.executable, path])
        except Exception as e:
            messagebox.showerror('Error', f'Failed to start process: {e}')
            self.process = None

    def stop_process(self):
        if not self.process:
            messagebox.showinfo('Info', 'No demo is running')
            return
        try:
            self.process.terminate()
            self.process.wait(timeout=3)
            self.output_text.insert(tk.END, 'Process terminated.\n')
        except Exception as e:
            self.output_text.insert(tk.END, f'Error stopping process: {e}\n')
        finally:
            self.process = None

    def open_folder(self):
        os.startfile(BASE_DIR)

if __name__ == '__main__':
    app = App()
    app.mainloop()
