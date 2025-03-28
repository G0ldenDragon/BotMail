import tkinter
import sv_ttk
import platform


from Controllers import ControllerExample1, ControllerExample3, ControllerExample2

from Models.ModelExample1 import ModelExample1
from Models.ModelExample2 import ModelExample2
from Models.ModelExample3 import ModelExample3

from Views.PageExample1 import PageExample1
from Views.PageExample2 import PageExample2
from Views.PageExample3 import PageExample3


# Application principale
class BotMailGUI(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("BotMailGUI")
        self.resizable(True, True)
        sv_ttk.set_theme("dark")

        self.os_name = platform.system()



        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.models = {
            PageExample1: ModelExample1(),
            PageExample2: ModelExample2(),
            PageExample3: ModelExample3()
        }
        self.controllers = {
            PageExample1: ControllerExample1,
            PageExample2: ControllerExample2,
            PageExample3: ControllerExample3
        }

        for F in (PageExample1, PageExample2, PageExample3):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            controller = self.controllers[F](self.models[F], frame)

        self.show_page(PageExample1)

    def show_page(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



if __name__ == "__main__":
    app = BotMailGUI()
    app.mainloop()