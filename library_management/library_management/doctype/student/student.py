import frappe
from frappe.model.document import Document

class Student(Document):
    def validate(self):
        self.cleanup_rows()
        self.calculate_result()

    def cleanup_rows(self):
        """Remove subject rows that have no subject name."""
        valid_rows = []
        for row in self.subjects:
            if row.subject_name:
                valid_rows.append(row)
        self.subjects = valid_rows
        
    def calculate_result(self):
        obtained_marks = 0
        subject_count = len(self.subjects or [])
        for row in self.subjects:
            obtained_marks += row.marks or 0
        total_marks = subject_count * 100
        self.total_marks = total_marks
        self.maximum_marks = obtained_marks  
        if total_marks > 0:
            self.percentage = round((obtained_marks / total_marks) * 100, 2)
        else:
            self.percentage = 0

        if self.percentage < 33:
            self.status = "Failed"
        elif self.percentage <= 50:
            self.status = "Pass"
        else:
            self.status = "Excellent"
