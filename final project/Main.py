from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image , ImageTk # for images
from Doctor import Doctor
from Patient import Patient
from Treatment import Treatment
from tkinter import messagebox


# setting data bases
patientList = []
doctorList = []
doctorNameList = []
treatmentList = []

# search methods
def searchPatientByName(pList, given_name):
    for patient in pList:
        if patient.fullName == given_name:
            return patient
    return None

def searchDoctorByName(dList, given_name):
    for doctor in dList:
        if doctor.fullName == given_name:
            return doctor
    return None

def searchTreatmentBynum(tList, given_id):
    for treatment in tList:
        if treatment.TreatNum == given_id:
            return treatment
    return None

def main():

    # defining preliminary users
    # fullName(str), id(str), age(int), height(int), weight(int), speciality(str), password(str)
    doc1 = Doctor("Eden Vilinsky", "11", 28, 183, 78, "Neurologist", "master")
    doc2 = Doctor("Guy Marcus", "222222222", 30, 178, 74, "Heart surgeon", "i_know_stuff")
    doc3 = Doctor("Omry Hemo", "333333333", 34, 175, 70, "Orthopedist", "bone_doc")
    doc4 = Doctor("Almog Malka", "444444444", 26, 164, 62, "Dermatologist", "skin_on_skin")
    doctorList.append(doc1)
    doctorList.append(doc2)
    doctorList.append(doc3)
    doctorList.append(doc4)
    doctorNameList.append(doc1.fullName)
    doctorNameList.append(doc2.fullName)
    doctorNameList.append(doc3.fullName)
    doctorNameList.append(doc4.fullName)


    # define preliminary patients
    # fullName(str), id(str), age(int), height(int), weight(int)
    pat1 = Patient("Eitan Vinograd", "123456789", 59, 190, 98)
    pat2 = Patient("Stav Levi", "234567891", 37, 173, 70)
    pat3 = Patient("Liel Ben David", "345678912", 42, 165, 63)
    pat4 = Patient("Eliran Keren", "456789123", 48, 197, 95)
    patientList.append(pat1)
    patientList.append(pat2)
    patientList.append(pat3)
    patientList.append(pat4)


    # define preliminary treatments
    # treatName(str), treatReason(str), treatArea(str), Doctor(Doctor), Patient(Patient)
    treat1 = Treatment("Ablation (burning)", "Heart arrhythmias", "Left side of chest", doc2, pat1)
    pat1.addTreat(treat1)
    treat2 = Treatment("Cast on shin to fixate bone", "Broken bone in shin", "Right leg", doc3, pat2)
    pat2.addTreat(treat2)
    treat3 = Treatment("Annual checkup", "Risk group", "Full body", doc4, pat3)
    pat3.addTreat(treat3)
    treat4 = Treatment("Final confirmation", "HNPP", "Nervous system", doc1, pat4)
    pat4.addTreat(treat4)

#################################################################### end of preliminary definitions and beginning of login page definition

    # login page definition
    LoginPage = tk.Tk()
    LoginPage.title("Log In Page")
    LoginPage.geometry("500x500+10+20")
    LoginPage.configure(bg = "white")

    # login page design
    # logo image for login page
    logimg = Image.open("LoginPage_image.png")
    logimg = logimg.resize((220, 220))
    welcome_logo = ImageTk.PhotoImage(logimg)
    img_label = tk.Label(LoginPage, image=welcome_logo, borderwidth=0, bg = "white")
    img_label.image = welcome_logo
    img_label.place(x=150, y=20)


    # request doctor ID and placing
    DocId = tk.Label(LoginPage, text ="Doctor ID", bg = "light blue", fg = "black")
    DocId.place(x = 100, y = 300)
    DocEnt = tk.Entry(LoginPage, bg = "light blue", fg = "black", font = ("Arial", 12))
    DocEnt.place(x = 200, y = 300)


    # request doctor personal password and placing
    DocPass = tk.Label(LoginPage, text="Password", bg = "light blue", fg = "black")
    DocPass.place(x = 100, y = 340)
    PassEnt = tk.Entry(LoginPage, bg = "light blue", fg = "black", font = ("Arial", 12),show = "*")
    PassEnt.place(x = 200, y = 340)

    # entry button and placing
    EntButton = tk.Button(LoginPage, text = "Enter", bg = "light green", fg = "black", font = ("Arial", 12, "bold"), command=lambda: open_Home_page(DocEnt, PassEnt))
    EntButton.place(x = 220, y = 400)

    LoginPage.mainloop()

######################################################################################### end of login page and beginning of Homepage

