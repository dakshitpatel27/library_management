import frappe

#------------------------------------------ TASK WEEK 5 -------------------------------------
def student_validate(doc, method=None):
    obtained = 0
    for row in doc.get("subjects") or []:
        try:
            marks = float(row.get("marks") or 0)
        except Exception:
            marks = 0
        obtained += marks
    total_marks = len(doc.subjects or []) * 100
    percentage = (obtained / total_marks) * 100 if total_marks else 0
    doc.total_marks = total_marks
    doc.obtained_marks = obtained
    doc.percentage = round(percentage, 2)
    if percentage < 40:
        doc.status = "Failed"
    elif percentage >= 85:
        doc.status = "Excellent"
    else:
        doc.status = "Pass"

#------------------------------------------ TASK WEEK 5 -------------------------------------

def customer_validate(doc, method=None):
    counts = frappe.db.sql("""SELECT customer_group, COUNT(*) as total FROM `tabCustomer` GROUP BY customer_group""", as_dict=True)
    for row in counts:
        frappe.db.sql("""UPDATE `tabCustomer` SET customer_group_count = %s WHERE customer_group = %s """, (row.total, row.customer_group))
    frappe.db.commit()


#-----------------------------------------Task Week 7--------------------------------------------

def customer_address(doc, method):
    if doc.primary_address:
        frappe.msgprint(
            f"""
            <b>Customer:</b> {doc.customer_name}<br>
            <b>Primary Address:</b> {doc.primary_address}<br><br>
            Customer details updated successfully.
            """,
            title="Customer Updated",
            indicator="green"
        )


#----------------------------Hooks WEEK 7----------------------------------------
def before_install():
    print("""

          Library Management is About to be installed !
          
          """)

def after_install():
    if not frappe.db.exists("Student", "Default Student"):
        frappe.get_doc({
            "doctype": "Student",
            "student_id":1,
            "name1": "Default Student"
        }).insert(ignore_permissions=True)
        print("""
              
              Default Student created after installation.
              
              """)

def before_uninstall():
    print("""
          
          Library Management Is About To Be Uninstalled !
          
          """)

def after_uninstall():
    print("""
          
          Library Management Successfully Uninstalled !
          
          """)

def before_tests():
    print("""
          
          Running Tests
          
          """)

def before_app_install():
    print("""
          
          Before app install hook executed
          
          """)

def after_app_install():
    print("""
          
          After app install hook executed
          
          """)

def before_app_uninstall(app_name):
    print(f"Uninstalling app: {app_name}")

def after_app_uninstall(app_name):
    print(f"Uninstalled app: {app_name}")

def before_migrate():
    print(f"Migratting App")

def after_migrate():
    print(f"Migration Is Done")

def get_notification_config():
    return {
        "for_doctype": {
            "Library Transaction": {"transaction_type": "Issue"},
            "Student": {"status": "Excellent"}
        },
        "for_module": {
            "Library Management": "library_management.events.get_library_management_count"
        }
    }

def get_library_management_count():
    issue_count = frappe.db.count(
        "Library Transaction",
        filters={"transaction_type": "Issue"}
    )

    return_count = frappe.db.count(
        "Library Transaction",
        filters={"transaction_type": "Return"}
    )

    return issue_count + return_count

def student_query(user):
    user = user or frappe.session.user
    return (
        "`tabStudent`.owner = {user} OR `tabStudent`.modified_by = {user}"
    ).format(user=frappe.db.escape(user))

def student_has_permission(doc, user=None, permission_type=None):
    user = user or frappe.session.user
    if permission_type == "read" and doc.owner == user:
        return True
    if permission_type == "write" and doc.owner == user:
        return True
    return False

def successful_login():
    frappe.msgprint("Successfull Login")

def logout():
    print("User Logged Out")

def before_request():
    frappe.local.request_start_time = frappe.utils.now()

def after_request(response=None):
    start = getattr(frappe.local, "request_start_time", None)
    if start:
        frappe.logger().info(
            f"Request by {frappe.session.user}"
        )
    return response



def before_job():
    print("""
          
          Before background job executed
          
          """)

def after_job():
    print("""
          
          After background job executed
          
          """)


def validate():
    print("""
          
          Auth hook executed
          
          """)



def has_app_permission():
	roles = frappe.get_roles(frappe.session.user)
	if "System Manager" in roles or "Librarian" in roles:
		return True
	return False

#----------------------------------LIBRARY CALENDAR-------------------------------------

@frappe.whitelist()
def get_library_transactions(start, end, filters=None):
    return frappe.get_all(
        "Library Transaction",
        fields=[
            "book",
            "issue_date",
            "due_date",
            "member"
        ],
        filters={
            "issue_date": ["between", [start, end]]
        }
    )