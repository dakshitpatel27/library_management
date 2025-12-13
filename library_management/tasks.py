import frappe

def _settings():
    try:
        return frappe.get_single("Library Settings")
    except Exception:
        return None
