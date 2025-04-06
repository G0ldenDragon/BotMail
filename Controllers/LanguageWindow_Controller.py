from Views.LanguageWindow_VIew import LanguageWindow_View

class LanguageWindow_Controller:
    def __init__(self, container, model):
        self.container = container      # Référence au container principale (BotMailGUI)
        self.model = model  # Associe le modèle au contrôleur
        self.view = LanguageWindow_View(container, self)    # Associe la vue au contrôleur (peut être utilisé plus tard)

        # Add the view to its parent using a layout manager
        self.view.grid(row=0, column=0, sticky="nsew")  # Use grid for consistent layout

    def languageSetter(self, language):
        """Traite ou affiche la langue sélectionnée (provisoire)"""
        print(f"Langue sélectionnée : {language}")

        # Redirige vers PageExample2 après avoir traité la langue
        self.container.show_page("PageExample2")

    def showPage(self):
        self.view.tkraise()
