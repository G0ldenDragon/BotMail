import tkinter as tk

class PageExample1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Page 1 : " + str(self.controller.models[PageExample1].data))
        label.pack(pady=10)
        button = tk.Button(self, text="Aller à la Page 2", command=lambda: self.controller.show_page("PageExample2"))
        button.pack()