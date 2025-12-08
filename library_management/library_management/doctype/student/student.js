// Copyright (c) 2025, Dakshit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Student", {
    onload(frm) {
        frm.set_value("status", "Draft");
    },
    
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button("Show Summary", () => {
                frappe.msgprint(`Percentage: ${frm.doc.percentage}`);
            });
        }
    },

    validate(frm) {
        if (frm.doc.percentage > 100) {
            frappe.throw("Percentage cannot exceed 100");
        }
    },

    before_save(frm) {
        if (frm.doc.name) {
            frm.doc.name = frm.doc.name.trim();
        }
    },

    after_save(frm) {
        frappe.show_alert("Student saved successfully");
    },

});

// Child Table
frappe.ui.form.on("Student Subject", {
    marks(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (row.marks < 0 || row.marks > 100) {
            frappe.msgprint({
                title: "Invalid Marks",
                message: "Marks must be between 0 and 100.",
                indicator: "red"
            });
            row.marks = 0;
            frm.refresh_field("subjects");  
        }
    }
});
