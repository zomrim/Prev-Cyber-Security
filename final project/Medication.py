
class Medication:
    def __init__(self, MedName: str, MedDaily: int, MedDept: str, MedPurpos: str):
        self.MedName = MedName
        self.MedDaily = MedDaily
        self.MedDept = MedDept
        self.MedPurpos = MedPurpos

    def can_be_issued_by(self, doctor): # Check if the medication can be issued by the given doctor
        return doctor.speciality == self.MedDept

    def __str__(self):
        return (
            f"Name: {self.MedName}\n"
            f"Daily Dose: {self.MedDaily}\n"
            f"Department: {self.MedDept}\n"
            f"Purpose: {self.MedPurpos}"
        )

