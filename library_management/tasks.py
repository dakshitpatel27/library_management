import frappe , time , random , string

def cron():
    print("CRON schedular task executed")

def insert_note_all():
    logger = frappe.logger("note_all")
    letters = string.ascii_letters
    note_title = "".join(random.choice(letters) for _ in range(5))
    try:
        note = frappe.get_doc({
            "doctype": "Note",
            "title": note_title
        })
        note.insert(ignore_permissions=True)
        frappe.db.commit()
        logger.info(f"Note created: {note_title}")
    except Exception:
        logger.error("Failed to insert Note")
        frappe.log_error("Note Cron Error",frappe.get_traceback())

def daily():
    print("DAILY scheduler task executed")

def hourly():
    print("HOURLY scheduler task executed")

def weekly():
    print("WEEKLY scheduler task executed")

def monthly():
    print("MONTHLY scheduler task executed")

def test_job():
    time.sleep(5)
    frappe.logger().info("Test job executed")

