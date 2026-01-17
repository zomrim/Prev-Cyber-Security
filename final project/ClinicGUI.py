import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import ClinicLogic as logic

# --- UI Constants ---
FONT_MAIN = ("Sans Serif", 10)
FONT_HEADER = ("Sans Serif", 14, "bold")
FONT_TITLE = ("Sans Serif", 18, "bold")
FONT_BUTTON = ("Sans Serif", 11, "bold")
COLOR_BG = "#ecf0f1"
COLOR_SIDEBAR = "#2c3e50"
COLOR_ACCENT = "#3498db"
COLOR_WHITE = "white"

class ClinicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clinic System")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(".", font=FONT_MAIN)
        self.style.configure("TEntry", padding=5, relief="flat", fieldbackground="#F0F2F5")
        self.style.configure("TCombobox", padding=5)
        self.style.configure("Treeview", font=FONT_MAIN, rowheight=25)
        self.style.configure("Treeview.Heading", font=("Sans Serif", 11, "bold"))

        self.current_user = None # Will hold the logged-in Doctor

        # Container for screens
        self.container = tk.Frame(self, bg=COLOR_BG)
        self.container.pack(fill="both", expand=True)

        self.show_login_screen()

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # =========================================================================
    # 1. LOGIN SCREEN
    # =========================================================================
    def show_login_screen(self):
        self.clear_screen()
        self.container.configure(bg=COLOR_WHITE)

        login_box = tk.Frame(self.container, bg=COLOR_WHITE, padx=40, pady=40)
        login_box.place(relx=0.5, rely=0.5, anchor="center")

        # Logo Image (Optional with try/except)
        try:
            script_dir = os.path.dirname(__file__)
            image_path = os.path.join(script_dir, "LoginPage_image.png")
            logimg = Image.open(image_path).resize((150, 150))
            self.logo_photo = ImageTk.PhotoImage(logimg) # Keep reference
            tk.Label(login_box, image=self.logo_photo, bg=COLOR_WHITE).pack(pady=(0, 20))
        except Exception:
            pass

        tk.Label(login_box, text="Sign In", font=("Sans Serif", 24, "bold"), 
                 bg=COLOR_WHITE, fg=COLOR_SIDEBAR).pack(pady=(0, 30))

        # Inputs
        input_frame = tk.Frame(login_box, bg=COLOR_WHITE)
        input_frame.pack(fill="x")
        input_frame.columnconfigure(1, weight=1)

        tk.Label(input_frame, text="Doctor ID", bg=COLOR_WHITE, fg="#7f8c8d", font=FONT_MAIN).grid(row=0, column=0, sticky="w", pady=5)
        id_ent = ttk.Entry(input_frame, font=("Sans Serif", 11))
        id_ent.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        tk.Label(input_frame, text="Password", bg=COLOR_WHITE, fg="#7f8c8d", font=FONT_MAIN).grid(row=2, column=0, sticky="w", pady=5)
        pass_ent = ttk.Entry(input_frame, show="*", font=("Sans Serif", 11))
        pass_ent.grid(row=3, column=0, sticky="ew", pady=(0, 20))

        def attempt_login(event=None):
            user = logic.system_instance.verify_login(id_ent.get(), pass_ent.get())
            if user:
                self.current_user = user
                self.build_dashboard_layout()
            else:
                messagebox.showerror("Error", "Invalid ID or Password")
        
        self.bind('<Return>', attempt_login)

        tk.Button(input_frame, text="Login", bg=COLOR_ACCENT, fg="white", 
                  font=("Sans Serif", 12, "bold"), relief="flat", cursor="hand2",
                  command=attempt_login).grid(row=4, column=0, sticky="ew", pady=10)

    # =========================================================================
    # 2. DASHBOARD LAYOUT (Sidebar + Content)
    # =========================================================================
    def build_dashboard_layout(self):
        self.clear_screen()
        self.container.configure(bg=COLOR_BG)

        # --- Header ---
        header = tk.Frame(self.container, bg=COLOR_WHITE, height=60)
        header.pack(side="top", fill="x")
        tk.Frame(self.container, bg="#bdc3c7", height=1).pack(side="top", fill="x") # Shadow line

        tk.Label(header, text="Medical Portal", font=FONT_HEADER, bg=COLOR_WHITE, fg=COLOR_SIDEBAR).pack(side="left", padx=20)
        tk.Label(header, text=f"Dr. {self.current_user.fullName}", font=("Sans Serif", 12), bg=COLOR_WHITE, fg="#7f8c8d").pack(side="right", padx=20)

        # --- Main Layout ---
        main_area = tk.Frame(self.container, bg=COLOR_BG)
        main_area.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(main_area, bg=COLOR_SIDEBAR, width=220)
        sidebar.pack(side="right", fill="y")
        sidebar.pack_propagate(False)

        # Content Area
        self.content_frame = tk.Frame(main_area, bg=COLOR_BG)
        self.content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # --- Sidebar Buttons ---
        def menu_btn(txt, cmd):
            tk.Button(sidebar, text=txt, font=FONT_BUTTON, bg=COLOR_SIDEBAR, fg="white",
                      activebackground="#34495e", activeforeground="white", bd=0, relief="flat",
                      cursor="hand2", anchor="w", padx=20, pady=10, command=cmd).pack(fill="x", pady=2)

        menu_btn("Dashboard", self.view_dashboard)
        menu_btn("Add Treatment", self.view_add_treatment)
        menu_btn("History", self.view_history)
        menu_btn("Patients List", self.view_patients)
        menu_btn("New Patient", self.view_new_patient)
        menu_btn("Prescribe Meds", self.view_prescribe_meds)  # <--- הוסף שורה זו
        
        tk.Frame(sidebar, bg="#34495e", height=1).pack(fill="x", pady=20)
        menu_btn("Personal Details", self.view_profile)
        
        tk.Button(sidebar, text="Log Out", font=FONT_BUTTON, bg="#c0392b", fg="white",
                  relief="flat", cursor="hand2", command=self.confirm_logout).pack(side="bottom", fill="x", padx=20, pady=20)
        
        # Start on Dashboard
        self.view_dashboard()

    # =========================================================================
    # NEW FUNCTION: LOGOUT CONFIRMATION
    # =========================================================================
    def confirm_logout(self):
        answer = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if answer:
            self.show_login_screen()

    # =========================================================================
    # VIEWS
    # =========================================================================
    def clear_content(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

    def view_dashboard(self):
        self.clear_content()
        
        # Calculate stats
        my_treatments = [t for t in logic.system_instance.treatmentList if t.Doctor == self.current_user]
        today = datetime.now().date()
        today_count = sum(1 for t in my_treatments if t.TreatDate.date() == today)
        
        treated_ids = {t.Patient.id for t in my_treatments}
        waiting_count = sum(1 for p in logic.system_instance.get_all_patients() if p.id not in treated_ids)

        last_activity = "None"
        if my_treatments:
            last_t = max(my_treatments, key=lambda x: x.TreatDate)
            last_activity = f"{last_t.TreatDate.strftime('%d/%m')}\n{last_t.Patient.fullName}"

        # Title
        tk.Label(self.content_frame, text="Control Panel", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_SIDEBAR).pack(anchor="w", pady=(0, 20))

        # Grid Cards
        grid = tk.Frame(self.content_frame, bg=COLOR_BG)
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1); grid.columnconfigure(1, weight=1)

        def make_card(r, c, title, val, accent):
            f = tk.Frame(grid, bg="white", highlightbackground="#d1d5db", highlightthickness=1)
            f.grid(row=r, column=c, sticky="ew", padx=10, pady=10, ipady=10)
            tk.Frame(f, bg=accent, width=5).pack(side="left", fill="y")
            tk.Label(f, text=title, font=("Sans Serif", 11, "bold"), fg="#95a5a6", bg="white").pack(anchor="w", padx=15)
            tk.Label(f, text=val, font=("Sans Serif", 22, "bold"), fg=COLOR_SIDEBAR, bg="white").pack(anchor="w", padx=15)

        make_card(0, 0, "Treatments Today", str(today_count), COLOR_ACCENT)
        make_card(0, 1, "My Patients", str(len(treated_ids)), COLOR_ACCENT)
        make_card(1, 0, "Not Treated Yet", str(waiting_count), "#e67e22")
        make_card(1, 1, "Last Activity", last_activity, "#27ae60")

        # Recent Treatments
        tk.Label(self.content_frame, text="Recent Treatments (Last 5)", font=("Sans Serif", 12, "bold"), 
                 bg=COLOR_BG, fg=COLOR_SIDEBAR).pack(anchor="w", pady=(30, 10))

        recent_frame = tk.Frame(self.content_frame, bg=COLOR_BG)
        recent_frame.pack(fill="both", expand=True)

        recent = sorted(my_treatments, key=lambda x: x.TreatDate, reverse=True)[:5]
        if not recent:
            tk.Label(recent_frame, text="No treatments yet.", bg=COLOR_BG, font=("Sans Serif", 10)).pack(anchor="w")
        else:
            for t in recent:
                c = tk.Frame(recent_frame, bg="white", pady=10, padx=10)
            c.pack(fill="x", pady=5)
            tk.Label(c, text=t.TreatDate.strftime('%d/%m/%Y'), font=("Sans Serif", 10, "bold"), fg="#7f8c8d", bg="white").pack(anchor="w")
            tk.Label(c, text=f"{t.TreatName} - {t.Patient.fullName}", font=("Sans Serif", 12, "bold"), bg="white").pack(anchor="w")
            tk.Label(c, text=f"Reason: {t.TreatReason} | Area: {t.TreatArea}", font=("Sans Serif", 11), bg="white").pack(anchor="w")

    def view_add_treatment(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Add New Treatment", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_SIDEBAR).pack(anchor="w", pady=(0, 20))
        
        form = tk.Frame(self.content_frame, bg="white", padx=30, pady=30)
        form.pack(fill="both", expand=True)
        form.columnconfigure(1, weight=1)

        tk.Label(form, text="Patient:", bg="white", font=FONT_MAIN).grid(row=0, column=0, sticky="w", pady=10)
        pat_var = tk.StringVar()
        pat_cb = ttk.Combobox(form, textvariable=pat_var, values=[p.fullName for p in logic.system_instance.get_all_patients()], state="readonly", font=("Sans Serif", 11))
        pat_cb.grid(row=0, column=1, sticky="ew", padx=10)

        entries = {}
        for i, label in enumerate(["Treatment Name", "Reason", "Area"], start=1):
            tk.Label(form, text=label+":", bg="white", font=FONT_MAIN).grid(row=i, column=0, sticky="w", pady=10)
            ent = ttk.Entry(form, font=("Sans Serif", 11))
            ent.grid(row=i, column=1, sticky="ew", padx=10)
            entries[label] = ent

        def save():
            success, msg = logic.system_instance.add_treatment(
                entries["Treatment Name"].get(), 
                entries["Reason"].get(), 
                entries["Area"].get(), 
                self.current_user, 
                pat_var.get()
            )
            if success:
                messagebox.showinfo("Success", msg)
                self.view_dashboard()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(form, text="Save", bg="#27ae60", fg="white", font=FONT_BUTTON, relief="flat", command=save).grid(row=4, column=1, sticky="e", pady=20, padx=10)

    def view_history(self):
        self.clear_content()
        tk.Label(self.content_frame, text="History", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_SIDEBAR).pack(anchor="w", pady=(0, 20))
        
        # Scrollable setup
        canvas = tk.Canvas(self.content_frame, bg=COLOR_BG, highlightthickness=0)
        scroll = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=COLOR_BG)
        
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw", width=canvas.winfo_reqwidth())
        # Auto-resize width
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas.find_withtag("all")[0], width=e.width))

        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        treatments = sorted([t for t in logic.system_instance.treatmentList if t.Doctor == self.current_user], key=lambda x: x.TreatDate, reverse=True)
        
        if not treatments:
            tk.Label(frame, text="No history available", bg=COLOR_BG).pack(pady=20)
        
        for t in treatments:
            c = tk.Frame(frame, bg="white", pady=10, padx=10)
            c.pack(fill="x", pady=5)
            tk.Label(c, text=t.TreatDate.strftime('%d/%m/%Y'), font=("Sans Serif", 10, "bold"), fg="#7f8c8d", bg="white").pack(anchor="w")
            tk.Label(c, text=f"{t.TreatName} - {t.Patient.fullName}", font=("Sans Serif", 11, "bold"), bg="white").pack(anchor="w")
            tk.Label(c, text=f"Reason: {t.TreatReason} | Area: {t.TreatArea}", font=("Sans Serif", 10), bg="white").pack(anchor="w")

    def view_patients(self):
        self.clear_content()
        tk.Label(self.content_frame, text="My Patients", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_SIDEBAR).pack(anchor="w", pady=(0, 20))
        
        # Scrollable area setup
        canvas = tk.Canvas(self.content_frame, bg=COLOR_BG, highlightthickness=0)
        scroll = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        cards_container = tk.Frame(canvas, bg=COLOR_BG)
        
        cards_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=cards_container, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas.find_withtag("all")[0], width=e.width))

        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Logic to get patients (all patients or filtered by doctor)
        # Using patients treated by doctor as per original logic, 
        # OR use logic.system_instance.get_all_patients() to see everyone.
        # Let's show patients who have a history with this doctor:
        my_pats_set = {t.Patient for t in logic.system_instance.treatmentList if t.Doctor == self.current_user}
        my_pats_list = list(my_pats_set)

        if not my_pats_list:
            tk.Label(cards_container, text="No patients linked to you found.", bg=COLOR_BG, font=FONT_MAIN).pack(pady=20)
            return

        for p in my_pats_list:
            # Create a Card Frame
            card = tk.Frame(cards_container, bg="white", bd=2, relief="raised")
            card.pack(fill="x", padx=10, pady=5, ipady=5)

            # Left side: Basic Info
            info_frame = tk.Frame(card, bg="white")
            info_frame.pack(side="left", fill="both", expand=True, padx=10)
            
            tk.Label(info_frame, text=p.fullName, font=("Sans Serif", 12, "bold"), fg=COLOR_SIDEBAR, bg="white").pack(anchor="w")
            tk.Label(info_frame, text=f"ID: {p.id}", font=("Sans Serif", 10), fg="gray", bg="white").pack(anchor="w")

            # Right side: Button
            btn_frame = tk.Frame(card, bg="white")
            btn_frame.pack(side="right", padx=10)
            
            # כפתור אחיד
            tk.Button(btn_frame, text="View Details", bg=COLOR_ACCENT, fg="white", 
                      font=("Sans Serif", 10, "bold"), relief="flat", padx=10, pady=5,
                      command=lambda pat=p: self.open_patient_details(pat)).pack()

    def open_patient_details(self, patient):
        # Create a Toplevel window (Popup)
        detail_win = tk.Toplevel(self)
        detail_win.title(f"Details: {patient.fullName}")
        detail_win.geometry("400x500")
        detail_win.configure(bg="white")

        tk.Label(detail_win, text=patient.fullName, font=FONT_TITLE, bg="white", fg=COLOR_SIDEBAR).pack(pady=(20, 5))
        tk.Label(detail_win, text=f"ID: {patient.id}", font=FONT_MAIN, bg="white", fg="gray").pack(pady=(0, 20))

        # Physical Stats
        stats_frame = tk.Frame(detail_win, bg="#F0F2F5", padx=10, pady=10)
        stats_frame.pack(fill="x", padx=20)
        
        tk.Label(stats_frame, text=f"Age: {patient.age}", bg="#F0F2F5", font=FONT_MAIN).pack(anchor="w")
        tk.Label(stats_frame, text=f"Height: {patient.height} cm", bg="#F0F2F5", font=FONT_MAIN).pack(anchor="w")
        tk.Label(stats_frame, text=f"Weight: {patient.weight} kg", bg="#F0F2F5", font=FONT_MAIN).pack(anchor="w")

        # Medications List
        tk.Label(detail_win, text="Medications / Prescriptions", font=("Sans Serif", 12, "bold"), bg="white", fg=COLOR_ACCENT).pack(anchor="w", padx=20, pady=(20, 5))
        
        med_frame = tk.Frame(detail_win, bg="white")
        med_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        if not patient.medications:
            tk.Label(med_frame, text="No active medications.", bg="white", font=FONT_MAIN, fg="gray").pack(anchor="w")
        else:
            for med in patient.medications:
                # Assuming med is a Medication object
                m_txt = f"• {med.MedName} ({med.MedDaily}/day)"
                tk.Label(med_frame, text=m_txt, bg="white", font=FONT_MAIN).pack(anchor="w")

        tk.Button(detail_win, text="Close", command=detail_win.destroy, bg="#c0392b", fg="white").pack(pady=10)

    def view_new_patient(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Register Patient", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_SIDEBAR).pack(anchor="w", pady=(0, 20))
        
        form = tk.Frame(self.content_frame, bg="white", padx=30, pady=30)
        form.pack(fill="both", expand=True)
        form.columnconfigure(1, weight=1)
        
        entries = {}
        fields = [("Full Name", "name"), ("ID", "id"), ("Age", "age"), ("Height", "h"), ("Weight", "w")]
        for i, (txt, key) in enumerate(fields):
            tk.Label(form, text=txt, bg="white", font=FONT_MAIN).grid(row=i, column=0, sticky="w", pady=10)
            ent = ttk.Entry(form, font=("Sans Serif", 11))
            ent.grid(row=i, column=1, sticky="ew", padx=10)
            entries[key] = ent
            
        def save():
            success, msg = logic.system_instance.create_new_patient(
                entries["name"].get(), entries["id"].get(), entries["age"].get(),
                entries["h"].get(), entries["w"].get()
            )
            if success:
                messagebox.showinfo("Success", msg)
                for e in entries.values(): e.delete(0, tk.END)
            else:
                messagebox.showerror("Error", msg)
                
        tk.Button(form, text="Register", bg="#27ae60", fg="white", font=("Sans Serif", 11, "bold"), relief="flat", command=save).grid(row=5, column=1, sticky="e", pady=20, padx=10)

    def view_prescribe_meds(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Prescribe Medication", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_SIDEBAR).pack(anchor="w", pady=(0, 20))

        form = tk.Frame(self.content_frame, bg="white", padx=30, pady=30)
        form.pack(fill="both", expand=True)
        form.columnconfigure(1, weight=1)

        # Patient Selection
        tk.Label(form, text="Select Patient", bg="white", font=("Sans Serif", 10)).grid(row=0, column=0, sticky="w", pady=10)
        pat_var = tk.StringVar()
        pats = [p.fullName for p in logic.system_instance.get_all_patients()]
        pat_cb = ttk.Combobox(form, textvariable=pat_var, values=pats, state="readonly", font=("Sans Serif", 11))
        pat_cb.grid(row=0, column=1, sticky="ew", padx=10)

        # Medication Selection
        tk.Label(form, text="Select Medication", bg="white", font=("Sans Serif", 10)).grid(row=1, column=0, sticky="w", pady=10)
        med_var = tk.StringVar()
        meds = [m.MedName for m in logic.system_instance.medicationList]
        med_cb = ttk.Combobox(form, textvariable=med_var, values=meds, state="readonly", font=("Sans Serif", 11))
        med_cb.grid(row=1, column=1, sticky="ew", padx=10)

        def prescribe():
            success, msg = logic.system_instance.issue_prescription(self.current_user, pat_var.get(), med_var.get())
            if success:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)

        tk.Button(form, text="Prescribe", bg="#3498db", fg="white", 
                font=("Sans Serif", 11, "bold"), relief="flat", command=prescribe).grid(row=2, column=1, sticky="e", pady=20, padx=10)

    def view_profile(self):
        self.clear_content()
        tk.Label(self.content_frame, text="My Profile", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_SIDEBAR).pack(anchor="w", pady=(0, 20))

        form = tk.Frame(self.content_frame, bg="white", padx=30, pady=30)
        form.pack(fill="both", expand=True)
        form.columnconfigure(1, weight=1)

        # משתנים לעריכה
        doc = self.current_user
        
        # שדות לקריאה בלבד
        tk.Label(form, text=f"Name: {doc.fullName}", bg="white", font=("Sans Serif", 12, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(form, text=f"ID: {doc.id}", bg="white", font=("Sans Serif", 12)).grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(form, text=f"Speciality: {getattr(doc, 'speciality', 'N/A')}", bg="white", font=("Sans Serif", 12)).grid(row=2, column=0, sticky="w", pady=5)

        # שדות לעריכה
        tk.Frame(form, bg="#bdc3c7", height=1).grid(row=3, column=0, columnspan=2, sticky="ew", pady=15) # קו מפריד

        edit_vars = {
            "Age": tk.StringVar(value=str(doc.age)),
            "Height": tk.StringVar(value=str(doc.height)),
            "Weight": tk.StringVar(value=str(doc.weight))
        }

        row_idx = 4
        for label, var in edit_vars.items():
            tk.Label(form, text=label, bg="white", font=FONT_MAIN).grid(row=row_idx, column=0, sticky="w", pady=5)
            ttk.Entry(form, textvariable=var, font=FONT_MAIN).grid(row=row_idx, column=1, sticky="ew", padx=10)
            row_idx += 1

        # שינוי סיסמה
        tk.Frame(form, bg="#bdc3c7", height=1).grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=15)
        row_idx += 1
        
        pass_new = tk.StringVar()
        pass_con = tk.StringVar()

        tk.Label(form, text="New Password", bg="white", font=FONT_MAIN).grid(row=row_idx, column=0, sticky="w", pady=5)
        ttk.Entry(form, textvariable=pass_new, show="*", font=FONT_MAIN).grid(row=row_idx, column=1, sticky="ew", padx=10)
        row_idx += 1
        
        tk.Label(form, text="Confirm Password", bg="white", font=FONT_MAIN).grid(row=row_idx, column=0, sticky="w", pady=5)
        ttk.Entry(form, textvariable=pass_con, show="*", font=FONT_MAIN).grid(row=row_idx, column=1, sticky="ew", padx=10)
        row_idx += 1

        def save_changes():
            # שמירת נתונים פיזיים
            try:
                doc.age = int(edit_vars["Age"].get())
                doc.height = int(edit_vars["Height"].get())
                doc.weight = int(edit_vars["Weight"].get())
            except ValueError:
                messagebox.showerror("Error", "Age, Height, and Weight must be numbers")
                return

            # שמירת סיסמה אם הוזנה
            p1 = pass_new.get().strip()
            p2 = pass_con.get().strip()
            
            if p1 or p2:
                if p1 == p2:
                    doc.changePassword(p1) # שימוש בפונקציה של המחלקה Doctor
                    pass_new.set("")
                    pass_con.set("")
                else:
                    messagebox.showerror("Error", "Passwords do not match")
                    return

            messagebox.showinfo("Success", "Profile updated successfully!")

        tk.Button(form, text="Update Profile", bg="#27ae60", fg="white", 
                  font=FONT_BUTTON, relief="flat", command=save_changes).grid(row=row_idx, column=1, sticky="e", pady=20, padx=10)