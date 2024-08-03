import tkinter as tk
from tkinter import scrolledtext
from subprocess import Popen, PIPE, STDOUT
import sys
import threading

class PythonEmulator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Python Emulator")
        self.geometry("800x600")

        # Frame for the code editor and buttons
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Code editor
        self.code_editor = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, height=20)
        self.code_editor.pack(fill=tk.BOTH, expand=True)

        # Frame for the buttons
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(fill=tk.X)

        # Run button
        self.run_button = tk.Button(self.button_frame, text="Run Code", command=self.run_code)
        self.run_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Tabulation button
        self.tab_button = tk.Button(self.button_frame, text="Tabulation", command=self.insert_tab)
        self.tab_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Terminal for installing libraries
        self.terminal = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10)
        self.terminal.pack(fill=tk.BOTH, expand=True)
        self.terminal.bind("<Return>", self.execute_terminal_command)

    def run_code(self):
        code = self.code_editor.get("1.0", tk.END)
        self.execute_code(code)

    def execute_code(self, code):
        process = Popen([sys.executable, "-c", code], stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()

        self.terminal.insert(tk.END, output.decode())
        self.terminal.insert(tk.END, error.decode())
        self.terminal.yview(tk.END)

    def insert_tab(self):
        self.code_editor.insert(tk.INSERT, "    ")

    def execute_terminal_command(self, event):
        command = self.terminal.get("insert linestart", "insert lineend")
        self.terminal.insert(tk.END, "\n")
        threading.Thread(target=self.run_command, args=(command,)).start()
        return "break"

    def run_command(self, command):
        process = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
        output = process.communicate()[0]
        self.terminal.insert(tk.END, output.decode())
        self.terminal.yview(tk.END)

if __name__ == "__main__":
    app = PythonEmulator()
    app.mainloop()