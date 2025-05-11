import tkinter as tk
import sv_ttk
import platform

# ---------------------
# Imports

from Views.MainWindow_View import MainWindow_View

from Models.EnvironmentVariable_Model import EnvironmentVariable_Model
from Models import Utilities_Model

from Controllers.LanguageWindow_Controller import LanguageWindow_Controller
from Controllers.MainWindow_Controller import MainWindow_Controller
from Controllers.ControllerExample3 import ControllerExample3

# ---------------------

class BotMailGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BotMailGUI")
        self.resizable(True, True)

        # Configuration du thème Sun Valley
        sv_ttk.set_theme("dark")
        self.os_name = platform.system()


        # # Conteneur principal pour les pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        # Initialisation des modèles
        environmentVariable_Model = EnvironmentVariable_Model()


        # Initialisation des contrôleurs avec une référence à l'application principale pour initialisation des vues en interne
        self.controllers = {
            "languageWindow_Controller" : LanguageWindow_Controller(container, {"environmentVariable_Model": environmentVariable_Model}),
            "mainWindow_Controller" : MainWindow_Controller(container, {
                "environmentVariable_Model": environmentVariable_Model,
                "Utilities_Model": Utilities_Model
            })
            # "controllerExample3" = ControllerExample3(self.models["PageExample3"], None)
        }

        # Mise en plein écran
        if self.os_name.lower().startswith('win'):
            self.state('zoomed')
        else:
            self.attributes('-zoomed', True)

        # Sélection de la première page d'affichage
        if not environmentVariable_Model.get_variable("LANGUAGE"):
            # Afficher la première page par défaut
            self.show_page("languageWindow_Controller")
        else:
            self.show_page("mainWindow_Controller")


    # Affiche une view associée au controlleur appellé
    def show_page(self, controller):
        self.controllers[controller].show_page()


if __name__ == "__main__":
    app = BotMailGUI()
    app.mainloop()
