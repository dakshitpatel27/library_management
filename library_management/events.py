# apps/library_management/library_management/events.py
import frappe

def student_validate(doc, method=None):
    """
    Calculate total marks, percentage and set status.
    - If child row has `max_marks` use it.
    - Otherwise assume default_max_per_subject (100).
    """
    default_max_per_subject = 100

    total_obtained = 0
    max_total = 0

    # `doc.subjects` is a list of child Document objects
    for row in doc.get("subjects") or []:
        # safe access for marks (0 if missing or falsy)
        try:
            marks = float(row.get("marks") or 0)
        except Exception:
            # fallback if row.marks is not convertible
            marks = 0.0

        # prefer explicit field; fallback to default
        # use getattr row.get() style for child row Document
        max_marks = None
        if hasattr(row, "max_marks"):
            max_marks = row.get("max_marks")
        elif row.get("max_marks") is not None:
            max_marks = row.get("max_marks")

        try:
            max_marks = float(max_marks) if max_marks is not None else default_max_per_subject
        except Exception:
            max_marks = default_max_per_subject

        total_obtained += marks
        max_total += max_marks

    percentage = (total_obtained / max_total * 100) if max_total else 0.0

    # set status based on percentage
    if percentage < 40:
        doc.status = "Failed"
    elif percentage >= 85:
        doc.status = "Excellent"
    else:
        doc.status = "Pass"

    # Optionally set computed fields on doc
    doc.total_obtained = total_obtained
    doc.max_total = max_total
    doc.percentage = round(percentage, 2)
