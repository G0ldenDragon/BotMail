import tkinter as tk

class PageExample2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Page 2")
        label.pack(pady=10)
        button = tk.Button(self, text="Aller à la Page 3", command=lambda: self.controller.show_page("PageExample3"))
        button.pack()