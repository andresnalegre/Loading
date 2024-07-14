import tkinter as tk
from tkinter import ttk
import threading
import time

class LoadingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x80")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.loading_complete = False

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TProgressbar",
                             thickness=20,
                             troughcolor='#f0f0f0',
                             background='#4caf50',
                             troughrelief='flat',
                             relief='flat',
                             bordercolor='#c0c0c0',  # Cor da borda
                             lightcolor='#c0c0c0',  # Cor do lado claro da borda
                             darkcolor='#c0c0c0')   # Cor do lado escuro da borda
        self.style.map("TProgressbar",
                       troughcolor=[('!disabled', '#f0f0f0')],
                       background=[('!disabled', '#4caf50')])

        self.frame = tk.Frame(self.root, bg='#f0f0f0')
        self.frame.pack(expand=True)

        self.percent_label = tk.Label(self.frame, text="0%", font=("Helvetica", 12), bg='#f0f0f0', fg='#000000')
        self.percent_label.pack(pady=(5, 5))

        self.progress_bar = ttk.Progressbar(self.frame, orient="horizontal", length=250, mode="determinate", style="TProgressbar", maximum=100)
        self.progress_bar.pack(pady=(5, 10))

        self.title_thread = threading.Thread(target=self.animate_title)
        self.title_thread.daemon = True
        self.title_thread.start()

        self.start_loading()

    def animate_title(self):
        while not self.loading_complete:
            for suffix in ["", ".", "..", "..."]:
                if self.loading_complete:
                    break
                self.root.title(f"Loading{suffix}")
                time.sleep(0.5)

    def simulate_loading(self):
        try:
            for i in range(101):
                time.sleep(0.05)
                if not self.root.winfo_exists():
                    return
                self.progress_bar['value'] = i
                self.percent_label.config(text=f"{i}%")
                self.root.update_idletasks()
            self.loading_complete = True
            if self.root.winfo_exists():
                self.root.title("Completed!")
        except tk.TclError:
            pass

    def start_loading(self):
        loading_thread = threading.Thread(target=self.simulate_loading)
        loading_thread.start()

    def on_closing(self):
        self.loading_complete = True
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LoadingApp()
    app.run()
