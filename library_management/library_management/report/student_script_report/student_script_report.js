// Copyright (c) 2025, Dakshit and contributors
// For license information, please see license.txt

frappe.query_reports["Student Script Report"] = {
    filters: [
        {
            fieldname: "student",
            label: "Student",
            fieldtype: "Link",
            options: "Student"
        },
        {
            fieldname: "grade",
            label: "Grade",
            fieldtype: "Data"
        },
        {
            fieldname: "status",
            label: "Status",
            fieldtype: "Select",
            options: "Failed\nPass\nExcellent"
        }
    ]
};

