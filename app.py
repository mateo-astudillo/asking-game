import json
import customtkinter
from customtkinter import (
    CTk, CTkEntry, CTkButton, CTkLabel, CTkFrame, CTkFont
)

customtkinter.set_default_color_theme("green")
customtkinter.set_widget_scaling(2)

with open("questions.json", "r") as questions:
    data = json.load(questions)


class InsertUsername(CTkFrame):
    def __init__(self, master: CTk):
        super().__init__(master)

        self.master = master

        self.username_label = CTkLabel(
            master=self,
            text="Nombre de usuario"
        )

        self.username_entry = CTkEntry(
            master=self,
        )

        self.username_btn = CTkButton(
            master=self,
            text="Ok",
            command=self.close
        )

        self.username_label.grid(row=0, column=0, padx=20, pady=10)
        self.username_entry.grid(row=1, column=0, padx=20, pady=10)
        self.username_btn.grid(row=2, column=0, padx=20, pady=10)

        self.username_entry.focus()
        self.username_entry.bind(sequence="<Return>", command=self.close)

    def close(self, event=None):
        self.master.username = self.username_entry.get().replace(" ", "")
        self.master.st_frm.pack()
        self.pack_forget()
        self.destroy()


class SelectThematic(CTkFrame):
    def __init__(self, master: CTk):
        super().__init__(master)
        self.master = master

        self.select_lbl = CTkLabel(
            master=self,
            text="Selecciona la temática",
        )

        self.thematics = []
        for key in data.keys():
            thematic_lbl = CTkButton(
                master=self,
                text=data.get(key).get("header"),
                command=lambda k=key: self.set_thematic(k)
            )
            thematic_lbl.pack(padx=20, pady=10)
            self.thematics.append(thematic_lbl)

    def set_thematic(self, key: str):
        self.pack_forget()
        self.master.set_thematic_key(key)
        self.master.init_questions()
        self.destroy()


class Question(CTkFrame):
    def __init__(self, master, question: str, options: list, next):
        super().__init__(master)

        self.question = CTkLabel(
            master=self,
            text=question
        )

        self.question.pack()
        for option in options:
            to = option.get("to")
            weight = option.get("weight")
            value_lbl = CTkButton(
                master=self,
                text=option.get("value"),
                command=lambda t=to, w=weight: next(t, w)
            )
            value_lbl.pack(padx=20, pady=10, fill="x")


class Questions(CTkFrame):
    def __init__(self, master: CTk, thematic_key: str):
        super().__init__(master)
        self.master = master

        self.nq = 0

        self.thematic_lbl = CTkLabel(
            master=self,
            text=data.get(thematic_key).get("header")
        )

        self.thematic_lbl.pack(padx=10, pady=10)

        self.questions = []
        questions = data.get(thematic_key).get("questions")
        for question in questions:
            q = Question(
                master=self,
                question=question.get("question"),
                options=question.get("options"),
                next=self.next
            )
            self.questions.append(q)

        self.questions[self.nq].pack(padx=20, pady=10, fill="x")

    def next(self, to: str, weight: int):
        self.master.add_to_the_result(to, weight)
        self.questions[self.nq].pack_forget()
        self.questions[self.nq].destroy()
        self.nq += 1
        if self.nq == len(self.questions):
            self.master.show_results()
            self.pack_forget()
            self.destroy()
            return
        self.questions[self.nq].pack(padx=20, pady=10, fill="x")


class Result(CTkFrame):
    def __init__(self, master: CTk, results: dict, user: str):
        super().__init__(master)

        result = ""
        max_score = 0
        print(results)
        for key in results.keys():
            s = results.get(key).get("score")
            if int(s) >= max_score:
                max_score = int(s)
                result = results.get(key).get("name")

        self.result_lbl = CTkLabel(
            master=self,
            text=f"{user}: {result.capitalize()}",
            # font=CTkFont(family="Courier", size=32, weight="bold")
        )

        self.pack()
        self.result_lbl.pack(fill="both", padx=20, pady=20)


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Juego de preguntas")
        self.minsize(width=800, height=800)

        self.username = ""
        self.thematic_key = ""
        self.results = {}

        self.iu_frm = InsertUsername(master=self)
        self.st_frm = SelectThematic(master=self)

        self.iu_frm.pack(padx=20, pady=20)

    def set_username(self, username: str):
        self.username = username

    def set_thematic_key(self, thematic_key: str):
        self.thematic_key = thematic_key

    def init_questions(self):
        results = data.get(self.thematic_key).get("results")
        for r in results.keys():
            self.results[r] = {
                "name": results.get(r),
                "score": 0
            }

        self.qq_frm = Questions(
            master=self,
            thematic_key=self.thematic_key
        )
        self.qq_frm.pack()

    def add_to_the_result(self, to: str, weight: int):
        self.results.get(to)["score"] += weight

    def show_results(self):
        self.result = Result(
            master=self,
            results=self.results,
            user=self.username
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
