from Human import *

class Patient(Human):

    # Patient attributes
    sensitivityL = []
    treatHistory = []

    # attributes are lists that are defined in the initialize function
    # full initialize method
    def __init__(self, fullName, id, age, height, weight):
        super().__init__(fullName, id, age, height, weight) # call parent function (Human)
        self.sensitivityL = [None]
        self.treatHistory = [None]

    # adding a treatment to patient medical history (treatment has already been done)
    def addTreat(self,newTreatment):
        self.treatHistory.append(newTreatment)

    # adding a new sensitivity that has been discovered
    def addS(self, newSensitivity):
        self.sensitivityL.append(newSensitivity)

# remove sensitiviy