# Views/LanguageScreen_View.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.metrics import dp


from Constants import LANGUAGES


class LanguageScreen_View(Screen):
    def __init__(self, controller, name: str, **kwargs):
        super().__init__(name=name, **kwargs)
        self.controller = controller
        
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        self.add_widget(layout)
        self.layout = layout


        # Permet l'affichage d'un message d'erreur
        self.layout.errorLabel = Label(text="", color=(1,0,0,1), size_hint_y=None, height=dp(30))
        self.layout.add_widget(self.layout.errorLabel)

        # Création du menu déroulant (Combobox)
        self.layout.spinner = Spinner(
            text=controller.get_translation("combobox"),
            values=LANGUAGES,
            size_hint=(1, None),
            height=dp(44)
        )
        self.layout.spinner.bind(text=self._dropdown_language_modification)
        self.layout.add_widget(self.layout.spinner)

        self.layout.button = Button(text=controller.get_translation("button"), size_hint=(1, None), height=dp(44))
        self.layout.button.bind(on_press=self._button_language_selection)
        self.layout.add_widget(self.layout.button)



    # Fonction appelée lors de la sélection d'une langue de la combobox
    def _dropdown_language_modification(self, spinner, text):
        self.controller.language_modification(text)



    # Fonction appelé lors de la confirmation de la langue
    def _button_language_selection(self, instance):
        self.controller.language_selection()



    # Permet l'affichage d'un message d'erreur
    def update_error_message(self, message):
        self.layout.errorLabel.text = message



    # Permet la modification du message du button
    def update_button_text(self, text):
        self.layout.button.text = text



    # Permet le changement de screen
    def show_page(self, screen_name):
        self.manager.current = screen_name
