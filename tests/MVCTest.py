import tkinter as tk

# Modèles
class Model1:
    def __init__(self):
        self.data = "Données du modèle 1"

class Model2:
    def __init__(self):
        self.data = "Données du modèle 2"

class Model3:
    def __init__(self):
        self.data = "Données du modèle 3"

# Vues
class Page1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Page 1 : " + str(self.controller.models[Page1].data))
        label.pack(pady=10)
        button = tk.Button(self, text="Aller à la Page 2", command=lambda: self.controller.show_page(Page2))
        button.pack()

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Page 2")
        label.pack(pady=10)
        button = tk.Button(self, text="Aller à la Page 3", command=lambda: self.controller.show_page(Page3))
        button.pack()

class Page3(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Page 3")
        label.pack(pady=10)
        button = tk.Button(self, text="Retour à la Page 1", command=lambda: self.controller.show_page(Page1))
        button.pack()

# Contrôleurs
class Controller1:
    def __init__(self, model, view):
        self.model = model
        self.view = view

class Controller2:
    def __init__(self, model, view):
        self.model = model
        self.view = view

class Controller3:
    def __init__(self, model, view):
        self.model = model
        self.view = view

# Application principale
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application MVC à trois pages")
        self.geometry("400x300")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.models = {
            Page1: Model1(),
            Page2: Model2(),
            Page3: Model3()
        }
        self.controllers = {
            Page1: Controller1,
            Page2: Controller2,
            Page3: Controller3
        }

        for F in (Page1, Page2, Page3):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            controller = self.controllers[F](self.models[F], frame)

        self.show_page(Page1)

    def show_page(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
