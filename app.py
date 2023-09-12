import json
import customtkinter
from customtkinter import CTk, CTkEntry, CTkButton, CTkLabel, CTkFrame

customtkinter.set_default_color_theme("green")
customtkinter.set_widget_scaling(2)

with open("questions.json", "r") as questions:
    data = json.load(questions)


class InsertUsername(CTkFrame):
    def __init__(self, master: CTk, callback):
        super().__init__(master)

        self.username_label = CTkLabel(
            master=self,
            text="Nombre de usuario"
        )

        self.username_entry = CTkEntry(
            master=self,
            # textvariable=self.username
        )

        self.username_btn = CTkButton(
            master=self,
            text="Ok",
            command=callback
        )

        self.username_label.grid(row=0, column=0, padx=20, pady=10)
        self.username_entry.grid(row=1, column=0, padx=20, pady=10)
        self.username_btn.grid(row=2, column=0, padx=20, pady=10)

        self.username_entry.focus()
        self.username_entry.bind(sequence="<Return>", command=callback)


class SelectThematic(CTkFrame):
    def __init__(self, master: CTk, callback):
        super().__init__(master)

        self.callback = callback
        self.thematic = customtkinter.StringVar()

        self.select_lbl = CTkLabel(
            master=self,
            text="Selecciona la temática",
            text_color="black",
            fg_color="white",
            corner_radius=5

        )

        self.thematics = []
        for thematic in data:
            thematic_lbl = CTkButton(
                master=self,
                text=thematic.get("header"),
                command=lambda: self.set_thematic(thematic.get("header"))
            )
            self.thematics.append(thematic_lbl)

        self.select_lbl.grid(row=0, column=0, padx=10, pady=10)
        for i in range(len(self.thematics)):
            self.thematics[i].grid(row=i + 1, column=0, padx=20, pady=10)

    def set_thematic(self, thematic: str):
        self.thematic.set(value=thematic)
        self.callback()


class Questions(CTkFrame):
    def __init__(self):
        super().__init__()


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Juego de preguntas")

        self.username = customtkinter.StringVar(value="username")
        self.thematic = customtkinter.Variable()

        self.iu_frm = InsertUsername(
            master=self,
            callback=self.on_close_insert_usename
        )

        self.st_frm = SelectThematic(
            master=self,
            callback=self.on_close_select_thematic
        )

        self.grid_columnconfigure((0, 1), weight=1)
        self.iu_frm.grid(row=0, column=0, padx=20, ipady=20)

    def on_close_insert_usename(self, event=None):
        self.username.set(self.iu_frm.username_entry.get())
        self.iu_frm.grid_remove()
        self.iu_frm.destroy()

        self.st_frm.grid(row=0, column=0, padx=20, ipady=20)

    def on_close_select_thematic(self):
        self.thematic.set(self.st_frm.thematic.get())
        self.st_frm.grid_remove()
        self.st_frm.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
