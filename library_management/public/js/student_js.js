frappe.ui.form.on("Student", {
    
    refresh: function (frm) {
        console.log("Student Doctype JS Loaded");
        frappe.msgprint("Student Form Loaded");
    }

});
