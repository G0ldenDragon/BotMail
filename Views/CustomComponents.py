# Views/CustomComponents.py

from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp, sp
from kivy.clock import mainthread
from kivy.properties import BooleanProperty

from plyer import filechooser

from Constants import COLORS, STANDARDIZED_HEIGHT, STANDARDIZED_VOID_HEIGHT


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


# Modifications des widgets

def change_widget_text(widget, text: str) -> None: 
    widget.text = text
    widget.cursor = (0, 0)
    widget.scroll_x = 0



# FileChooser

def choose_files(filter: list, defaultReturn = "", multiple: bool= False) -> str:
        result = {'files': defaultReturn}  # container mutable (pour palier à l'asynchronéité)

        def on_select(paths):
            if paths:
                result['files'] = "; ".join(paths)
        
        def on_cancel():
            result['files'] = defaultReturn

        filechooser.open_file(
            title="Choisir le(s) fichier(s)...",
            filters=filter,
            multiple=multiple,
            on_selection=on_select,
            on_cancel=on_cancel
        )

        return result['files']



def choose_directory(defaultReturn="") -> str:
    result = {'directory': defaultReturn}  # container mutable (pour palier à l'asynchronéité)

    def on_select(paths):
        if paths:
            result['directory'] = paths[0]

    def on_cancel():
        result['directory'] = defaultReturn

    filechooser.choose_dir(
        title="Choisir le dossier...", 
        on_selection=on_select,
        on_cancel=on_cancel
    )

    return result['directory']

    

def choose_save(filter: list) -> str:
    save = filechooser.save_file(
        title="Enregistrer sous...", 
        filters=filter
    )

    print(save)
