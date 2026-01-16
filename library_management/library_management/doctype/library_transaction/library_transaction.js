frappe.ui.form.on("Library Transaction", {
    refresh(frm) {
        toggle_ui(frm);
        show_block_warning(frm);
    },

    transaction_type(frm) {
        toggle_ui(frm);
        if (frm.doc.transaction_type === "Issue") {
            frm.set_value("return_date", "");
            frm.set_value("penalty", 0);
        }
    },
    due_date(frm){
        if (frm.doc.due_date < frm.doc.issue_date) {
            frm.set_value("due_date","")
            frappe.throw("Due Date Must Be Greater Then Issue Date ")
        }
    },
    return_date(frm){
        if(frm.doc.return_date<frm.doc.issue_date){
            frm.set_value("return_date","")
            frappe.throw("Return Date Must Be Greater Then Issue Date")
        }
        if(frm.doc.return_date>frm.doc.issue_date){
            frappe.msgprint(f`Penalty Applied On ${frm.doc.member}'s Library Transaction Due To Late Return Please Find Penalty Details On Email`)
        }
    },

    member(frm) {
        show_block_warning(frm);
    }
});

function toggle_ui(frm) {
    const type = frm.doc.transaction_type;
    frm.toggle_display("return_date", type === "Return");
    frm.toggle_display("penalty", type === "Return");
}

function show_block_warning(frm) {
    if (!frm.doc.member) return;

    frappe.db.get_value("Library Member", frm.doc.member, "is_blocked", (d) => {
        if (d && d.is_blocked) {
            frm.dashboard.set_headline_alert(
                "This member is BLOCKED from issuing new books.",
                "red"
            );
        }
    });
}



