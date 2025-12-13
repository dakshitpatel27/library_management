import frappe

def student_validate(doc, method=None):
    obtained = 0
    for row in doc.get("subjects") or []:
        try:
            marks = float(row.get("marks") or 0)
        except Exception:
            marks = 0
        obtained += marks
    total_marks = 100
    percentage = (obtained / total_marks) * 100 if total_marks else 0
    doc.total_marks = total_marks
    doc.obtained_marks = obtained
    doc.percentage = round(percentage, 2)
    if percentage < 40:
        doc.status = "Failed"
    elif percentage >= 85:
        doc.status = "Excellent"
    else:
        doc.status = "Pass"

def student_before_save(doc, method=None):
    obtained = 0
    for row in doc.get("subjects") or []:
        marks = float(row.get("marks") or 0)
        obtained += marks
    total_marks = 100
    percentage = (obtained / total_marks) * 100 if total_marks else 0
    doc.total_marks = total_marks
    doc.obtained_marks = obtained
    doc.percentage = round(percentage, 2)
    if percentage < 40:
        doc.status = "Failed"
    elif percentage >= 85:
        doc.status = "Excellent"
    else:
        doc.status = "Pass"

def customer_validate(doc, method):
    """
    Count customers in the same customer group and update field.
    """
    if doc.customer_group:
        count = frappe.db.count("Customer", {"customer_group": doc.customer_group})
        doc.customer_group_count = count  

def on_submit(doc, event):
    frappe.sendmail(
        recipients=["gajiparadakshit@gmail.com"], 
        subject=f"Student Created: {doc.student_name}",
        message=f"""
            A new student has been submitted.<br>
            Name: {doc.student_name}<br>
            Subject: {doc.subject}<br>
            Marks: {doc.marks}
        """
    )
