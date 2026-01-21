
// -----------------------------------------Task Week 7--------------------------------------------

frappe.listview_settings["Student"] = {
    add_fields: ["status"],

    get_indicator: function (doc) {
        if (!doc.status) return;

        if (doc.status === "Excellent") {
            return [__("Excellent"), "green", "status,=,Excellent"];
        }

        if (doc.status === "Pass") {
            return [__("Pass"), "blue", "status,=,Pass"];
        }

        if (doc.status === "Failed") {
            return [__("Failed"), "red", "status,=,Failed"];
        }
    }
};


//-----------------------------Review Task------------------------------------

frappe.listview_settings["Student"] = {
    onload: function (listview) {
        listview.page.add_inner_button(__("Button"), function () {
            frappe.msgprint({
                title: __("Triggered"),
                message: __("This Is List View Button By Using Onload Method & Inner Button"),
                indicator: "blue"
            });
        });
    }
};

