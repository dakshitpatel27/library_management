# Copyright (c) 2026, Dakshit and contributors
# For license information, please see license.txt
import frappe

def execute(filters=None):
	columns = [
		{"label": "Book", "fieldname": "book", "fieldtype": "Link", "options": "Library Book"},
		{"label": "Member", "fieldname": "member", "fieldtype": "Link", "options": "Library Member"},
		{"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date"},
		{"label": "Days Overdue", "fieldname": "days_overdue", "fieldtype": "Int"},
	]

	data = frappe.db.sql("""
		SELECT
			book,
			member,
			due_date,
			DATEDIFF(CURDATE(), due_date) AS days_overdue
		FROM `tabLibrary Transaction`
		WHERE
			docstatus = 1
			AND due_date < CURDATE()
	""", as_dict=True)

	return columns, data
