from tkinter import ttk

class PageExample3(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="Page 3")
        label.pack(pady=10)
        button = ttk.Button(self, text="Retour à la Page 1", command=lambda: self.controller.show_page("LanguageWindow"))
        button.pack()