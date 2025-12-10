import frappe
from frappe.utils import nowdate, getdate, date_diff


def _settings():
    try:
        return frappe.get_single("Library Settings")
    except Exception:
        return None

def update_block_status_for_members():
    settings = _settings()
    if not settings or not getattr(settings, "block_on_overdue", 0):
        return

    members = frappe.get_all("Library Member", pluck="name")

    for m in members:
        unpaid_penalty = frappe.db.sql(
            """
            SELECT SUM(penalty)
            FROM `tabLibrary Transaction`
            WHERE member=%s AND transaction_type='Return' AND docstatus=1
              AND penalty > 0 AND IFNULL(penalty_cleared, 0) = 0
            """,
            m,
        )[0][0] or 0

        frappe.db.set_value("Library Member", m, "is_blocked", 1 if unpaid_penalty > 0 else 0)

    frappe.db.commit()
    frappe.logger().info("Block status updated for library members")