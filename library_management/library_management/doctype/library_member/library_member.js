frappe.ui.form.on("Library Member", {
    refresh(frm) {
        if (frm.doc.first_name && frm.doc.last_name) {
            frm.set_value("full_name", frm.doc.first_name + " " + frm.doc.last_name);
        }
    },

    first_name(frm) {
        frm.trigger("generate_full_name");
    },

    last_name(frm) {
        frm.trigger("generate_full_name");
    },

    generate_full_name(frm) {
        if (frm.doc.first_name && frm.doc.last_name) {
            frm.set_value("full_name", frm.doc.first_name + " " + frm.doc.last_name);
        }
    }
});

