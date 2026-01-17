from Human import *

class Patient(Human):

    # Patient attributes
    sensitivityL = []
    treatHistory = []
    medications = []

    # attributes are lists that are defined in the initialize function
    # full initialize method
    def __init__(self, fullName, id, age, height, weight):
        super().__init__(fullName, id, age, height, weight) # call parent function (Human)
        self.sensitivityL = []
        self.treatHistory = []
        self.medications = []

    # adding a treatment to patient medical history (treatment has already been done)
    def addTreat(self,newTreatment):
        self.treatHistory.append(newTreatment)

    # adding a new sensitivity that has been discovered
    def addS(self, newSensitivity):
        self.sensitivityL.append(newSensitivity)

    def addMedication(self, med):
        self.medications.append(med)

    def removeSensitivity(self, sensitivity):
        self.sensitivityL.remove(sensitivity)