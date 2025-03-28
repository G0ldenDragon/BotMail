import tkinter as tk

class PageExample3(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Page 3")
        label.pack(pady=10)
        button = tk.Button(self, text="Retour à la Page 1", command=lambda: self.controller.show_page("PageExample1"))
        button.pack()