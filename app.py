import os

import pandas as pd
from sklearn import linear_model
import tkinter as tk
import tkinter.font as font
from tkinter import filedialog

try:
    from pyresparser import ResumeParser
except ImportError:
    ResumeParser = None


class TrainModel:
    def train(self):
        csv_path = os.path.join(os.path.dirname(__file__), "training_dataset.csv")

        if os.path.exists(csv_path):
            data = pd.read_csv(csv_path)
        else:
            data = pd.DataFrame(
                [
                    [1, 22, 8, 3, 7, 8, 6, "Extrovert"],
                    [0, 28, 4, 7, 6, 5, 3, "Introvert"],
                    [1, 30, 7, 4, 8, 7, 8, "Extrovert"],
                    [0, 24, 5, 6, 7, 6, 4, "Balanced"],
                    [1, 27, 6, 5, 8, 7, 5, "Balanced"],
                    [0, 35, 3, 8, 5, 4, 2, "Introvert"],
                    [1, 26, 9, 4, 7, 8, 7, "Extrovert"],
                    [0, 31, 4, 7, 6, 5, 3, "Introvert"],
                ],
                columns=[
                    "gender",
                    "age",
                    "openness",
                    "neuroticism",
                    "conscientiousness",
                    "agreeableness",
                    "extraversion",
                    "personality",
                ],
            )

        feature_columns = [
            "gender",
            "age",
            "openness",
            "neuroticism",
            "conscientiousness",
            "agreeableness",
            "extraversion",
        ]
        X = data[feature_columns]
        y = data["personality"]

        self.mul_lr = linear_model.LogisticRegression(
            multi_class="multinomial",
            solver="newton-cg",
            max_iter=1000,
        )
        self.mul_lr.fit(X, y)

    def test(self, test_data):
        try:
            test_predict = [float(value) for value in test_data]
            y_pred = self.mul_lr.predict([test_predict])
            return y_pred[0]
        except Exception:
            print("All factors for finding personality not entered!")
            return None


def check_type(data):
    if isinstance(data, (str, int, float)):
        return str(data).title()
    if isinstance(data, (list, tuple)):
        return ", ".join(str(item) for item in data)
    return str(data)


model = TrainModel()
model.train()


def prediction_result(top, applicant_name, cv_path, personality_values):
    top.withdraw()

    applicant_data = {
        "Candidate Name": applicant_name,
        "CV Location": cv_path,
    }

    print("\n#############CandidateEnteredData#############\n")
    print(applicant_data, personality_values)

    personality = model.test(personality_values)
    print("\n#############PredictedPersonality#############\n")
    print(personality)

    if ResumeParser is None:
        resume_data = {}
    else:
        resume_data = ResumeParser(cv_path).get_extracted_data() if cv_path else {}

    try:
        if isinstance(resume_data, dict):
            resume_data.pop("name", None)
            mobile = resume_data.get("mobile_number")
            if mobile is not None and len(str(mobile)) < 10:
                resume_data.pop("mobile_number", None)
    except Exception:
        pass

    result = tk.Tk()
    result.geometry("{0}x{1}+0+0".format(result.winfo_screenwidth(), result.winfo_screenheight()))
    result.configure(background="White")
    result.title("Predicted Personality")

    title_font = font.Font(family="Arial", size=40, weight="bold")
    tk.Label(
        result,
        text="Result Personality Prediction",
        foreground="green",
        bg="white",
        font=title_font,
        pady=10,
        anchor=tk.CENTER,
    ).pack(fill=tk.BOTH)

    tk.Label(
        result,
        text=str("Name: {}".format(applicant_name)).title(),
        foreground="black",
        bg="white",
        anchor="w",
    ).pack(fill=tk.BOTH)

    for key in resume_data.keys():
        value = resume_data[key]
        if value is not None:
            tk.Label(
                result,
                text=str("{}: {}".format(check_type(key.title()), check_type(value))),
                foreground="black",
                bg="white",
                anchor="w",
                width=60,
            ).pack(fill=tk.BOTH)

    tk.Label(
        result,
        text=str("Predicted personality: {}".format(personality)).title(),
        foreground="black",
        bg="white",
        anchor="w",
    ).pack(fill=tk.BOTH)

    tk.Button(result, text="Exit", command=lambda: result.destroy()).pack()

    terms_mean = """
# Openness:
People who like to learn new things and enjoy new experiences usually score high in openness.
# Conscientiousness:
People that have a high degree of conscientiousness are reliable and prompt.
# Extraversion:
Extraversion traits include being energetic, talkative, and assertive.
# Agreeableness:
These individuals are warm, friendly, compassionate and cooperative.
# Neuroticism:
Neuroticism relates to the degree of negative emotions.
"""
    tk.Label(result, text=terms_mean, justify=tk.LEFT).pack(fill=tk.BOTH)
    result.mainloop()


