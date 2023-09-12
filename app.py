import json
import customtkinter
from customtkinter import CTk, CTkEntry, CTkButton, CTkLabel, CTkFrame

with open("questions.json", "r") as questions:
    data = json.load(questions)


class InsertUsername(CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master)

        self.username_label = CTkLabel(
            master=self,
            text="Username"
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


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Juego de preguntas")

        self.username = customtkinter.StringVar(value="username")

        self.st = InsertUsername(
            master=self,
            callback=self.on_close_select_thematic
        )

        self.st.grid(row=0, column=0)

    def on_close_insert_usename(self, event):
        self.username.set(self.st.username_entry.get())
        self.st.grid_remove()
        self.st.destroy()


if __name__ == "__main__":
    app = App()
    app.grid_columnconfigure((0, 1), weight=1)
    app.mainloop()
