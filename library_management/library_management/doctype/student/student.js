frappe.ui.form.on("Student", {
    refresh(frm) {
        frm.trigger("set_save_indicator");
        frm.trigger("calculate_totals");
    },
    set_save_indicator(frm) {
        if (!frm.doc.__islocal && !frm.doc.__unsaved && frm.is_dirty()) {
            frm.page.set_indicator("Saved", "green");
        } else {
            frm.page.set_indicator("Not Saved", "orange");
        }
    },
    calculate_totals(frm) {
        let obtained = 0;
        (frm.doc.subjects || []).forEach(row => {
            obtained += flt(row.marks) || 0;
        });
        const total = (frm.doc.subjects?.length || 0) * 100;
        const percentage = total ? (obtained / total) * 100 : 0;
        frm.set_value("maximum_marks", obtained);
        frm.set_value("total_marks", total);
        frm.set_value("percentage", percentage.toFixed(2));
    },
    after_save(frm) {
        frm.reload_doc().then(() => {
            frm.trigger("calculate_totals");
            frm.trigger("set_save_indicator");
        });

    }
});
frappe.ui.form.on("Student Subject", {
    subject_name(frm, cdt, cdn) {
        const row = frappe.get_doc(cdt, cdn);
        if (!row.marks) {
            row.marks = 0;
            frm.refresh_field("subjects");
        }
    },
    marks(frm, cdt, cdn) {
        const row = frappe.get_doc(cdt, cdn);
        row.marks = flt(row.marks) || 0;
        if (row.marks < 0 || row.marks > 100) {
            frappe.msgprint({
                title: "Invalid Marks",
                message: "Marks must be between 0 and 100",
                indicator: "red"
            });
            row.marks = 0;
        }
        frm.refresh_field("subjects");
        frm.trigger("calculate_totals");
        frm.trigger("set_save_indicator");
    },
    subjects_remove(frm) {
        frm.trigger("calculate_totals");
        frm.trigger("set_save_indicator");
    }
});