def OpenFile(button):
    global loc
    name = filedialog.askopenfilename(
        initialdir="C:/Users",
        filetypes=(("Document", "*.docx*"), ("PDF", "*.pdf*"), ("All files", "*")),
        title="Choose a file.",
    )
    if name:
        loc = name
        button.config(text=os.path.basename(name))
    return loc


def predict_person():
    global root, loc
    root.withdraw()

    top = tk.Toplevel()
    top.geometry("700x500")
    top.configure(background="black")
    top.title("Apply For A Job")

    title_font = font.Font(family="Helvetica", size=20, weight="bold")
    tk.Label(top, text="Personality Prediction", foreground="red", bg="black", font=title_font, pady=10).pack()

    loc = ""
    job_list = ("Select Job", "101-Developer at TTC", "102-Chef at Taj", "103-Professor at MIT")
    job = tk.StringVar(top)
    job.set(job_list[0])

    tk.Label(top, text="Applicant Name", foreground="white", bg="black").place(x=70, y=130)
    tk.Label(top, text="Age", foreground="white", bg="black").place(x=70, y=160)
    tk.Label(top, text="Gender", foreground="white", bg="black").place(x=70, y=190)
    tk.Label(top, text="Upload Resume", foreground="white", bg="black").place(x=70, y=220)

    s_name = tk.Entry(top)
    s_name.place(x=450, y=130, width=160)

    age = tk.Entry(top)
    age.place(x=450, y=160, width=160)

    gender = tk.IntVar()
    tk.Radiobutton(top, text="Male", variable=gender, value=1, padx=7).place(x=450, y=190)
    tk.Radiobutton(top, text="Female", variable=gender, value=0, padx=3).place(x=540, y=190)

    cv_button = tk.Button(top, text="Select File", command=lambda: OpenFile(cv_button))
    cv_button.place(x=450, y=220, width=160)

    labels = [
        ("Enjoy New Experience or Thing (Openness)", 250),
        ("How often you feel negativity (Neuroticism)", 280),
        ("Wishing to do work thoroughly (Conscientiousness)", 310),
        ("How much would you like peers (Agreeableness)", 340),
        ("How outgoing and social you are (Extraversion)", 370),
    ]

    entries = {}
    for label_text, y_position in labels:
        tk.Label(top, text=label_text, foreground="white", bg="black").place(x=70, y=y_position)
        entry = tk.Entry(top)
        entry.insert(0, "1-10")
        entry.place(x=450, y=y_position, width=160)
        entries[label_text] = entry

    def submit_form():
        personality_values = [
            gender.get(),
            float(age.get() or 0),
            float(entries[labels[0][0]].get().replace("1-10", "5") or 5),
            float(entries[labels[1][0]].get().replace("1-10", "5") or 5),
            float(entries[labels[2][0]].get().replace("1-10", "5") or 5),
            float(entries[labels[3][0]].get().replace("1-10", "5") or 5),
            float(entries[labels[4][0]].get().replace("1-10", "5") or 5),
        ]
        prediction_result(top, s_name.get(), loc, personality_values)

    submit_btn = tk.Button(top, text="Submit", bg="red", fg="white", command=submit_form)
    submit_btn.place(x=350, y=420, width=200)

    top.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x500")
    root.configure(background="white")
    root.title("Personality Prediction System")

    title_font = font.Font(family="Helvetica", size=25, weight="bold")
    home_btn_font = font.Font(size=12, weight="bold")

    tk.Label(root, text="Personality Prediction System", bg="white", font=title_font, pady=30).pack()
    tk.Button(
        root,
        padx=4,
        pady=4,
        width=30,
        text="Predict Personality",
        foreground="white",
        bd=1,
        font=home_btn_font,
        bg="black",
        command=predict_person,
    ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    root.mainloop()