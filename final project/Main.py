from datetime import datetime
import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # for images
from Doctor import Doctor
from Medication import Medication
from Patient import Patient
from Treatment import Treatment
from tkinter import messagebox

# setting global data bases
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


# ---------- NEW: login handler (single-window flow) ----------
def try_login(id_val, pass_val, on_success):
    for doct in doctorList:
        if doct.id == id_val and doct.password == pass_val:
            on_success(doct)
            return
    messagebox.showerror("Login Failed", "Incorrect ID or password")


# ---------- NEW: build home screen inside the SAME root window ----------
def build_home_screen(doct, home_frame, show_login):
    # clear home_frame before rebuilding UI (important when switching doctors)
    for w in home_frame.winfo_children():
        w.destroy()

    # home page definition
    width = 500
    height = 500

    # Home page design
    home_frame.configure(bg="light grey")
    top_frame = tk.Frame(home_frame, bg="orange", height=int(height * 0.1))
    top_frame.pack(fill="x")

    greet_label = tk.Label(
        home_frame,
        text=f"Welcome Doctor {doct.fullName}",
        font=("Cascadia", 16, "bold"),
        bg="orange"
    )
    greet_label.place(x=40, y=10)

    # sidebar menu
    right_frame = tk.Frame(home_frame, bg="light blue", width=int(width * 0.2))
    right_frame.pack(side="right", fill="y")

    # details request and information menu
    left_frame0 = tk.Frame(home_frame, bg="light green", width=int(width * 0.85))
    left_frame0.pack(side="left", fill="both", expand=True)

    # leave one page to the other
    def clear_left_frame():
        for widget in left_frame0.winfo_children():
            widget.destroy()

    # ---------- HOME BUTTON SYSTEM (ONE BUTTON ONLY) ----------
    home_btn = None

    # show only when not on home page
    def hide_home_button():
        nonlocal home_btn
        if home_btn is not None:
            home_btn.place_forget()

############################################################################ begining of home page definition

    def left_frame_home():
        clear_left_frame()
        hide_home_button()

        frame = tk.Frame(left_frame0, bg="light green")
        frame.pack(fill="both", expand=True)

        today = datetime.now().date()

        my_treatments = [t for t in treatmentList if t.Doctor == doct]
        my_treatments_today = [t for t in my_treatments if t.TreatDate.date() == today]

        # unique patients for this doctor
        treated_ids = set()
        treated_patients = []
        for t in my_treatments:
            p = t.Patient
            if p.id not in treated_ids:
                treated_ids.add(p.id)
                treated_patients.append(p)

        # patients in system not treated yet by this doctor
        waiting_count = sum(1 for p in patientList if p.id not in treated_ids)

        # last activity
        last_text = "No treatments yet."
        if my_treatments:
            last_t = max(my_treatments, key=lambda x: x.TreatDate)
            last_text = f"{last_t.TreatDate.strftime('%d/%m %H:%M')} - {last_t.Patient.fullName}"

        # home page title
        tk.Label(frame, text="Control Panel", font=("Arial", 18, "bold"), bg="light green").place(x=150, y=15)
        tk.Label(frame, text=f"Today: {datetime.now().strftime('%d/%m/%Y')}",
                 font=("Arial", 11), bg="light green").place(x=185, y=45)

        # draw a "card" helper. cards contain details
        def card(x, y, title_txt, value_txt, w=200, h=80, big_font=18):
            c = tk.Frame(frame, bg="white", bd=2, relief="groove")
            c.place(x=x, y=y, width=w, height=h)

            tk.Label(c, text=title_txt, font=("Arial", 10, "bold"), bg="white").pack(pady=(10, 0))
            tk.Label(
                c,
                text=value_txt,
                font=("Arial", big_font, "bold"),
                bg="white",
                wraplength=w - 20,
                justify="center"
            ).pack(pady=(6, 0))

        # --- cards layout (fits 500x500) ---
        # row 1
        card(30, 90, "Treatments Today", str(len(my_treatments_today)), w=200, h=80)
        card(260, 90, "My Patients", str(len(treated_patients)), w=200, h=80)

        # row 2
        card(30, 185, "Patients Not Treated Yet", str(waiting_count), w=200, h=80)

        # last activity needs a bit more height and smaller font (text is longer)
        card(260, 185, "Last Activity", last_text, w=200, h=90, big_font=11)

        # recent treatments (last 5)
        tk.Label(frame, text="Recent Treatments (last 5)", font=("Arial", 11, "bold"),
                 bg="light green").place(x=30, y=300)

        recent = sorted(my_treatments, key=lambda x: x.TreatDate, reverse=True)[:5]
        y = 330

        if not recent:
            tk.Label(frame, text="No treatments yet.", bg="light green").place(x=30, y=y)
        else:
            for t in recent:
                txt = f"{t.TreatDate.strftime('%d/%m %H:%M')} | {t.Patient.fullName} | {t.TreatName}"
                tk.Label(frame, text=txt, bg="light green", anchor="w", font=("Arial", 10)).place(x=30, y=y, width=440)
                y += 22

    # show when not on home page
    def show_home_button():
        nonlocal home_btn
        if home_btn is None:
            home_btn = tk.Button(
                top_frame,
                text="HOME",
                bg="orange",
                fg="black",
                font=("Arial", 10, "bold"),
                command=left_frame_home
            )

        # home button placing, top right corner.
        home_btn.place(relx=0.97, y=8, anchor="ne", width=70, height=28)

    left_frame_home()

