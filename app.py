from customtkinter import CTk
import json

with open("questions.json", "r") as questions:
    data = json.load(questions)


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Juego de preguntas")


if __name__ == "__main__":
    app = App()
    app.mainloop()
