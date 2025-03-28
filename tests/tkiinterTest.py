import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import sv_ttk
import platform

class FileSelectorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sélecteur de Fichier")
        self.geometry("700x500")
        self.resizable(True, True)

        self.os_name = platform.system()

        sv_ttk.set_theme("dark")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=(20, 20))
        main_frame.pack(expand=True, fill="both")

        title_label = ttk.Label(
            main_frame,
            text="Sélecteur de Fichier/Dossier",
            font=("Segoe UI", 18, "bold"),
            anchor="center"
        )
        title_label.pack(pady=(0, 20))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(10, 20))

        file_button = ttk.Button(
            button_frame,
            text="Sélectionner un fichier",
            command=self.select_file,
            style="Accent.TButton"
        )
        file_button.pack(side="left", padx=10)

        folder_button = ttk.Button(
            button_frame,
            text="Sélectionner un dossier",
            command=self.select_folder
        )
        folder_button.pack(side="left", padx=10)

        self.path_var = tk.StringVar()
        path_label = ttk.Label(main_frame, text="Chemin sélectionné :", font=("Segoe UI", 12))
        path_label.pack(anchor="w")

        self.path_entry = ttk.Entry(main_frame, textvariable=self.path_var, font=("Segoe UI", 12))
        self.path_entry.pack(fill="x", pady=5)
        self.path_entry.bind('<Key>', self.clear_entry)  # Ajout de l'événement de suppression rapide

        self.text_area = tk.Text(
            main_frame,
            wrap="word",
            height=15,
            bg="#1e1e1e",
            fg="#ffffff",
            font=("Consolas", 11),
            relief="flat"
        )
        self.text_area.pack(expand=True, fill="both", pady=(10, 0))

    def clear_entry(self, event):
        if event.state == 4 and event.keysym == 'Delete':  # 4 correspond à Ctrl
            self.path_entry.delete(0, tk.END)

    def select_file(self):
        filetypes = [
            ("Fichiers texte", "*.txt"),
            ("Fichiers CSV", "*.csv"),
            ("Tous les fichiers", "*.*")
        ]

        path = filedialog.askopenfilename(
            title="Sélectionnez un fichier",
            initialdir=str(Path.home()),
            filetypes=filetypes
        )

        if path:
            self.path_var.set(path)
            self.display_content(path)

    def select_folder(self):
        path = filedialog.askdirectory(
            title="Sélectionnez un dossier",
            initialdir=str(Path.home())
        )

        if path:
            self.path_var.set(path)
            self.display_content(path)

    def display_content(self, path):
        self.text_area.delete("1.0", "end")

        try:
            if Path(path).is_file():
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.insert("1.0", content)
            elif Path(path).is_dir():
                folder_content = "\n".join([str(p) for p in Path(path).iterdir()])
                self.text_area.insert("1.0", f"Contenu du dossier :\n{folder_content}")
            else:
                self.text_area.insert("1.0", "Le chemin sélectionné est invalide.")

        except Exception as e:
            self.text_area.insert("1.0", f"Erreur lors de la lecture : {str(e)}")

if __name__ == "__main__":
    app = FileSelectorApp()
    app.mainloop()
