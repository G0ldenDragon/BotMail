# Views/KivyCustomComponents.py

from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp, sp
from kivy.properties import BooleanProperty

from plyer import filechooser


from Models.Language import Language


from Constants import COLORS, STANDARDIZED_HEIGHT, STANDARDIZED_VOID_HEIGHT
SCRIPT_NAME = "kivy_custom_components"


# TextInput custom
class CustomTextInput(TextInput):
    def __init__(self, 
                 height=dp(STANDARDIZED_HEIGHT), 
                 font_size=sp(15),
                 textcolor=COLORS["white"],
                 multiline=False, 
                 readonly=False, 
                 **kwargs
                ):

        super().__init__(multiline=multiline, readonly=readonly, **kwargs)
        self.size_hint_y = None
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (0.17, 0.17, 0.17, 1)
        self.padding = dp(10)
        self.cursor_color = (0.3, 0.7, 1, 1)
        self.cursor_width = dp(1.5)

        self.font_size = font_size
        self.height = height
        self.foreground_color = textcolor



# Base Button stylé
class CustomButton(Button):
    hovered = BooleanProperty(False)

    def __init__(self, 
                 text="", 
                 normal_bg_color=COLORS["lightBlue"], 
                 hovered_bg_color=COLORS["red"], 
                 color=COLORS["white"], 
                 height=dp(STANDARDIZED_HEIGHT), 
                 font_size=sp(15), 
                 **kwargs
                ):
        
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.background_normal = ""
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.bind(hovered=self.on_hover)
        
        self.text = text
        self.background_color = normal_bg_color
        self.normal_bg_color = normal_bg_color
        self.hovered_bg_color = hovered_bg_color
        self.color = color
        self.height = height
        self.font_size = font_size

    def on_mouse_pos(self, window, pos):
        inside = self.collide_point(*self.to_widget(*pos))
        self.hovered = inside

    def on_hover(self, instance, value):
        if value:
            self.background_color = self.hovered_bg_color  # Couleur au survol
        else:
            self.background_color = self.normal_bg_color  # Couleur par défaut



# Ligne séparatrice horizontale
class SeparatorLine(Widget):
    def __init__(self, 
                 height=dp(2), 
                 color=COLORS["grey"], 
                 **kwargs
                ):
        
        super().__init__(size_hint_y=None, height=height, **kwargs)
        with self.canvas:
            Color(*color)
            self.line = Rectangle(pos=self.pos, size=(self.width, height))
        self.bind(pos=self._update_line, size=self._update_line)

    def _update_line(self, *args):
        self.line.pos = self.pos
        self.line.size = (self.width, self.height)



# Block vide pour séparer les parties
class SeparatorBlock(BoxLayout):
    def __init__(self, 
                 height=dp(STANDARDIZED_VOID_HEIGHT),
                 **kwargs
                ):
        
        super().__init__(size_hint_y=None, height=height, **kwargs)



# ScrollView custom avec scrollbar fine et hover
class CustomScrollView(ScrollView):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.bar_width = dp(12)
        self.scroll_type = ['bars']
        self.bar_color = (0.5, 0.5, 0.5, 0.8)
        self.bar_inactive_color = (0.5, 0.5, 0.5, 0.5)



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
        cell = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            size_hint_x=(0.99 / len(self.pattern) + 1),
            height=self.row_height
        )

        created_widgets = {}

        for classe, parameters in widgets:
            on_press_func_str = parameters.get("on_press_func")
            text_input = created_widgets.get("text_input")

            # Supprime on_press_func et instances des paramètres passés à la classe
            params_copy = parameters.copy()
            params_copy.pop("on_press_func", None)
            instances_dict = params_copy.pop("instances", {})

            instance = classe(**params_copy)

            if on_press_func_str and text_input:
                on_press_func_str = on_press_func_str.replace("TEXTINPUT", "text_input")
                eval_context = instances_dict.copy()
                eval_context["text_input"] = text_input

                print(eval_context)

                # évaluer la lambda dans un espace sécurisé avec les bonnes références
                func = eval(on_press_func_str, {}, eval_context)
                instance.bind(on_press=func)

            if issubclass(classe, TextInput):
                created_widgets["text_input"] = instance

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

# --------------------------------------------------

# Modifications des widgets
def change_widget_text(widget, text: str) -> None: 
    widget.text = text
    widget.cursor = (len(text), 0)
    widget.scroll_x = 0



# FileChooser
def choose_files(filter: list, title: str = Language().get_translation(SCRIPT_NAME, "choose_files"), defaultReturn = "", multiple: bool= False) -> str:
        result = {'files': defaultReturn}  # container mutable (pour palier à l'asynchronéité)

        def on_select(paths):
            if paths:
                result['files'] = "; ".join(paths)
        
        def on_cancel():
            result['files'] = defaultReturn

        filechooser.open_file(
            title=title,
            filters=filter,
            multiple=multiple,
            on_selection=on_select,
            on_cancel=on_cancel
        )

        return result['files']



def choose_directory(title: str = Language().get_translation(SCRIPT_NAME, "choose_directory"), defaultReturn = "") -> str:
    result = {'directory': defaultReturn}  # container mutable (pour palier à l'asynchronéité)

    def on_select(paths):
        if paths:
            result['directory'] = paths[0]

    def on_cancel():
        result['directory'] = defaultReturn

    filechooser.choose_dir(
        title=title, 
        on_selection=on_select,
        on_cancel=on_cancel
    )

    return result['directory']

    

def choose_save(filter: list, title: str = Language().get_translation(SCRIPT_NAME, "choose_save"), defaultReturn = "") -> str:
    result = {'save': defaultReturn}  # container mutable (pour palier à l'asynchronéité)

    def on_select(paths):
        if paths:
            result['save'] = paths[0]

    def on_cancel():
        result['save'] = defaultReturn

    filechooser.save_file(
        title=title, 
        filters=filter,
        on_selection=on_select,
        on_cancel=on_cancel
    )

    return result['save']