######################################################################### begining of add treatment from sidebar menu

    # add treatment button
    btn1 = tk.Button(right_frame, text="Add Treatment", width=12, bg="white", command=lambda: left_frame1())
    btn1.pack(pady=10)  # vertical spacing

    def left_frame1():
        clear_left_frame()
        left_frame1 = tk.Frame(left_frame0, bg="light green")
        left_frame1.pack(fill="both", expand=True)
        show_home_button()
        # Row 1: Doctor (logged in)
        TDoctor = tk.Label(left_frame1, text="Attending physician", bg="light blue", fg="black")
        TDoctor.place(x=10, y=10, width=width * 0.3, height=height * 0.08)

        DoctorEnt = tk.Entry(left_frame1, bg="light grey", fg="black", font=("Arial", 12))
        DoctorEnt.place(x=150, y=10, width=width * 0.4, height=height * 0.08)
        DoctorEnt.insert(0, doct.fullName)
        DoctorEnt.config(state="readonly")

        # Row 2: Patient
        TPatient = tk.Label(left_frame1, text="Patient", bg="light blue", fg="black")
        TPatient.place(x=10, y=80, width=width * 0.3, height=height * 0.08)

        PatSelec = tk.StringVar(value="")
        Pvalues = {pat.fullName: pat for pat in patientList}
        TPatientEnt = ttk.Combobox(left_frame1, textvariable=PatSelec, values=list(Pvalues.keys()), state="readonly")
        TPatientEnt.place(x=150, y=80, width=width * 0.4, height=height * 0.08)
        TPatientEnt.set("")

        # Row 3: Name of treatment
        TName = tk.Label(left_frame1, text="Name of treatment", bg="light blue", fg="black")
        TName.place(x=10, y=150, width=width * 0.3, height=height * 0.08)

        TNameEnt = tk.Entry(left_frame1, bg="light blue", fg="black", font=("Arial", 12))
        TNameEnt.place(x=150, y=150, width=width * 0.4, height=height * 0.08)

        # Row 4: Reason
        TReason = tk.Label(left_frame1, text="Reason for treatment", bg="light blue", fg="black")
        TReason.place(x=10, y=220, width=width * 0.3, height=height * 0.08)

        TReasonEnt = tk.Entry(left_frame1, bg="light blue", fg="black", font=("Arial", 12))
        TReasonEnt.place(x=150, y=220, width=width * 0.4, height=height * 0.08)

        # Row 5: Area
        TArea = tk.Label(left_frame1, text="Treatment area", bg="light blue", fg="black")
        TArea.place(x=10, y=290, width=width * 0.3, height=height * 0.08)

        TAreaEnt = tk.Entry(left_frame1, bg="light blue", fg="black", font=("Arial", 12))
        TAreaEnt.place(x=150, y=290, width=width * 0.4, height=height * 0.08)

        # save details button
        def save_treatment():
            # validation
            name = TNameEnt.get().strip()
            reason = TReasonEnt.get().strip()
            area = TAreaEnt.get().strip()
            chosen_patient_name = TPatientEnt.get().strip()

            if not name or not reason or not area:
                messagebox.showerror("Error", "All fields must be filled", parent=left_frame1.winfo_toplevel())
                return

            if not chosen_patient_name:
                messagebox.showerror("Error", "You must choose a patient", parent=left_frame1.winfo_toplevel())
                return

            # Doctor is logged-in doctor
            doctor = doct

            # Patient from selection
            patient = Pvalues.get(chosen_patient_name)

            if patient is None:
                messagebox.showerror("Error", "Invalid patient selection", parent=left_frame1.winfo_toplevel())
                return

            treatment = Treatment(name, reason, area, doctor, patient)
            patient.addTreat(treatment)
            doctor.addTreat(treatment)
            treatmentList.append(treatment)

            messagebox.showinfo("Success", "Treatment added successfully!", parent=left_frame1.winfo_toplevel())

        Savebtn = tk.Button(left_frame1, text="Save Treatment", command=save_treatment)
        Savebtn.place(x=70, y=360, width=width * 0.4, height=height * 0.08)

