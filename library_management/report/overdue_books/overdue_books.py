# Copyright (c) 2025, Dakshit and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data

import frappe
from frappe.utils import nowdate, getdate, date_diff

def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data

def get_columns():
    return [
        {"label": "Transaction", "fieldname": "name", "fieldtype": "Link", "options": "Library Transaction", "width": 140},
        {"label": "Member", "fieldname": "member", "fieldtype": "Link", "options": "Library Member", "width": 160},
        {"label": "Book", "fieldname": "book", "fieldtype": "Link", "options": "Library Book", "width": 160},
        {"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date", "width": 110},
        {"label": "Days Overdue", "fieldname": "days_overdue", "fieldtype": "Int", "width": 120},
        {"label": "Current Penalty", "fieldname": "penalty", "fieldtype": "Currency", "width": 120},
    ]

def get_data():
    today = getdate(nowdate())

    transactions = frappe.get_all(
        "Library Transaction",
        filters={
            "docstatus": 1,
            "transaction_type": "Issue",
            "return_date": ["is", "not set"],
            "due_date": ["<", today],
        },
        fields=["name", "member", "book", "due_date", "penalty"],
        order_by="due_date asc",
    )

    data = []
    for d in transactions:
        days_overdue = max(0, date_diff(today, d.due_date))
        data.append({
            "name": d.name,
            "member": d.member,
            "book": d.book,
            "due_date": d.due_date,
            "days_overdue": days_overdue,
            "penalty": d.penalty,
        })

    return data
