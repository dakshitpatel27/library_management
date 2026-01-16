frappe.views.calendar["Library Transaction"] = {
    field_map: {
        start: "issue_date",
        end: "due_date",
        id: "book",
        title: "member"
    },
    get_events_method: "library_management.events.get_library_transactions"
};