######################################################################## end of Add treatment menu and begining of treatment History menu

    # treatment history button
    btn2 = tk.Button(right_frame, text="History", width=12, bg="white", command=lambda: left_frame2())
    btn2.pack(pady=10)  # vertical spacing

    # History left menu
    def left_frame2():
        # clear previous left content
        clear_left_frame()
        # main container for history screen
        frame = tk.Frame(left_frame0, bg="light green")
        frame.pack(fill="both", expand=True)
        show_home_button()
        title = tk.Label(frame, text="Treatment History", font=("Arial", 16, "bold"), bg="light green")
        title.pack(pady=10)

        # filter treatments by logged-in doctor and sort by date (newest first)
        doctor_treatments = sorted([t for t in treatmentList if t.Doctor == doct], key=lambda t: t.TreatDate,
                                   reverse=True)

        if not doctor_treatments:
            tk.Label(frame, text="No treatments found.", font=("Arial", 12), bg="light green").pack(pady=20)
            return

        # scrolling area
        canvas = tk.Canvas(frame, bg="light green", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="light green")
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # show each treatment
        for t in doctor_treatments:
            card = tk.Frame(scroll_frame, bg="white", bd=2, relief="groove")
            card.pack(fill="x", padx=20, pady=6)
            tk.Label(card, text=f"Date: {t.TreatDate.strftime('%d/%m/%Y')}", font=("Arial", 10, "bold"),
                     bg="white").pack(anchor="w", padx=10, pady=(5, 0))
            tk.Label(card, text=f"Patient: {t.Patient.fullName}", bg="white").pack(anchor="w", padx=10)
            tk.Label(card, text=(f"Treatment: {t.TreatName}\n" f"Reason: {t.TreatReason}\n" f"Area: {t.TreatArea}"),
                     bg="white", justify="left", wraplength=380).pack(anchor="w", padx=10, pady=(0, 5))

