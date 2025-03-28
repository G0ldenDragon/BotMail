import tkinter
from tkinter import ttk

class MainApplication(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application Multi-Pages")
        self.geometry("400x300")

        self.frames = {}
        for F in (Page1, Page2):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Page1)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Page1(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        label = ttk.Label(self, text="Page 1")
        label.pack(pady=10)
        button = ttk.Button(self, text="Aller à la Page 2", command=lambda: parent.show_frame(Page2))
        button.pack()

class Page2(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        label = ttk.Label(self, text="Page 2")
        label.pack(pady=10)
        button = ttk.Button(self, text="Retour à la Page 1", command=lambda: parent.show_frame(Page1))
        button.pack()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