# enter Home Page
def open_Home_page(DocEnt, PassEnt):
    id_val = DocEnt.get()
    pass_val = PassEnt.get()
    for doct in doctorList: # go over list of doctors and confirm login details
        if doct.id == id_val and doct.password == pass_val:
            # home page definition
            width = 500
            height = 500
            HomePage = tk.Tk()
            HomePage.title("Home Page")
            HomePage.geometry(f"{width}x{height}+10+20")

            # Home page design
            HomePage.configure(bg="light grey")
            top_frame = tk.Frame(HomePage, bg="orange", height=height*0.1)
            top_frame.pack(fill="x")
            greet_label = tk.Label(HomePage, text=f"Welcome Doctor {doct.fullName}", font = ("Cascadia", 16, "bold"))
            greet_label.place(x=40, y=10)
            right_frame = tk.Frame(HomePage, bg="light blue", width=width * 0.2)
            right_frame.pack(side="right", fill="y")
            left_frame0 = tk.Frame(HomePage, bg="light green", width=width * 0.85)
            left_frame0.pack(side="left", fill="y")

            # home page sidebar buttons
            # add treatment button
            btn1 = tk.Button(right_frame, text="Add Treatment", width=12, bg="white", command=lambda: left_frame1())
            btn1.pack(pady=10)  # vertical spacing
            def left_frame1():
                left_frame0.pack_forget()  # hide default left frame 0
                left_frame1 = tk.Frame(HomePage, bg="light green", width=width * 0.85)
                left_frame1.pack(side="left", fill="y")

                # name of treatment label and entry
                TName = tk.Label(left_frame1, text="Name of treatment", bg="light blue", fg="black")
                TName.place(x=10, y=10, width=width * 0.3, height=height * 0.08)
                TNameEnt = tk.Entry(left_frame1, bg="light blue", fg="black", font=("Arial", 12))
                TNameEnt.place(x=150, y=10, width=width * 0.4, height=height * 0.08)

                # reason for treatment label and entry
                TReason = tk.Label(left_frame1, text="Reason for treatment", bg="light blue", fg="black")
                TReason.place(x=10, y=80, width=width * 0.3, height=height * 0.08)
                TReasonEnt = tk.Entry(left_frame1, bg="light blue", fg="black", font=("Arial", 12))
                TReasonEnt.place(x=150, y=80, width=width * 0.4, height=height * 0.08)

                # area of treatment in the body label and entry
                TArea = tk.Label(left_frame1, text="Treatment area", bg="light blue", fg="black")
                TArea.place(x=10, y=150, width=width * 0.3, height=height * 0.08)
                TAreaEnt = tk.Entry(left_frame1, bg="light blue", fg="black", font=("Arial", 12))
                TAreaEnt.place(x=150, y=150, width=width * 0.4, height=height * 0.08)

                # Doctor that provided treatment label and entry
                TDoctor = tk.Label(left_frame1, text="Attending physician", bg="light blue", fg="black")
                TDoctor.place(x=10, y=220, width=width * 0.3, height=height * 0.08)
                DocSelec = tk.StringVar()
                Dvalues = {doc.fullName: doc for doc in doctorList}
                TDoctorEnt = ttk.Combobox(left_frame1, textvariable=DocSelec, values= list(Dvalues.keys()), state="readonly")  # user must choose from list
                TDoctorEnt.place(x=150, y=220, width=width * 0.4, height=height * 0.08)
                TDoctorEnt.current(0)

                # Patient that recieved treatment label and entry
                TPatient = tk.Label(left_frame1, text="Patient", bg="light blue", fg="black")
                TPatient.place(x=10, y=290, width=width * 0.3, height=height * 0.08)
                PatSelec = tk.StringVar()
                Pvalues = {pat.fullName: pat for pat in patientList}
                TPatientEnt = ttk.Combobox(left_frame1, textvariable=PatSelec, values= list(Pvalues.keys()), state="readonly")
                TPatientEnt.place(x=150, y=290, width=width * 0.4, height=height * 0.08)
                TPatientEnt.current(0)

                #selected_patient = Pvalues[PatSelec.get()]
                # save details button
                def save_treatment():
                    #name = TNameEnt.get()
                    #reason = TReasonEnt.get()
                    #area = TAreaEnt.get()
                    #doctor_obj = searchDoctorByName(doctorList, DocSelec.get())
                    #patient_obj = searchPatientByName(patientList, PatSelec.get())

                    # validation
                    name = TNameEnt.get()
                    reason = TReasonEnt.get()
                    area = TAreaEnt.get()
                    if not name or not reason or not area:
                        messagebox.showerror("Error", "All fields must be filled", parent=left_frame1.winfo_toplevel())
                        return
                    doctor = Dvalues.get(DocSelec.get())
                    patient = Pvalues.get(PatSelec.get())

                    if doctor is None or patient is None:
                        messagebox.showerror(
                            "Error",
                            "Invalid doctor or patient selection",
                            parent=left_frame1.winfo_toplevel()
                        )
                        return

                    treatment = Treatment(name, reason, area, doctor, patient)
                    patient.addTreat(treatment)
                    treatmentList.append(treatment)
                    messagebox.showinfo("Success", "Treatment added successfully!", parent=left_frame1.winfo_toplevel())

                Savebtn = tk.Button(left_frame1, text="Save Treatment", command=save_treatment)
                Savebtn.place(x=70, y=360, width=width * 0.4, height=height * 0.08)
            # Treatment.__init__(TNameEnt, TReasonEnt, TAreaEnt, Do, Pa)
            # treatName(str), treatReason(str), treatArea(str), Doctor(Doctor), Patient(Patient)

            # treatment history button
            btn2 = tk.Button(right_frame, text="History", width=12, bg="white")
            btn2.pack(pady=10)  # vertical spacing

            # search patient button
            btn3 = tk.Button(right_frame, text="Patients", width=12, bg="white")
            btn3.pack(pady=10)  # vertical spacing

            # add new patient button
            btn4 = tk.Button(right_frame, text="New Patient", width=12, bg="white")
            btn4.pack(pady=10)  # vertical spacing

            # edit personal details button
            btn5 = tk.Button(right_frame, text="Personal details", width=12, bg="white")
            btn5.pack(pady=10)  # vertical spacing

            # Log out button
            btn6 = tk.Button(right_frame, text="Log out", width=12, bg="white")
            btn6.pack(pady=10)  # vertical spacing
            return

    # if details are incorrect
    messagebox.showerror("Login Failed", "Incorrect ID or password")


if __name__ == "__main__":
    main()
