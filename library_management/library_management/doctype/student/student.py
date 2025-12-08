import frappe
from frappe.model.document import Document

class Student(Document):
    def validate(self):
        self.calculate_result()

    def calculate_result(self):
        total_marks = 0
        subject_count = 0
        if self.subjects:
            for row in self.subjects:
                total_marks += row.marks
                subject_count += 1
        self.total_marks = subject_count * 100           
        self.maximum_marks = total_marks                 

        if self.total_marks > 0:
            self.percentage = round((total_marks / self.total_marks) * 100, 2)
        else:
            self.percentage = 0

        if self.percentage < 33:
            self.status = "Failed"
        elif 33 <= self.percentage <= 50:
            self.status = "Pass"
        else:
            self.status = "Excellent"
