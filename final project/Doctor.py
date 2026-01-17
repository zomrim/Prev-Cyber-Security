from Patient import Patient
from Staff import Staff

class Doctor(Patient, Staff):

    # Doctor attributes
    speciality = ""
    isActive = True
    treatNum = 0
    treatHistory = []
    password = ""

    # full initialize method
    def __init__(self,fullName, id, age, height, weight, speciality, password, employee_id, salary):
        Patient.__init__(self, fullName, id, age, height, weight)
        Staff.__init__(self, employee_id, salary)
        self.speciality = speciality
        self.isActive = True
        self.treatHistory = []
        self.treatNum = 0
        self.password = password

    # doctor adds treatment to his treating history.
    def addTreat(self,newTreatment):
        self.treatHistory.append(newTreatment)
        self.treatNum = self.treatNum + 1

    # change isActive status in case doctor is not present in the hospital
    def absent(self):
        self.isActive = False

    # change isActive status in case doctor has arrived back to the hospital
    def arrived(self):
        self.isActive = True

    # in case there is suspicion that password has been leaked
    def changePassword(self,newPassword):
        self.password = newPassword

