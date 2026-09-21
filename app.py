
import os
import tkinter.font as font
from tkinter import *
from tkinter import filedialog

try:
    import pandas as pd
except ImportError:
    pd = None  # type: ignore[assignment]

try:
    from pyresparser import ResumeParser
except Exception:
    ResumeParser = None

try:
    from sklearn import linear_model
except ImportError:
    linear_model = None  # type: ignore[assignment]


def extract_resume_text(cv_path):
    if not cv_path:
        return ""

    if ResumeParser is not None:
        try:
            return str(ResumeParser(cv_path).get_extracted_data())
        except Exception:
            pass

    lower_path = cv_path.lower()

    if lower_path.endswith('.pdf'):
        try:
            from pypdf import PdfReader
            reader = PdfReader(cv_path)
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(pages)
        except Exception:
            return ""

    if lower_path.endswith('.docx'):
        try:
            from docx import Document
            doc = Document(cv_path)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            return ""

    try:
        with open(cv_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ""

class train_model:
    def train(self):
        csv_path = os.path.join(os.path.dirname(__file__), 'training_dataset.csv')
        data = pd.read_csv(csv_path)
        array = data.values
        for row in array:
            if row[0] == "Male":
                row[0] = 1
            else:
                row[0] = 0
        df=pd.DataFrame(array) 
        maindf=df[[0,1,2,3,4,5,6]] 
        mainarray=maindf.values 
        temp=df[7] 
        train_y =temp.values
        self.mul_lr = linear_model.LogisticRegression (
            multi_class='multinomial',
            solver='newton-cg',
            max_iter =1000
        )
        self.mul_lr.fit (mainarray,train_y) 

    def test(self,test_data):
        try:
            test_predict= list () 
            for i in test_data: 
                test_predict.append (int(i)) 
            y_pred=self.mul_lr.predict([test_predict]) 
            return y_pred 
        except Exception:
            print ("All Factors For Finding Personality Not Entered!")

def check_type(data):
    if type(data)==str or type(data)==str: 
        return str(data).title() 
    if type(data)==list or type(data)==tuple:
        str_list = ""
        for item in data:
            str_list += str(item) + ", "
        return str_list
    else: 
        return str(data)
    
def  prediction_result(top, aplcnt_name, cv_path, personality_values):
    "after applying a job" 
    top.withdraw()

    applicant_name = aplcnt_name.get() if hasattr(aplcnt_name, 'get') else str(aplcnt_name)

    applicant_data = {
        "Candidate Name": applicant_name,
        "CV Location": cv_path
    } 
    age = personality_values[1] if len(personality_values) > 1 else 0
    print("\n#############Candidate Entered Data#############\n")  
    print(applicant_data, personality_values) 

    personality = model.test(personality_values)
    personality_text = str(personality).replace("[", "").replace("]", "").replace("'", "")
    print("\n#############Predicted Personality#############\n")
    print(personality)

    data = {}
    if cv_path:
        text = extract_resume_text(cv_path)
        data = {
            'name': None,
            'mobile_number': None,
            'email': None,
            'summary': text[:500],
            'skills': [],
            'raw_text': text,
        }

    if isinstance(data, dict):
        try:
            data.pop('name', None)
            mobile_number = data.get('mobile_number')
            if mobile_number is not None and len(str(mobile_number)) < 10:
                data.pop('mobile_number', None)
        except Exception:
            pass

    print("\n#############Resume Parsed Data#############\n")
    for key in data.keys():
        if data[key] is not None:
            print('{}: {}'.format(key, data[key]))
    result = Toplevel()
    result.configure(background='White')
    result.title("Predicted Personality")
    result.resizable(True, True)

    width = 780
    height = 700
    result.update_idletasks()
    x = (result.winfo_screenwidth() // 2) - (width // 2)
    y = (result.winfo_screenheight() // 2) - (height // 2)
    result.geometry(f"{width}x{height}+{x}+{y}")

    titleFont=font.Font(family='Arial', size=18, weight='bold')
    labelFont=font.Font(family='Arial', size=10, weight='bold')

    outer_frame = Frame(result, bg='white', bd=2, relief='solid', padx=12, pady=12)
    outer_frame.pack(fill=BOTH, expand=True, padx=18, pady=18)

    main_frame = Frame(outer_frame, bg='white', bd=1, relief='groove', padx=12, pady=12)
    main_frame.pack(fill=BOTH, expand=True)

    canvas = Canvas(main_frame, bg='white', highlightthickness=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    y_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    y_scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=y_scrollbar.set)
    content_frame = Frame(canvas, bg='white', padx=20, pady=20)

    def center_canvas_content(event=None):
        canvas.update_idletasks()
        usable_width = max(canvas.winfo_width() - 60, 550)
        canvas.coords(content_frame_id, canvas.winfo_width() / 2, 0)
        canvas.itemconfigure(content_frame_id, width=usable_width)

    content_frame_id = canvas.create_window((0, 0), window=content_frame, anchor='n')
    center_canvas_content()
    canvas.bind("<Configure>", center_canvas_content)

    def _on_mouse_wheel(event):
        if event.state & 0x1:
            canvas.xview_scroll(int(-event.delta / 120), "units")
        else:
            canvas.yview_scroll(int(-event.delta / 120), "units")

    def _on_shift_mouse_wheel(event):
        canvas.xview_scroll(int(-event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
    canvas.bind_all("<Shift-MouseWheel>", _on_shift_mouse_wheel)
    canvas.bind_all("<Button-4>", lambda _event: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda _event: canvas.yview_scroll(1, "units"))

    Label(
        content_frame,
        text="Result Personality Prediction",
        foreground='green',
        bg='white',
        font=titleFont,
        pady=10,
        justify=CENTER,
        anchor=CENTER,
        padx=20
    ).pack(fill=X, pady=(10, 5), padx=10)

    applicant_name_display = aplcnt_name.get() if hasattr(aplcnt_name, 'get') else str(aplcnt_name)

    Label(
        content_frame,
        text=str('{}:{}'.format("Name:", applicant_name_display)).title(),
        foreground='black',
        bg='white',
        font=labelFont,
        justify=CENTER,
        anchor=CENTER
    ).pack(fill=X, pady=3)

    Label(
        content_frame,
        text=str('{}:{}'.format("Age:", age)),
        foreground='black',
        bg='white',
        font=labelFont,
        justify=CENTER,
        anchor=CENTER
    ).pack(fill=X, pady=3)

    for key in data.keys():
        if data[key] is not None:
            Label(
                content_frame,
                text=str('{}:{}'.format(key.title(), check_type(data[key]))),
                foreground='black',
                bg='white',
                font=labelFont,
                justify=CENTER,
                anchor=CENTER,
                wraplength=620,
                width=80
            ).pack(fill=X, pady=3, padx=10)

    Label(
        content_frame,
        text="Predicted Personality: " + personality_text + ", Age: " + str(age),
        foreground='black',
        bg='white',
        font=labelFont,
        justify=CENTER,
        anchor=CENTER
    ).pack(fill=X, pady=8)

    quitBtn=Button(content_frame,text="Exit",font=labelFont,command=lambda: result.destroy())
    quitBtn.pack(pady=10)

    terms_mean=""" 
        #Openness: 
        People who like to learn new things and enjoy new experiences usually score high in openness. 
        Openness includes traits like being insightful and imaginative and having a wide variety of 
        interests. 
        #Conscientiousness: 
        People that have a high degree of conscientiousness are reliable and prompt. Traits include 
        being organised, methodic, and thorough. 
        #Extraversion: 
        Extraversion traits include being energetic, talkative, and assertive (sometimes seen as 
        outspoken by Introverts). Extraverts get their energy and drive from others, while introverts get their drive from within themselves. 
        #Agreeableness: 
        As it perhaps sounds, these individuals are warm, friendly, compassionate and cooperative and traits include being kind, affectionate, and sympathetic. In contrast, people with lower levels of 
        agreeableness may be more distant. 
        #Neuroticism: 
        Neuroticism or Emotional Stability relates to degree of negative emotions. People that score high 
        on neuroticism often experience emotional instability and negative emotions. Characteristics 
        typically include being moody and tense. 
        """ 
    Label(content_frame,text=terms_mean,justify=CENTER, bg='white', font=font.Font(family='Arial', size=9, weight='normal'), wraplength=620).pack(fill=BOTH, padx=20, pady=10)

    content_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    result.mainloop() 

def predict_person():
    """Predict Personality""" 

    #Closing The Previous Window  
    root.withdraw() 

    # Creating new window 
    top = Toplevel()
    top.geometry('700x500') 
    top.configure(background='black') 
    top.title("Apply For A Job") 

    #Title 
    titleFont=font.Font(family='Helvetica',size=20,weight='bold')
    Label(
        top, text="PersonalityPrediction",
        foreground='red', 
        bg='black',
        font=titleFont,
        pady=10
    ).pack()
    
    #Job_Form 
    job_list=('SelectJob','101-DeveloperatTTC','102-ChefatTaj','103- Professor at MIT') 
    job=StringVar(top)
    job.set(job_list[0])

    Label(top,text="ApplicantName",foreground='white', bg='black').place(x=70, y=130)
    Label(top,text="Age",foreground='white',bg='black').place(x=70, y=160)
    Label(top,text="Gender",foreground='white', bg='black').place(x=70, y=190)
    Label(top,text="UploadResume",foreground='white', bg='black').place(x=70, y=220)
    Label(top,text="EnjoyNewExperienceorthing(Openness)",foreground='white', bg='black').place(x=70, y=250)
    Label(top,text="How Offen You Feel Negativity(Neuroticism)", foreground='white', bg='black').place(x=70, y=280)
    Label(top,text="Wishing to do one's work well and thoroughly(Conscientiousness)",foreground='white', bg='black').place(x=70, y=310)
    Label(top,text="How much would you like peers(Agreeableness)",foreground='white',bg='black').place(x=70, y=340)
    Label(top,text="How outgoing and social like(Extraversion)",foreground='white',bg='black').place(x=70,y=370)

    sName=Entry(top) 
    sName.place(x=450,y=130,width=160) 

    age=Entry(top) 
    age.place(x=450,y=160,width=160)

    gender = IntVar() 
    #work with interaction 
    R1=Radiobutton(top,text="Male",variable=gender,value=1,padx=7)
    R1.place(x=450, y=190) 

    R2=Radiobutton(top,text="Female",variable=gender,value=0, padx=3) 
    R2.place(x=540,y=190) 

    cv=Button(top,text="SelectFile",command=lambda:OpenFile(cv)) 
    cv.place(x=450, y=220, width=160) 

    openness=Entry(top) 
    openness.insert(0,'1-10')
    openness.place(x=450, y=250, width=160)  

    neuroticism=Entry(top)
    neuroticism.insert(0,'1-10')
    neuroticism.place(x=450,y=280,width=160)  

    conscientiousness=Entry(top)
    conscientiousness.insert(0,'1-10') 
    conscientiousness.place(x=450,y=310,width=160)  

    agreeableness=Entry(top) 
    agreeableness.insert(0,'1-10') 
    agreeableness.place(x=450,y=340,width=160)  

    extraversion=Entry(top)
    extraversion.insert(0,'1-10')
    extraversion.place(x=450, y=370, width=160) 

    submitBtn = Button(
        top,
        padx=2,
        pady=0,
        text="Submit",
        bd=0,
        foreground='white',
        font=("Arial", 12),
        bg='red'
        )
    submitBtn.config(
        command=lambda: prediction_result(
            top,
            sName.get(),
            loc,
            (
                gender.get(),
                age.get(),
                openness.get(),
                neuroticism.get(),
                conscientiousness.get(),
                agreeableness.get(),
                extraversion.get()
            )
        )
    )
    submitBtn.place(x=350,y=400,width=200) 

    top.mainloop()  

def OpenFile(b4):
    global loc
    name = filedialog.askopenfilename(
        initialdir="C:/Users/Downloads",
        filetypes=(("Document", "*.docx*"), ("PDF", "*.pdf*"), ("All files", "*")),
        title="Choose a file."
    )
    if name:
        loc = name
        filename = os.path.basename(name)
        b4.config(text=filename)
    return loc

if __name__ == "__main__":
    loc = ""
    root = Tk()   
    model = train_model() 
    model.train() 
    root.geometry('700x500')  
    root.configure(background='white') 
    root.title("Personality Prediction System") 

    titleFont = font.Font(family='Helvetica', size=25, weight='bold')
    homeBtnFont = font.Font(size=12, weight='bold')

    label=Label(
        root,
        text="PersonalityPredictionSystem",
        bg='white',
        font=titleFont,
        pady=30
        )
    label.pack() 

    b2=Button(
        root,
        padx=4,
        pady=4,
        width=30,
        text="PredictPersonality", 
        foreground='white', 
        bd=1,
        font=homeBtnFont,
        bg='black', 
        command=predict_person
    )
    b2.place(
        relx=0.5,
        rely=0.5,
        anchor=CENTER
    ) 
    root.mainloop()