######################################################################## end of treat History menu and begining of Search Patient menu

    # search patient button
    btn3 = tk.Button(right_frame, text="Patients", width=12, bg="white", command=lambda: left_frame3())
    btn3.pack(pady=10)

    def left_frame3():
        clear_left_frame()

        frame = tk.Frame(left_frame0, bg="light green")
        frame.pack(fill="both", expand=True)
        show_home_button()
        title = tk.Label(frame, text="My Patients", font=("Arial", 16, "bold"), bg="light green")
        title.pack(pady=10)

        # pull all patients treated by the logged-in doctor (no duplicates)
        doctor_patients = []
        seen_ids = set()

        for t in treatmentList:
            if t.Doctor == doct:
                p = t.Patient
                if p.id not in seen_ids:
                    seen_ids.add(p.id)
                    doctor_patients.append(p)

        if not doctor_patients:
            tk.Label(frame, text="No patients found for this doctor.", font=("Arial", 12), bg="light green").pack(
                pady=20)
            return

        # scrolling area
        canvas = tk.Canvas(frame, bg="light green", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="light green")
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # show each patient
        for p in doctor_patients:
            card = tk.Frame(scroll_frame, bg="white", bd=2, relief="groove")
            card.pack(fill="x", padx=20, pady=6)

            tk.Label(card, text=p.fullName, font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10,
                                                                                         pady=(5, 0))
            tk.Label(card, text=f"ID: {p.id}", bg="white").pack(anchor="w", padx=10)
            tk.Label(card, text=f"Age: {p.age} | Height: {p.height} | Weight: {p.weight}", bg="white").pack(anchor="w",
                                                                                                            padx=10,
                                                                                                            pady=(0, 5))

######################################################################## end of search Patient menu and begining of New patient menu

    # sidebar button
    btn4 = tk.Button(right_frame, text="New Patient", width=12, bg="white", command=lambda: left_frame4())
    btn4.pack(pady=10)

    def left_frame4():
        clear_left_frame()

        frame = tk.Frame(left_frame0, bg="light green")
        frame.pack(fill="both", expand=True)
        show_home_button()
        title = tk.Label(frame, text="New Patient", font=("Arial", 16, "bold"), bg="light green")
        title.place(x=160, y=20)

        # layout
        lx, ex = 10, 180
        label_w, entry_w = 160, 220
        row_h, gap = 30, 12
        y0 = 70

        def row(i, label, ent):
            y = y0 + i * (row_h + gap)
            tk.Label(frame, text=label, bg="light blue", fg="black").place(x=lx, y=y, width=label_w, height=row_h)
            ent.place(x=ex, y=y, width=entry_w, height=row_h)

        # entries
        name_ent = tk.Entry(frame, font=("Arial", 12), bg="white")
        id_ent = tk.Entry(frame, font=("Arial", 12), bg="white")
        age_ent = tk.Entry(frame, font=("Arial", 12), bg="white")
        h_ent = tk.Entry(frame, font=("Arial", 12), bg="white")
        w_ent = tk.Entry(frame, font=("Arial", 12), bg="white")

        row(0, "Full Name", name_ent)
        row(1, "Patient ID", id_ent)
        row(2, "Age", age_ent)
        row(3, "Height", h_ent)
        row(4, "Weight", w_ent)

        def save_patient():
            full_name = name_ent.get().strip()
            pid = id_ent.get().strip()
            age_s = age_ent.get().strip()
            h_s = h_ent.get().strip()
            w_s = w_ent.get().strip()

            # basic validation
            if not full_name or not pid or not age_s or not h_s or not w_s:
                messagebox.showerror("Error", "All fields must be filled", parent=frame.winfo_toplevel())
                return

            # ID must be unique
            for p in patientList:
                if p.id == pid:
                    messagebox.showerror("Error", "Patient ID already exists", parent=frame.winfo_toplevel())
                    return

            try:
                age = int(age_s)
                height_v = int(h_s)
                weight_v = int(w_s)
            except ValueError:
                messagebox.showerror("Error", "Age/Height/Weight must be numbers", parent=frame.winfo_toplevel())
                return

            new_pat = Patient(full_name, pid, age, height_v, weight_v)
            patientList.append(new_pat)
            messagebox.showinfo("Success", "Patient added successfully!", parent=frame.winfo_toplevel())

            # optional: clear fields after save
            name_ent.delete(0, tk.END)
            id_ent.delete(0, tk.END)
            age_ent.delete(0, tk.END)
            h_ent.delete(0, tk.END)
            w_ent.delete(0, tk.END)

        save_btn = tk.Button(frame, text="Save Patient", bg="light green", font=("Arial", 12, "bold"),
                             command=save_patient)
        save_btn.place(x=ex, y=y0 + 5 * (row_h + gap) + 10, width=140, height=32)

