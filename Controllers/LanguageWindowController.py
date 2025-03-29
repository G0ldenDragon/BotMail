class LanguageWindowController:
    def __init__(self, model, view, app):
        self.model = model  # Associe le modèle au contrôleur
        self.view = view    # Associe la vue au contrôleur (peut être utilisé plus tard)
        self.app = app      # Référence à l'application principale (BotMailGUI)

    def languageSetter(self, language):
        """Traite ou affiche la langue sélectionnée (provisoire)"""
        print(f"Langue sélectionnée : {language}")

        # Redirige vers PageExample2 après avoir traité la langue
        self.app.show_page("PageExample2")
