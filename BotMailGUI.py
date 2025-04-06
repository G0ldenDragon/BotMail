import tkinter as tk
import sv_ttk
import platform

from Views.PageExample2 import PageExample2

from Models.EnvironmentVariable_Model import EnvironmentVariable_Model
from Models.ModelExample1 import ModelExample1
from Models.ModelExample2 import ModelExample2
from Models.ModelExample3 import ModelExample3

from Controllers.LanguageWindow_Controller import LanguageWindow_Controller
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


        # Initialisation des modèles
        environmentVariable_Model = EnvironmentVariable_Model()
        modelExample2 = ModelExample2()
        modelExample3 = ModelExample3()


        # Initialisation des contrôleurs avec une référence à l'application principale pour initialisation des vues en interne
        self.controllers = {
            "languageWindow_Controller" : LanguageWindow_Controller(container, environmentVariable_Model),
            # controllerExample2 = ControllerExample2(self.models["PageExample2"], None)
            # controllerExample3 = ControllerExample3(self.models["PageExample3"], None)
        }


        # Afficher la première page par défaut
        self.show_page("languageWindow_Controller")

    def show_page(self, controller):
        """Affiche une page donnée par son nom"""
        self.controllers[controller].showPage()


if __name__ == "__main__":
    app = BotMailGUI()
    app.mainloop()
