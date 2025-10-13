# BotMailGUI.py

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import NoTransition, SlideTransition


from Models.Language_Model import Language
from Models.EnvironmentVariable_Model import *

from Controllers.LanguageWindow_Controller import LanguageWindow_Controller
from Controllers.MainWindow_Controller import MainWindow_Controller


from Constants import LANGUAGES


class BotMailGUI(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controllers = {}

    def build(self):
        # Configuration fenêtre
        Window.minimum_width = 800
        Window.minimum_height = 600

        self.language_Model = Language()

        # Initialisation contrôleurs avec construction des vues.
        self.languageScreenController = LanguageWindow_Controller(
            {
                "language_Model": self.language_Model,
            }, 
            screen_name = "language_selection"
        )
        self.mainScreenController = MainWindow_Controller(
            {
                "language_Model": self.language_Model,
            },
            screen_name = "main"
        )


        sm = ScreenManager()
        sm.add_widget(self.languageScreenController.view)
        sm.add_widget(self.mainScreenController.view)


        sm.transition = NoTransition()
        if not get_variable("LANGUAGE") in LANGUAGES :
            # Afficher la première page par défaut
            sm.current = "language_selection"  
        else:
            sm.current = "main"
        sm.transition = SlideTransition()


        # # Mise en plein écran
        # if self.os_name.lower().startswith('win'):
        #     self.state('zoomed')
        # else:
        #     self.attributes('-zoomed', True)

        return sm
    

    # def on_start(self):
    #     if not self.environmentVariable_Model.get_variable("LANGUAGE") in LANGUAGES :
    #         # Afficher la première page par défaut
    #         self.root.current = "language"
    #     else:
    #         self.root.current = "main"
        

if __name__ == "__main__":
    BotMailGUI().run()
