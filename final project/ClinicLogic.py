from Doctor import Doctor
from Medication import Medication
from Patient import Patient
from Treatment import Treatment

class ClinicSystem:
    def __init__(self):
        # רשימות (Lists) - דרישת חובה
        self.doctorList = []
        self.treatmentList = []
        self.medicationList = []
        
        # מילון (Dict) - דרישת חובה (מיפוי ת"ז -> אובייקט מטופל)
        self.patients_dict = {} 

        self.init_system_data()

    def init_system_data(self):
        # 1. Doctors
        doc1 = Doctor("Eden Vilinsky", "11", 28, 183, 78, "Neurology", "11", "D001", 15000)
        doc2 = Doctor("Guy Marcus", "22", 30, 178, 74, "Cardiology", "22", "D002", 16000)
        doc3 = Doctor("Omry Hemo", "333333333", 34, 175, 70, "Orthopedics", "bone_doc", "D003", 17000)
        doc4 = Doctor("Almog Malka", "444444444", 26, 164, 62, "Dermatology", "skin_on_skin", "D004", 18000)
        self.doctorList.extend([doc1, doc2, doc3, doc4])

        # 2. Patients (Using Dict for storage)
        pat1 = Patient("Eitan Vinograd", "123456789", 59, 190, 98)
        pat2 = Patient("Stav Levi", "234567891", 37, 173, 70)
        pat3 = Patient("Liel Ben David", "345678912", 42, 165, 63)
        pat4 = Patient("Eliran Keren", "456789123", 48, 197, 95)
        
        # שמירה במילון לפי תעודת זהות
        self.patients_dict[pat1.id] = pat1
        self.patients_dict[pat2.id] = pat2
        self.patients_dict[pat3.id] = pat3
        self.patients_dict[pat4.id] = pat4

        # 3. Medications
        self.medicationList = [
            Medication("Gabapentin", 3, "Neurology", "Nerve pain"),
            Medication("Aspirin", 1, "Cardiology", "Blood thinner"),
            Medication("Ibuprofen", 3, "Orthopedics", "Pain"),
            Medication("Hydrocortisone", 2, "Dermatology", "Inflammation"),
        ]

        # 4. Treatments
        t1 = Treatment("Ablation", "Arrhythmias", "Chest", doc2, pat1)
        pat1.addTreat(t1); doc2.addTreat(t1)
        
        t2 = Treatment("Cast", "Broken Bone", "Leg", doc3, pat2)
        pat2.addTreat(t2); doc3.addTreat(t2)
        
        t3 = Treatment("Checkup", "Routine", "Full Body", doc4, pat3)
        pat3.addTreat(t3); doc4.addTreat(t3)
        
        t4 = Treatment("Final Check", "HNPP", "Nervous Sys", doc1, pat4)
        pat4.addTreat(t4); doc1.addTreat(t4)
        
        self.treatmentList.extend([t1, t2, t3, t4])

    # --- פונקציות גישה ---

    def get_all_patients(self):
        return list(self.patients_dict.values()) # המרה ממילון לרשימה לתצוגה

    def verify_login(self, id_val, pass_val):
        for doc in self.doctorList:
            if doc.id == id_val and doc.password == pass_val:
                return doc
        return None

    def create_new_patient(self, name, pid, age, height, weight):
        if not name or not pid or not str(age):
            return False, "All fields required"
        
        # בדיקה במילון (יעיל יותר)
        if pid in self.patients_dict:
            return False, "ID already exists"
        
        try:
            new_p = Patient(name, pid, int(age), int(height), int(weight))
            self.patients_dict[pid] = new_p # הוספה למילון
            return True, "Patient added"
        except ValueError:
            return False, "Invalid numbers"

    def add_treatment(self, name, reason, area, doctor, patient_name):
        # חיפוש מטופל לפי שם (רץ על ערכי המילון)
        patient = next((p for p in self.patients_dict.values() if p.fullName == patient_name), None)
        if not patient:
            return False, "Patient not found"
            
        t = Treatment(name, reason, area, doctor, patient)
        patient.addTreat(t)
        doctor.addTreat(t)
        self.treatmentList.append(t)
        return True, "Treatment saved"

    def issue_prescription(self, doctor, patient_name, med_name):
        # מציאת התרופה
        med = next((m for m in self.medicationList if m.MedName == med_name), None)
        # מציאת המטופל
        patient = next((p for p in self.patients_dict.values() if p.fullName == patient_name), None)

        if not med or not patient:
            return False, "Invalid Selection"

        if med.can_be_issued_by(doctor):
            # עדכון אובייקט המטופל (שמירת המרשם)
            patient.addMedication(med)
            return True, f"Prescribed {med.MedName}"
        
        return False, "Authorization Error"

# יצירת המופע היחיד של המערכת (Singleton) לשימוש ב-GUI
system_instance = ClinicSystem()