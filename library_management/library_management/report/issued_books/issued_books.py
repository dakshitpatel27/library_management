# Copyright (c) 2025, Dakshit and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data

def get_columns():
    return [
        {"label": "Transaction", "fieldname": "name", "fieldtype": "Link", "options": "Library Transaction", "width": 140},
        {"label": "Member", "fieldname": "member", "fieldtype": "Link", "options": "Library Member", "width": 160},
        {"label": "Book", "fieldname": "book", "fieldtype": "Link", "options": "Library Book", "width": 160},
        {"label": "Issue Date", "fieldname": "issue_date", "fieldtype": "Date", "width": 110},
        {"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date", "width": 110},
        {"label": "Return Date", "fieldname": "return_date", "fieldtype": "Date", "width": 110},
        {"label": "Penalty", "fieldname": "penalty", "fieldtype": "Currency", "width": 100},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 90},
    ]

def get_data(filters):
    conditions = {"docstatus": 1}
    if filters.get("member"):
        conditions["member"] = filters["member"]
    if filters.get("book"):
        conditions["book"] = filters["book"]

    records = frappe.get_all(
        "Library Transaction",
        filters=conditions,
        fields=["name", "member", "book", "issue_date", "due_date", "return_date", "penalty", "transaction_type"],
        order_by="issue_date desc",
    )

    data = []
    for d in records:
        if d.return_date:
            status = "Returned"
        elif d.transaction_type == "Issue":
            status = "Issued"
        else:
            status = d.transaction_type

        data.append({
            "name": d.name,
            "member": d.member,
            "book": d.book,
            "issue_date": d.issue_date,
            "due_date": d.due_date,
            "return_date": d.return_date,
            "penalty": d.penalty,
            "status": status,
        })

    return data
