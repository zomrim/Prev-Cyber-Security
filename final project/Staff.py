class Staff:
    def __init__(self, employee_id, salary):
        self.employee_id = employee_id
        self.salary = salary

    # פונקציה לוגית 1
    def give_raise(self, percentage):
        self.salary = self.salary * (1 + percentage / 100)

    # פונקציה לוגית 2
    def get_annual_salary(self):
        return self.salary * 12