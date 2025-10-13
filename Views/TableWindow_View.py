# Views/TableWindow_View.py

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.metrics import dp


from .CustomComponents import CustomButton


from Constants import COLORS, CORRECT_SHEET_FILE_EXTENSIONS, STANDARDIZED_HEIGHT, STANDARDIZED_VOID_HEIGHT, STANDARDIZED_VOID_WIDTH


# Tableau interactif reprenant ta classe Kivy
class TableauInteractif(GridLayout):
    def __init__(self, headers: list[str], pattern: list[list], **kwargs):
        super().__init__(cols=len(headers) + 1, size_hint_y=None, **kwargs)

        if len(headers) != len(pattern):
            raise ValueError("Le nombre d'entêtes ne correspond pas au nombre de colonnes à créés.")
    

        self.row_height = dp(STANDARDIZED_HEIGHT)
        self.bind(minimum_height=self.setter('height'))
        self.rows_widgets = []


        # En-têtes
        for h in headers:
            self.add_widget(Label(text=h, size_hint_y=None, height=self.row_height, color=COLORS["white"]))
        self.add_widget(Label(text="Actions", size_hint_y=None, height=self.row_height, color=COLORS["white"]))


        # Vérification du patterne
        for cells in pattern:
            for widget in cells:
                if len(widget) != 2:
                    raise ValueError("Rows doit avoir le format suivant [[[Classe, Dict], [Classe, Dict]]]")
                    
                if not callable(widget[0]):
                    raise ValueError("Le premier élément doit être une Classe.")
            
                if type(widget[1]) != dict:
                    raise ValueError("Le second élément doit être un Dictionnaire.")
            
        self.pattern = pattern


        # Ligne ajout avec cellule éditable + bouton loupe à droite
        self.add_row_widgets = []
        for cells in pattern:
            cell = self._new_cell(cells)
            self.add_widget(cell)
            self.add_row_widgets.append(cell)
        
        add_cell = BoxLayout(orientation="horizontal", size_hint_y=None, height=self.row_height)
        btn_add = CustomButton(
            text="+", 
            normal_bg_color=(0.1, 0.7, 0.3, 1), 
            color=COLORS["white"],
            on_press=self._on_add_row,
            size_hint_x=0.01
        )
        add_cell.add_widget(btn_add)
        self.add_widget(add_cell)



    # Création d'un ligne à partir du patterne
    def _new_cell(self, widgets: list):
        cell = BoxLayout(orientation="horizontal", size_hint_y=None, size_hint_x=(0.99 / len(self.pattern) + 1), height=self.row_height)

        for widget in widgets:
            classe, parameters = widget
            instance = classe(**parameters)

            cell.add_widget(instance)

        return cell



    # Obtention des valeurs dans les TextInput et suppression de celles-ci
    def _on_add_row(self, instance):
        values = []
        for cell in self.add_row_widgets:
            for widget in cell.children:
                if isinstance(widget, TextInput):
                    values.append(widget.text.strip())
                    widget.text = ""

        self.add_row(values)



    # Utilisation des valeurs obtenues pour l'ajout d'une nouvelle ligne
    def add_row(self, values):
        self.rows_widgets.append([])

        for i, cells in enumerate(self.pattern):
            for widgets in cells:
                if issubclass(widgets[0], TextInput):
                    widgets[1].update({"text" : values[i]})

                    cell = self._new_cell(cells)
                    self.add_widget(cell)
                    self.rows_widgets[-1].append(cell)


        del_cell = BoxLayout(orientation="horizontal", size_hint_y=None, height=self.row_height)
        btn_del = CustomButton(
            text="-", 
            normal_bg_color=(0.8, 0.2, 0.2, 1), 
            color=COLORS["white"], 
            on_press=self._on_del_row,
            size_hint_x=0.01
        )
        del_cell.add_widget(btn_del)
        self.add_widget(del_cell)
        self.rows_widgets[-1].append(del_cell)



    # Recherche de l'instance du boutton dans les widgets enfant des BoxLayout pour la suppression de la liste
    def _on_del_row(self, instance):
        for index, cells in enumerate(self.rows_widgets):
            for cell in cells:
                if instance in cell.children:
                    self.delete_row(index)
                    return



    def delete_row(self, index):
        if 0 <= index < len(self.rows_widgets):
            for widget in self.rows_widgets[index]:
                self.remove_widget(widget)
            del self.rows_widgets[index]



    # def on_click(self, instance):



    # def _make_editable_cell(self, text):
    #     ti = CustomTextInput(text=text, multiline=False, height=self.row_height)
    #     return ti



    # def get_all_rows(self):
    #     # Retourne des listes des valeurs actuelles visibles dans la table (sauf boutons)
    #     result = []
    #     for row_widgets in self.rows_widgets:
    #         row_values = []
    #         for w in row_widgets:
    #             # Si c'est un CustomTextInput ou BoxLayout avec textinput, récupérer le texte
    #             if hasattr(w, 'textinput'):
    #                 row_values.append(w.textinput.text)
    #             elif isinstance(w, CustomTextInput):
    #                 row_values.append(w.text)
    #         if row_values:
    #             result.append(row_values)
    #     return result
