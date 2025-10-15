# Views/MainWindow_View.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import mainthread
from plyer import filechooser


from .KivyCustomComponents import CustomTextInput, CustomButton, SeparatorLine, CustomScrollView, SeparatorBlock, TableauInteractif, choose_files, choose_directory, choose_save, change_widget_text


from Constants import COLORS, CORRECT_SHEET_FILE_EXTENSIONS, CORRECT_DOCUMENT_FILE_EXTENSIONS, STANDARDIZED_HEIGHT, STANDARDIZED_VOID_HEIGHT, STANDARDIZED_VOID_WIDTH


class MainWindow_View(Screen):
    def __init__(self, controller, name: str, **kwargs):
        super().__init__(name=name, **kwargs)

        self.controller = controller
        # Filtres explicites pour le sélecteur fichier natif
        self.filter_sheets = [
            (
                "Excel/Calc files " + ", ".join(CORRECT_SHEET_FILE_EXTENSIONS),
                ";".join(f"*{ext}" for ext in CORRECT_SHEET_FILE_EXTENSIONS)
            )
        ]

        self.filter_documents = [
            (
                "Word/Write files " + ", ".join(CORRECT_DOCUMENT_FILE_EXTENSIONS),
                ";".join(f"*{ext}" for ext in CORRECT_DOCUMENT_FILE_EXTENSIONS)
            )
        ]


        # -------------------
        # UI
        layout = BoxLayout(orientation='vertical', padding=[dp(8), 0, dp(4), 0])
        self.add_widget(layout)
        self.layout = layout


        # Scrollbar + Base
        scroll = CustomScrollView(size_hint=(1, 1))
        layout.add_widget(scroll)
        self.scroll = scroll

        content = GridLayout(
            cols=1, 
            padding=[0, dp(8), dp(16), 0],
            size_hint_y=None, 
            size_hint_x=1
        )
        content.bind(minimum_height=content.setter("height"))
        scroll.add_widget(content)
        self.content = content


        # Boutons pour l'import du fichier CSV et chemin vers le fichier de sauvegarde
        box1 = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(STANDARDIZED_VOID_WIDTH), padding=[dp(25), 0, dp(25), 0])
        box1.add_widget(CustomButton(
            text="Import du tableur (Excel/Calc)", 
            on_press=lambda instance: change_widget_text(self.import_path_display, choose_files(self.filter_sheets, "Veuillez importer un fichier..."))
        ))
        box1.add_widget(CustomButton(
            text="Définition du chemin pour le tableur de résultat", 
            on_press=lambda instance: choose_save(self.filter_sheets)
        ))
        content.add_widget(box1)
        self.box1 = box1

        box2 = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(STANDARDIZED_VOID_WIDTH), padding=[dp(25), 0, dp(25), 0])
        import_path_display = CustomTextInput(
            text="Veuillez importer un fichier...", 
            readonly=True
        )
        result_path_input = CustomTextInput(
            text="Veuillez sélectionner un chemin...", 
            readonly=True
        )
        box2.add_widget(import_path_display)
        box2.add_widget(result_path_input)
        content.add_widget(box2)
        self.import_path_display = import_path_display
        self.result_path_input = result_path_input
        self.box2 = box2


        # Block vide pour séparer
        content.add_widget(SeparatorBlock())


        # Input pour l'Objet des emails
        email_object = CustomTextInput()
        content.add_widget(Label(text="Objet des emails", size_hint_y=None, height=dp(STANDARDIZED_HEIGHT), color=COLORS["white"]))
        content.add_widget(email_object)
        self.email_object = email_object


        # Block vide pour séparer
        content.add_widget(SeparatorBlock())


        # Input pour le Corps des email avec multilignes auto-ajusté
        email_body = CustomTextInput(multiline=True, height=dp(120))
        content.add_widget(Label(text="Corps des emails", size_hint_y=None, height=dp(STANDARDIZED_HEIGHT), color=COLORS["white"]))
        email_body.bind(text=self._adjust_corps_height)
        content.add_widget(email_body)
        content.add_widget(Label(text="Rappel : Ajouter XXN dans l'objet ou le corps de l'email pour personnaliser automatiquement.", size_hint_y=None, height=dp(STANDARDIZED_HEIGHT), color=COLORS["white"]))
        self.email_body = email_body


        # Block vide pour séparer
        content.add_widget(SeparatorBlock())
        # Ligne de séparation
        content.add_widget(SeparatorLine())
        # Block vide pour séparer
        content.add_widget(SeparatorBlock())

        
        # Tableau pour l'imports des documents Word/Writter
        content.add_widget(Label(text="Documents Word/Writer", size_hint_y=None, height=dp(STANDARDIZED_HEIGHT), color=COLORS["white"]))
        self.table_doc = TableauInteractif(
            headers=[
                "Chemin vers le fichier Word/Writer", 
                "Nom du fichier PDF résultant pour l'envoi"
            ],
            pattern=[
                [
                    [
                        CustomTextInput,
                        {
                            "size_hint_x" : 0.75
                        } 
                    ], 
                    [
                        CustomButton,
                        {
                            "text" : "Click me !",
                            "size_hint_x" : 0.25
                        } 
                    ], 
                ],
                [
                    [
                        CustomTextInput,
                        {
                            "size_hint_x" : 0.75
                        } 
                    ], 
                    [
                        CustomButton,
                        {
                            "text" : "Click me !",
                            "size_hint_x" : 0.25
                        } 
                    ], 
                ]
            ]
        )
        # self._patch_table_buttons(self.table_doc, self._on_table_doc_file_selected)
        content.add_widget(self.table_doc)


        # Block vide pour séparer
        content.add_widget(SeparatorBlock())


        # Tableau pour l'imports des documents PDFs supplémentaires
        content.add_widget(Label(text="Documents PDFs supplémentaires", size_hint_y=None, height=dp(STANDARDIZED_HEIGHT), color=COLORS["white"]))
        self.table_pdf = TableauInteractif(
            headers=[
                "Chemin vers le fichier Word/Writer", 
                "Nom du fichier PDF résultant pour l'envoi"
            ],
            pattern=[
                [
                    [
                        CustomTextInput,
                        {
                            "size_hint_x" : 0.75
                        } 
                    ], 
                    [
                        CustomButton,
                        {
                            "text" : "Click me !",
                            "size_hint_x" : 0.25
                        } 
                    ], 
                ],
                [
                    [
                        CustomTextInput,
                        {} 
                    ],
                ]
            ]
        )
        # self._patch_table_buttons(self.table_pdf, self._on_table_pdf_file_selected)
        content.add_widget(self.table_pdf)



    

    

    


    

    



    def _adjust_corps_height(self, instance, value):
        lines = value.count('\n') + 1
        new_height = max(120, min(300, lines * 28))
        self.email_body.height = dp(new_height)


    def _patch_table_buttons(self, table, on_file_selected):
        for cell in table.add_row_widgets:
            if hasattr(cell, 'children'):
                btn = cell.children[0]
                def make_cb(c):
                    return lambda instance: filechooser.open_file(
                        filters=self.filter_sheets,
                        on_selection=lambda paths: self._on_table_file_chosen(c, paths, on_file_selected)
                    )
                btn.unbind(on_press=btn._bound_callback) if hasattr(btn, '_bound_callback') else None
                btn.bind(on_press=make_cb(cell))

    @mainthread
    def _on_table_file_chosen(self, cell_widget, paths, update_fn):
        if paths:
            update_fn(cell_widget, paths[0])
            print(paths[0])

    def _on_table_doc_file_selected(self, cell_widget, path):
        if hasattr(cell_widget, 'textinput'):
            cell_widget.textinput.text = path

    def _on_table_pdf_file_selected(self, cell_widget, path):
        if hasattr(cell_widget, 'textinput'):
            cell_widget.textinput.text = path

    def update_import_path(self, path):
        self.import_path_display.text = path

    def update_result_path(self, path):
        self.result_path_input.text = path

    def get_objet_text(self):
        return self.email_object.text

    def get_email_body(self):
        return self.email_body.text

    def get_table_doc_data(self):
        return self.table_doc.get_all_rows()

    def get_table_pdf_data(self):
        return self.table_pdf.get_all_rows()
