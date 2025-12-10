# Copyright (c) 2025, Dakshit and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
import frappe

def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Member", "fieldname": "member", "fieldtype": "Link", "options": "Library Member", "width": 160},
        {"label": "Total Issues", "fieldname": "total_issues", "fieldtype": "Int", "width": 110},
        {"label": "Currently Issued", "fieldname": "active_issues", "fieldtype": "Int", "width": 130},
        {"label": "Total Penalty", "fieldname": "total_penalty", "fieldtype": "Currency", "width": 120},
    ]

def get_data(filters):
    # Optional filter by member
    member_filter = ""
    if filters.get("member"):
        member_filter = "AND member = %(member)s"

    data = frappe.db.sql(
        f"""
        SELECT
            member,
            COUNT(CASE WHEN transaction_type = 'Issue' THEN 1 END) AS total_issues,
            COUNT(
                CASE
                    WHEN transaction_type = 'Issue'
                    AND docstatus = 1
                    AND return_date IS NULL
                THEN 1 END
            ) AS active_issues,
            SUM(COALESCE(penalty, 0)) AS total_penalty
        FROM `tabLibrary Transaction`
        WHERE docstatus = 1
        {member_filter}
        GROUP BY member
        ORDER BY total_issues DESC
        """,
        filters,
        as_dict=True,
    )

    return data
