from datetime import datetime
from Doctor import Doctor
from Patient import Patient


class Treatment:

    # Treatment attributes
    TreatNum = 0
    TreatName = ""
    TreatReason = ""
    TreatArea = ""
    TreatDate = ""
    Doctor : Doctor
    #PatientID = ""
    Patient : Patient


    # treatment methods
    # full initialize
    def __init__(self,treatName, treatReason, treatArea, Doc: Doctor, pat : Patient):
        self.TreatNum += 1
        self.TreatName = treatName
        self.treatReason = treatReason
        self.treatArea = treatArea
        self.treatDate = datetime.now() # using datetime library
        self.Doctor = Doc
        self.Patient = pat


    # print method
    def __str__(self):
        return ("treatment name: " + self.TreatName + ", reason for treatment: " + self.TreatReason +
                ", limb or area that received treatment: " + self.TreatArea + ", treatment Date: " + self.TreatDate +
                ", name of doctor: " + self.Doctor.fullName + ", patient name: " + self.Patient.fullName)
