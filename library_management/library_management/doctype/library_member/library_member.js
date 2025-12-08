// Copyright (c) 2025, Dakshit and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Library Member", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Library Member", {
    refresh(frm) {
        if (frm.doc.is_blocked) {
            frm.dashboard.set_headline_alert(
                "🚫 This Member is BLOCKED — Cannot Issue New Books",
                "red"
            );
        } else {
            frm.dashboard.clear_headline();
        }
    }
});

