frappe.ui.form.on("Student", {
    refresh(frm) {
        frm.set_df_property("date_of_birth","max_date",frappe.datetime.get_today());
    },

    date_of_birth(frm) {
        const today = frappe.datetime.get_today();
        if (frm.doc.date_of_birth >= today) {
            frm.set_value("date_of_birth", null);
            frappe.throw("Date of Birth cannot be a future date");
        }
    },
    enrollment_date(frm){
        if(frm.doc.date_of_birth >= frm.doc.enrollment_date){
            frm.set_value("enrollment_date",null);
            frappe.throw("Enrollment Date Should Be Grater Than DOB")
        }
    },
    set_save_indicator(frm) {
        if (!frm.doc.__islocal && !frm.doc.__unsaved) {
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
        frm.set_value("total_marks", total);
        const percentage = total ? (obtained / total) * 100 : 0;
        frm.set_value("maximum_marks", obtained);
        frm.set_value("percentage", percentage.toFixed(2));
    },
    after_save(frm) {
        frm.reload_doc().then(() => {
            frm.trigger("calculate_totals");
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
    },
});

//------------------------------------ Task Week 5&6 -------------------------------------------------
// frappe.ui.form.on("Student Subject", {
//     subject_name(frm) {
//         if (!frm.is_new() || frm.__last_student_shown) return;
//         frm.__last_student_shown = true;
//         frappe.call({
//             method: "library_management.library_management.doctype.student.student.get_last_student_subjects",
//             callback(r) {
//                 if (!r.message || !r.message.length) return;
//                 frappe.msgprint({title: __("Last Student Subjects"),message: r.message.map(row => row.subject_name).join("<br>")});
//             }
//         });
//     }
// });
//----------------------------------------------------------------------------------------------------


//-------------------------------------------------Databse API --------------------------------------
frappe.ui.form.on("Student", {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button("Run Database APIs", () => {
                run_all_db_apis(frm);
            });
        }
    }
});

function run_all_db_apis(frm) {
    frappe.call({
        method: "library_management.library_management.doctype.student.student.get_active_student",
        callback(r) {
            frappe.msgprint(`Excellent Students Count: ${r.message}`);
        }
    });

    frappe.call({
        method: "library_management.library_management.doctype.student.student.get_list",
        callback(r) {
            console.log("get_list:", r.message);
        }
    });

    frappe.call({
        method: "library_management.library_management.doctype.student.student.get_all",
        callback(r) {
            console.log("get_all:", r.message);
        }
    });

    frappe.call({
        method: "library_management.library_management.doctype.student.student.get_value",
        callback(r) {
            frappe.msgprint(`get_value Result: ${r.message}`);
        }
    });

    frappe.call({
        method: "library_management.library_management.doctype.student.student.get_single_value",
        callback(r) {
            frappe.msgprint(`get_single_value Result: ${r.message}`);
        }
    });

    frappe.call({
        method: "library_management.library_management.doctype.student.student.set_value",
        callback(r) {
            frappe.msgprint("Value Updated Successfully");
        }
    });

    frappe.call({
        method: "library_management.library_management.doctype.student.student.exists",
        callback(r) {
            frappe.msgprint(`Exists Result: ${r.message}`);
        }
    });
}