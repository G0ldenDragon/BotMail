import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog

from numpy.distutils.lib2def import parse_nm

from Constants import LANGUAGES

class MainWindow_View(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selectedLanguage = tk.StringVar()
        MODERN_FONT = ("Segoe UI", 12)

        # Permet l'affichage d'un message d'erreur
        self.errorLabel = tk.Label(self, text="", fg="red")
        self.errorLabel.pack()

        # ---

        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.f = ttk.Frame(canvas)
        window = canvas.create_window((0, 0), window=self.f, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.bind("<Configure>", lambda e: canvas.itemconfig(window, width=e.width))
        self.f.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        def wheel(e):
            first, last = canvas.yview()
            if (e.delta > 0 or getattr(e, 'num', 0) == 4) and first <= 0: return
            if (e.delta < 0 or getattr(e, 'num', 0) == 5) and last >= 1: return
            canvas.yview_scroll(-1 if (e.delta > 0 or getattr(e, 'num', 0) == 4) else 1, "units")
        canvas.bind_all("<MouseWheel>", wheel)
        canvas.bind_all("<Button-4>", wheel)
        canvas.bind_all("<Button-5>", wheel)

        style = ttk.Style()
        style.configure("TButton", font=MODERN_FONT)
        style.configure("TLabel", font=MODERN_FONT)
        style.configure("TEntry", font=MODERN_FONT)
        style.configure("Add.TButton", foreground="green", background="#27ae60", font=MODERN_FONT)
        style.map("Add.TButton", background=[('active', '#c0392b')])
        style.configure("Del.TButton", foreground="#e74c3c", background="#23272e")
        style.map("Del.TButton", foreground=[('active', '#c0392b')])

        for i in range(3): self.f.columnconfigure(i, weight=1)
        PADX = 20

        ttk.Button(self.f, text="Import du tableur (Excel/Calc)", style="Accent.TButton", command=self.button_file_sheet_selector).grid(row=0, column=0, sticky="ew", padx=(PADX, 5), pady=10)
        self.path_file_sheet_selector = tk.StringVar()
        ttk.Button(self.f, text="Définition du chemin pour le tableur de résultat", style="Accent.TButton").grid(row=0, column=2, sticky="ew", padx=(5, PADX), pady=10)
        import_entry = ttk.Entry(self.f, font=MODERN_FONT, state="readonly")
        import_entry.insert(0, "Veuillez importer un fichier...")
        import_entry.grid(row=1, column=0, sticky="ew", padx=(PADX, 5), pady=(0, 10))
        path_entry = ttk.Entry(self.f, font=MODERN_FONT, state="readonly")
        path_entry.insert(0, "Veuillez sélectionner un chemin...")
        path_entry.grid(row=1, column=2, sticky="ew", padx=(5, PADX), pady=(0, 10))

        self.f.rowconfigure(2, minsize=15)
        ttk.Label(self.f, text="Objet des emails", anchor="center").grid(row=3, column=0, columnspan=3, sticky="ew", padx=PADX, pady=5)
        entry = ttk.Entry(self.f, font=MODERN_FONT)
        entry.grid(row=4, column=0, columnspan=3, sticky="ew", padx=PADX, pady=5)
        self.f.rowconfigure(5, minsize=15)
        ttk.Label(self.f, text="Corps des emails", anchor="center").grid(row=6, column=0, columnspan=3, sticky="ew", padx=PADX, pady=5)
        text2 = tk.Text(self.f, height=5, wrap="word", relief="groove", borderwidth=0, highlightthickness=2,
                        highlightbackground="#444", highlightcolor="#0078D7", font=MODERN_FONT, fg="#fafafa", padx=10, pady=8)
        text2.grid(row=7, column=0, columnspan=3, sticky="ew", padx=PADX, pady=5)
        self.f.rowconfigure(7, weight=1)
        ttk.Label(self.f, text="Rappel : Ajouter XXN dans l'objet ou le corps de l'email pour personnaliser automatiquement.", anchor="center").grid(row=8, column=0, columnspan=3, sticky="ew", padx=PADX, pady=5)
        def adjust_height(event=None):
            lines = int(text2.index('end-1c').split('.')[0])
            text2.configure(height=max(5, lines))
        text2.bind("<KeyRelease>", adjust_height)

        # Tableaux
        # self.f.rowconfigure(10, minsize=20)
        # ttk.Separator(self.f, orient="horizontal").grid(row=11, column=0, columnspan=3, sticky="ew", pady=(10, 10))
        # ttk.Label(self.f, text="Documents Word/Writer", anchor="center", font=(MODERN_FONT[0], 13, "bold")).grid(row=12, column=0, columnspan=3, sticky="ew", padx=PADX, pady=(0, 10))
        # doc = TableauInteractif(self.f, ["Chemin vers les documents", "Nom du document PDF résultant", ""])
        # doc.grid(row=13, column=0, columnspan=3, sticky="ew", padx=PADX, pady=5)
        #
        # self.f.rowconfigure(14, minsize=20)
        # ttk.Separator(self.f, orient="horizontal").grid(row=15, column=0, columnspan=3, sticky="ew", pady=(10, 10))
        # ttk.Label(self.f, text="Documents PDFs supplémentaires", anchor="center", font=(MODERN_FONT[0], 13, "bold")).grid(row=16, column=0, columnspan=3, sticky="ew", padx=PADX, pady=(0, 10))
        # pdf = TableauInteractif(self.f, ["Chemin vers les documents", "Nom du document PDF à envoyé", ""])
        # pdf.grid(row=17, column=0, columnspan=3, sticky="ew", padx=PADX, pady=5)


        # ---


    # Fonction appelée lors de la modification dans la combobox
    def dropdown_language_modification(self, event=None):
        self.controller.language_modification(self.selectedLanguage.get())


    # Gestion du bouton de séléction du tableur
    def button_file_sheet_selector(self):
        path = filedialog.askopenfilename(
            title="Sélectionnez un fichier",
            initialdir=str(Path.home()),
            filetypes=self.controller.get_available_file_sheet_extensions()
        )

        if path:
            self.controller.file_sheet_selector(path)


    # Permet l'affichage d'un message d'erreur
    def update_error_message(self, message):
        self.errorLabel.config(text=message)


    # Permet la modification du message du button
    def update_button_message(self, message):
        self.button.config(text=message)