######################################################################## end of New patient menu and begining of Prescribe Meds menu

    btn5 = tk.Button(
        right_frame,
        text="Prescribe Meds",
        width=12,
        bg="white",
        command=lambda: show_prescribe_meds()
    )
    btn5.pack(pady=10)

    def show_prescribe_meds():
        clear_left_frame()
        show_home_button()

        frame = tk.Frame(left_frame0, bg="light green")
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Prescription Medications",
            font=("Cascadia", 16, "bold"),
            bg="light green"
        ).pack(pady=(30,20),padx=(20,20))

        # ---- Patient dropdown ----
        tk.Label(frame, text="Select Patient:", bg="light green").pack(anchor="w", padx=20, pady=(20,0))
        patient_var = tk.StringVar()
        ttk.Combobox(
            frame,
            textvariable=patient_var,
            values=[p.fullName for p in patientList],
            state="readonly"
        ).pack(padx=20, pady=(0,25))

        # ---- Doctor (logged-in only) ----
        tk.Label(frame, text="Doctor:", bg="light green").pack(anchor="w", padx=20, pady=(20,0))
        doctor_var = tk.StringVar(value=doct.fullName)
        ttk.Combobox(
            frame,
            textvariable=doctor_var,
            values=[doct.fullName],
            state="readonly"
        ).pack(padx=20, pady=(0,25))

        # ---- Medication dropdown ----
        tk.Label(frame, text="Select Medication:", bg="light green").pack(anchor="w", padx=20, pady=(20,0))
        med_var = tk.StringVar()
        ttk.Combobox(
            frame,
            textvariable=med_var,
            values=[m.MedName for m in medicationList],
            state="readonly"
        ).pack(padx=20, pady=(0,25))

        def prescribe():
            if not patient_var.get() or not med_var.get():
                messagebox.showerror("Error", "Please select patient and medication")
                return

            selected_med = next(m for m in medicationList if m.MedName == med_var.get())

            if selected_med.can_be_issued_by(doct):  ############################################### לסנן תרופות רק למה שבסמכות הרופא
                messagebox.showinfo("Success", "Medication prescribed successfully")
            else:
                messagebox.showerror(
                    "Authorization Error",
                    "Doctor is not authorized to prescribe this medication"
                )

        tk.Button(
            frame,
            text="Prescribe",
            bg="light blue",
            font=("Arial", 12, "bold"),
            command=prescribe
        ).pack(pady=20)

