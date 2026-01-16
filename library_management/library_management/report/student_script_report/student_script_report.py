# Copyright (c) 2025, Dakshit and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"fieldname": "student_id", "label": "Student ID", "fieldtype": "Data", "width": 120},
        {"fieldname": "student_name", "label": "Student Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "grade", "label": "Grade", "fieldtype": "Data", "width": 80},
        {"fieldname": "subject_name", "label": "Subject", "fieldtype": "Data", "width": 150},
        {"fieldname": "marks", "label": "Marks", "fieldtype": "Float", "width": 80},
        {"fieldname": "total_marks", "label": "Total Marks", "fieldtype": "Float", "width": 100},
        {"fieldname": "percentage", "label": "Percentage", "fieldtype": "Float", "width": 100},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("student"):
        conditions += " AND s.name = %(student)s"
        values["student"] = filters["student"]

    if filters.get("grade"):
        conditions += " AND s.grade = %(grade)s"
        values["grade"] = filters["grade"]

    if filters.get("status"):
        conditions += " AND s.status = %(status)s"
        values["status"] = filters["status"]

    query = f"""
        SELECT
            s.student_id,
            s.name1 AS student_name,
            s.grade,
            ss.subject_name,
            ss.marks,
            s.total_marks,
            s.status,
            ROUND((ss.marks / s.total_marks) * 100, 2) AS percentage
        FROM `tabStudent` s
        JOIN `tabStudent Subject` ss
            ON ss.parent = s.name
        WHERE s.docstatus < 2
        {conditions}
        ORDER BY s.name, ss.subject_name
    """

    return frappe.db.sql(query, values, as_dict=True)
