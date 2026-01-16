import frappe
from frappe.model.document import Document

class Student(Document):
    def validate(self):
        self.cleanup_rows()
        self.calculate_result()

    def cleanup_rows(self):
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


#------------------------------------ Task Week 5&6 -------------------------------------------------

@frappe.whitelist()
def get_last_student_subjects():
    last_student = frappe.get_all("Student",fields=["name"],order_by="modified desc",limit=1)

    if not last_student:
        return []

    subjects = frappe.get_all("Student Subject",filters={"parent": last_student[0].name},fields=["subject_name"])

    return subjects

#------------------------------DATABASE API--------------------------------------------
@frappe.whitelist()
def get_active_student():
    count = frappe.db.count("Student",{'status':'Excellent'})
    if not count:
        return "GET_COUNT"
    return count

@frappe.whitelist()
def get_list():
    list1 = frappe.db.get_list('Student')
    if not list1:
        return "GET_LIST"
    return list1

@frappe.whitelist()
def get_all():
    all1 = frappe.db.get_all('Student')
    if not all1:
        return "GET_ALL"
    return all1

@frappe.whitelist()
def get_value():
    value1 = frappe.db.get_value('Student', 'STU-00001', 'name1')
    if not value1:
        return "GET_VALUE"
    return value1

@frappe.whitelist()
def get_single_value():
    svalue = frappe.db.get_single_value("System Settings", "setup_complete")
    if not svalue:
        return "GET_SINGLE_VALUE"
    return svalue

@frappe.whitelist()
def set_value():
    value2=frappe.db.set_value('Student','STU-00001','name1','New')
    if not value2:
        return "SET_VALUE"
    return value2

@frappe.whitelist()
def exists():
    exist1 =frappe.db.exists("Student", "STU-00001")
    if not exist1:
        return "NOT EXISTS"
    return exist1

#----------------------------Document API------------------------------------------



#-----------------------------REST API---------------------------------------------
#http://localhost:8000/api/method/library_management.library_management.doctype.student.student.get_current_user

@frappe.whitelist()
def get_current_user():
    return {
        "user": frappe.session.user,
        "roles": frappe.get_roles(frappe.session.user)
    }