############################################################################ end of Prescribe Meds and begining of Personal details

    # sidebar button
    btn5 = tk.Button(right_frame, text="Personal details", width=12, bg="white", command=lambda: left_frame5())
    btn5.pack(pady=10)

    def left_frame5():
        clear_left_frame()

        # new page and tital with placing
        frame = tk.Frame(left_frame0, bg="light green")
        frame.pack(fill="both", expand=True)
        show_home_button()
        title = tk.Label(frame, text="Personal Details", font=("Arial", 16, "bold"), bg="light green")
        title.place(x=120, y=20)

        # --- fixed layout for 500x500 ---
        lx, ex = 10, 180
        label_w = 160
        entry_w = 220

        row_h = 30
        gap = 10
        y0 = 60  # begin under tital

        def row(i, label, widget):
            y = y0 + i * (row_h + gap)
            tk.Label(frame, text=label, bg="light blue", fg="black").place(x=lx, y=y, width=label_w, height=row_h)
            widget.place(x=ex, y=y, width=entry_w, height=row_h)

        # Variables
        name_var = tk.StringVar(value=doct.fullName)
        id_var = tk.StringVar(value=doct.id)
        age_var = tk.StringVar(value=str(doct.age))
        h_var = tk.StringVar(value=str(doct.height))
        w_var = tk.StringVar(value=str(doct.weight))
        spec_var = tk.StringVar(value=getattr(doct, "speciality", ""))

        new_pass_var = tk.StringVar(value="")
        confirm_pass_var = tk.StringVar(value="")

        # Widgets
        name_ent = tk.Entry(frame, textvariable=name_var, font=("Arial", 12), bg="white")
        id_ent = tk.Entry(frame, textvariable=id_var, font=("Arial", 12), bg="light grey", state="readonly")
        age_ent = tk.Entry(frame, textvariable=age_var, font=("Arial", 12), bg="white")
        h_ent = tk.Entry(frame, textvariable=h_var, font=("Arial", 12), bg="white")
        w_ent = tk.Entry(frame, textvariable=w_var, font=("Arial", 12), bg="white")
        spec_ent = tk.Entry(frame, textvariable=spec_var, font=("Arial", 12), bg="white")

        new_pass_ent = tk.Entry(frame, textvariable=new_pass_var, font=("Arial", 12), bg="white", show="*")
        confirm_pass_ent = tk.Entry(frame, textvariable=confirm_pass_var, font=("Arial", 12), bg="white", show="*")

        # Place rows (0..7)
        row(0, "Full Name", name_ent)
        row(1, "Doctor ID", id_ent)
        row(2, "Age", age_ent)
        row(3, "Height", h_ent)
        row(4, "Weight", w_ent)
        row(5, "Speciality", spec_ent)
        row(6, "New Password", new_pass_ent)
        row(7, "Confirm Password", confirm_pass_ent)

        def save_details():
            # Validate numeric fields
            try:
                age = int(age_var.get().strip())
                height_v = int(h_var.get().strip())
                weight_v = int(w_var.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Age/Height/Weight must be numbers", parent=frame.winfo_toplevel())
                return

            doct.fullName = name_var.get().strip()
            doct.age = age
            doct.height = height_v
            doct.weight = weight_v
            doct.speciality = spec_var.get().strip()

            np = new_pass_var.get().strip()
            cp = confirm_pass_var.get().strip()

            if np or cp:
                if np != cp:
                    messagebox.showerror("Error", "Passwords do not match", parent=frame.winfo_toplevel())
                    return
                doct.password = np
                new_pass_var.set("")
                confirm_pass_var.set("")

            messagebox.showinfo("Saved", "Personal details updated!", parent=frame.winfo_toplevel())

        # Save button - placed AFTER last row (no overlap)
        last_y = y0 + 7 * (row_h + gap)
        save_y = last_y + row_h + 12
        save_btn = tk.Button(frame, text="Save", bg="light green", font=("Arial", 12, "bold"), command=save_details)
        save_btn.place(x=ex, y=save_y, width=120, height=32)

########################################################################################### end of Personal details menu

    # Log out button
    btn6 = tk.Button(right_frame, text="Log out", width=12, bg="white", command=show_login)
    btn6.pack(pady=10)  # vertical spacing
    return

# assist function to register medication used in hospital according to departments
def init_medications():
    return [

        # ---------- Neurology ----------
        Medication("Gabapentin", 3, "Neurology", "Nerve pain and seizures"),
        Medication("Pregabalin", 2, "Neurology", "Neuropathic pain"),
        Medication("Levetiracetam", 2, "Neurology", "Epilepsy treatment"),
        Medication("Topiramate", 2, "Neurology", "Migraine prevention"),
        Medication("Carbamazepine", 3, "Neurology", "Seizure control"),
        Medication("Lamotrigine", 2, "Neurology", "Mood stabilization"),
        Medication("Valproate", 2, "Neurology", "Seizure prevention"),
        Medication("Baclofen", 3, "Neurology", "Muscle spasticity"),
        Medication("Clonazepam", 1, "Neurology", "Seizures and anxiety"),
        Medication("Donepezil", 1, "Neurology", "Alzheimer treatment"),
        Medication("Memantine", 1, "Neurology", "Dementia treatment"),
        Medication("Amantadine", 2, "Neurology", "Parkinson symptoms"),

        # ---------- Cardiology ----------
        Medication("Aspirin", 1, "Cardiology", "Blood thinner"),
        Medication("Metoprolol", 2, "Cardiology", "Heart rate control"),
        Medication("Atorvastatin", 1, "Cardiology", "Cholesterol reduction"),
        Medication("Lisinopril", 1, "Cardiology", "Blood pressure control"),
        Medication("Losartan", 1, "Cardiology", "Hypertension"),
        Medication("Furosemide", 2, "Cardiology", "Fluid removal"),
        Medication("Spironolactone", 1, "Cardiology", "Heart failure"),
        Medication("Digoxin", 1, "Cardiology", "Heart contraction strength"),
        Medication("Amlodipine", 1, "Cardiology", "Angina prevention"),
        Medication("Clopidogrel", 1, "Cardiology", "Prevent blood clots"),
        Medication("Warfarin", 1, "Cardiology", "Anticoagulant"),
        Medication("Bisoprolol", 1, "Cardiology", "Heart rhythm control"),

        # ---------- Orthopedics ----------
        Medication("Ibuprofen", 3, "Orthopedics", "Pain and inflammation"),
        Medication("Diclofenac", 2, "Orthopedics", "Joint inflammation"),
        Medication("Naproxen", 2, "Orthopedics", "Arthritis pain"),
        Medication("Celecoxib", 1, "Orthopedics", "Chronic joint pain"),
        Medication("Tramadol", 2, "Orthopedics", "Moderate pain"),
        Medication("Paracetamol", 3, "Orthopedics", "Mild pain"),
        Medication("Meloxicam", 1, "Orthopedics", "Osteoarthritis"),
        Medication("Etodolac", 2, "Orthopedics", "Inflammation"),
        Medication("Methocarbamol", 2, "Orthopedics", "Muscle spasms"),
        Medication("Tizanidine", 1, "Orthopedics", "Muscle relaxation"),
        Medication("Glucosamine", 1, "Orthopedics", "Joint support"),
        Medication("CalciumD3", 1, "Orthopedics", "Bone strength"),

        # ---------- Dermatology ----------
        Medication("Hydrocortisone", 2, "Dermatology", "Skin inflammation"),
        Medication("Betamethasone", 1, "Dermatology", "Severe dermatitis"),
        Medication("Clotrimazole", 2, "Dermatology", "Fungal infections"),
        Medication("Ketoconazole", 1, "Dermatology", "Scalp treatment"),
        Medication("Isotretinoin", 1, "Dermatology", "Severe acne"),
        Medication("Tretinoin", 1, "Dermatology", "Acne and wrinkles"),
        Medication("Adapalene", 1, "Dermatology", "Acne treatment"),
        Medication("Mupirocin", 3, "Dermatology", "Bacterial skin infection"),
        Medication("ErythromycinGel", 2, "Dermatology", "Acne antibiotic"),
        Medication("Tacrolimus", 2, "Dermatology", "Eczema treatment"),
        Medication("Calcipotriol", 1, "Dermatology", "Psoriasis treatment"),
        Medication("UreaCream", 1, "Dermatology", "Dry skin repair"),
    ]



def main():

    # defining preliminary users
    # fullName(str), id(str), age(int), height(int), weight(int), speciality(str), password(str)
    doc1 = Doctor("Eden Vilinsky", "11", 28, 183, 78, "Neurology", "11")
    doc2 = Doctor("Guy Marcus", "22", 30, 178, 74, "Cardiology", "22")
    doc3 = Doctor("Omry Hemo", "333333333", 34, 175, 70, "Orthopedics", "bone_doc")
    doc4 = Doctor("Almog Malka", "444444444", 26, 164, 62, "Dermatology", "skin_on_skin")

    # add new doctors to doctors database
    doctorList.append(doc1)
    doctorList.append(doc2)
    doctorList.append(doc3)
    doctorList.append(doc4)

    # add doctors names to list of doctors names for drop down menues
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

    # add patient to patients database
    patientList.append(pat1)
    patientList.append(pat2)
    patientList.append(pat3)
    patientList.append(pat4)

    # define preliminary treatments and register treatments to both treating doctor and treated patients
    # treatName(str), treatReason(str), treatArea(str), Doctor(Doctor), Patient(Patient)
    treat1 = Treatment("Ablation (burning)", "Heart arrhythmias", "Left side of chest", doc2, pat1)
    pat1.addTreat(treat1)
    doc2.addTreat(treat1)
    treat2 = Treatment("Cast on shin to fixate bone", "Broken bone in shin", "Right leg", doc3, pat2)
    pat2.addTreat(treat2)
    doc3.addTreat(treat2)
    treat3 = Treatment("Annual checkup", "Risk group", "Full body", doc4, pat3)
    pat3.addTreat(treat3)
    doc4.addTreat(treat3)
    treat4 = Treatment("Final confirmation", "HNPP", "Nervous system", doc1, pat4)
    pat4.addTreat(treat4)
    doc1.addTreat(treat4)

    # add treatments to treatments database
    treatmentList.append(treat1)
    treatmentList.append(treat2)
    treatmentList.append(treat3)
    treatmentList.append(treat4)

    # create Medication database
    global medicationList
    medicationList = init_medications()

    ######################################################################## end of preliminary definitions and beginning of login page definition

    # login page definition (SINGLE WINDOW)
    root = tk.Tk()
    root.title("Clinic System")
    root.geometry("600x500+10+20")
    root.configure(bg="white")

    # two screens in same window
    login_frame = tk.Frame(root, bg="white")
    home_frame = tk.Frame(root, bg="light grey")

    login_frame.pack(fill="both", expand=True)

    # login page design
    script_dir = os.path.dirname(__file__)
    image_path = os.path.join(script_dir, "LoginPage_image.png")
    logimg = Image.open(image_path)
    logimg = logimg.resize((220, 220))
    welcome_logo = ImageTk.PhotoImage(logimg)
    img_label = tk.Label(login_frame, image=welcome_logo, borderwidth=0, bg="white")
    img_label.image = welcome_logo
    img_label.place(x=150, y=20)

    # request doctor ID and placing
    DocId = tk.Label(login_frame, text="Doctor ID", bg="light blue", fg="black")
    DocId.place(x=100, y=300)
    DocEnt = tk.Entry(login_frame, bg="light blue", fg="black", font=("Arial", 12))
    DocEnt.place(x=200, y=300)

    # request doctor personal password and placing
    DocPass = tk.Label(login_frame, text="Password", bg="light blue", fg="black")
    DocPass.place(x=100, y=340)
    PassEnt = tk.Entry(login_frame, bg="light blue", fg="black", font=("Arial", 12), show="*")
    PassEnt.place(x=200, y=340)

    # screen navigation
    def show_login():
        home_frame.pack_forget()
        login_frame.pack(fill="both", expand=True)
        DocEnt.delete(0, tk.END)
        PassEnt.delete(0, tk.END)

    def show_home(doct):
        login_frame.pack_forget()
        home_frame.pack(fill="both", expand=True)
        build_home_screen(doct, home_frame, show_login)

    # entry button
    EntButton = tk.Button(
        login_frame,
        text="Enter",
        bg="light green",
        fg="black",
        font=("Arial", 12, "bold"),
        command=lambda: try_login(DocEnt.get(), PassEnt.get(), show_home)
    )
    EntButton.place(x=220, y=400)

    root.mainloop()


if __name__ == "__main__":
    main()
