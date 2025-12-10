import frappe
from frappe.utils import nowdate, getdate, date_diff


# ---------------- SETTINGS FETCH ----------------
def _settings():
    try:
        return frappe.get_single("Library Settings")
    except Exception:
        return None


# ---------------- DUE / OVERDUE EMAIL REMINDERS ----------------
def send_due_and_overdue_reminders():
    settings = _settings()
    if not settings or not getattr(settings, "enable_reminders", 0):
        return

    today = getdate(nowdate())
    transactions = frappe.get_all(
        "Library Transaction",
        filters={"docstatus": 1, "transaction_type": "Issue", "return_date": ["is", "not set"]},
        fields=["name", "member", "book", "due_date"]
    )

    for tx in transactions:
        member = frappe.get_doc("Library Member", tx.member)
        if not member.email:
            continue

        book_title = frappe.db.get_value("Library Book", tx.book, "title")
        late_days = max(0, date_diff(today, tx.due_date))

        if late_days == 0:
            subject = f"Book Due Today: {book_title}"
            msg = f"Your book '{book_title}' is due today. Please return to avoid penalty."
        else:
            subject = f"Book Overdue ({late_days} days): {book_title}"
            msg = f"Your book '{book_title}' is overdue by {late_days} days. Return immediately to stop penalty charges."

        frappe.sendmail(recipients=[member.email], subject=subject, message=msg)
        frappe.logger().info(f"Email sent to {member.email} for {tx.name}")
        

# ---------------- AUTO BLOCK MEMBERS ----------------
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