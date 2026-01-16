frappe.listview_settings["Customer"] = {
    onload: function (listview) {
        listview.page.add_inner_button(__("Button"), function () {
            frappe.msgprint({
                title: __("Triggered"),
                message: __("Button Clicked"),
                indicator: "blue"
            });
        });
    }
};
