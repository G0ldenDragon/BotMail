import tkinter as tk
import sv_ttk
import platform

from Views.LanguageWindow import LanguageWindow
from Views.PageExample2 import PageExample2
from Views.PageExample3 import PageExample3

from Models.ModelExample1 import ModelExample1
from Models.ModelExample2 import ModelExample2
from Models.ModelExample3 import ModelExample3

from Controllers.LanguageWindowController import LanguageWindowController
from Controllers.ControllerExample2 import ControllerExample2
from Controllers.ControllerExample3 import ControllerExample3


class BotMailGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BotMailGUI")
        self.resizable(True, True)

        # Configuration du thème Sun Valley
        sv_ttk.set_theme("dark")

        self.os_name = platform.system()

        # Conteneur principal pour les pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionnaires pour stocker frames, modèles et contrôleurs
        self.frames = {}
        self.models = {
            "LanguageWindow": ModelExample1(),
            "PageExample2": ModelExample2(),
            "PageExample3": ModelExample3()
        }

        # Initialisation des contrôleurs avec une référence à l'application principale
        self.controllers = {
            "LanguageWindow": LanguageWindowController(self.models["LanguageWindow"], None, self),
            "PageExample2": ControllerExample2(self.models["PageExample2"], None),
            "PageExample3": ControllerExample3(self.models["PageExample3"], None)
        }

        # Initialisation des pages
        for page_name, page_class in [
            ("LanguageWindow", LanguageWindow),
            ("PageExample2", PageExample2),
            ("PageExample3", PageExample3)
        ]:
            frame = page_class(container, self.controllers[page_name])  # Passer le contrôleur à la vue
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Afficher la première page par défaut
        self.show_page("LanguageWindow")

    def show_page(self, page_name):
        """Affiche une page donnée par son nom"""
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = BotMailGUI()
    app.mainloop()
