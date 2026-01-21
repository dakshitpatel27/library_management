import frappe
import json
#------------------------------------TASK 1 WEEK 8 ---------------------------------------
#POST
#http://localhost:8000/api/method/library_management.api.rest_api.create_student
#BODY
# {
#   "student_id": 27,
#   "name1": "Daksh",
#   "date_of_birth": "2005-07-27",
#   "gender": "Male",
#   "grade": 10,
#   "enrollment_date": "2025-11-03",    
#   "subjects": [
#     {
#       "subject_name": "Frappe",
#       "marks": 98
#     },
#     {
#       "subject_name": "ERPNext",
#       "marks": 95
#     }
#   ]
# }

@frappe.whitelist()
def create_student():
    data = frappe.request.get_json()
    doc = frappe.new_doc("Student")
    doc.update(data)
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return {
        "status": "success",
        "message": "Student created successfully",
        "student_name": doc.name
    }


#---------------------------------------TASK 2 WEEK 8 -----------------------------------
#POST
#http://localhost:8000/api/method/library_management.api.rest_api.get_customers_groupwise
#BODY
# {
#   "data": {
#     "customer_group": "Demo Customer Group",
#     "disabled": 0
#   }
# }
@frappe.whitelist()
def get_customers_groupwise():
    data = frappe.local.form_dict.get("data")
    if isinstance(data, str):
        data = json.loads(data)
    customer_group = data.get("customer_group")
    disabled = data.get("disabled", 0)
    filters = {"disabled": disabled}
    if customer_group:
        filters["customer_group"] = customer_group
    customers = frappe.get_all(
        "Customer",
        filters=filters,
        fields=["name","customer_name","customer_group"],
        order_by="customer_group asc, customer_name asc"
    )
    grouped_data = {}
    for cust in customers:
        group = cust.customer_group
        grouped_data.setdefault(group, []).append(cust)
    return {
        "status": "success",
        "total_records": len(customers),
        "data": grouped_data
    }


# GET
#http://localhost:8000/api/method/library_management.api.rest_api.get_logged_user
@frappe.whitelist()
def get_logged_user():
    return frappe.session.user

#POST
#http://localhost:8000/api/method/library_management.api.rest_api.set_email_for_all?email=gajiparadakshit@gmail.com
@frappe.whitelist()
def set_email_for_all(email=None):
    if not email:
        frappe.throw("Email is required")
    users = frappe.get_all("User", pluck="name")
    for user in users:
        frappe.db.set_value("User", user, "email", email)
    frappe.db.commit()
    return {
        "status": "success",
        "updated_users": len(users)
    }

#GET
#http://localhost:8000/api/method/library_management.api.rest_api.greet_user?name=Dakshit
@frappe.whitelist()
def greet_user(name):
    return f"Hello, {name}!"

# GET & POST
#http://localhost:8000/api/method/library_management.api.rest_api.detect_method
@frappe.whitelist()
def detect_method():
    method = frappe.request.method
    if method == "GET":
        return "GET request received"
    if method == "POST":
        return "POST request received"


#POST
#http://localhost:8000/api/method/library_management.api.rest_api.create_student
#Body 
#{"data": {"first_name":"Dakshit","last_name":"Gajipara","email":"gajiparadakshit@gmail.com","student_id":"2"}}
# @frappe.whitelist()
# def create_student(data=None):
#     if frappe.request.method != "POST":
#         frappe.throw("Only POST allowed")

#     if not data:
#         frappe.throw("Data is required")

#     if isinstance(data, str):
#         data = json.loads(data)

#     doc = frappe.new_doc("REST API")
#     doc.update(data)
#     doc.insert(ignore_permissions=True)

#     return {
#         "status": "success",
#         "name": doc.name
#     }

##--------------------------------------Review Task ------------------------------------
#GET
#http://sigzen.local:8000/api/method/library_management.api.rest_api.get_child_items
@frappe.whitelist()
def get_child_items():
    invoice_name = "ACC-SINV-2025-00001"
    items = frappe.db.get_list("Sales Invoice Item",
        filters={
            "parent": invoice_name,
            "parenttype": "Sales Invoice",
            "parentfield": "items"
        },
        fields=["item_code","item_name","qty","uom","rate","amount"]
    )
    return {
        "invoice": invoice_name,
        "total_items": len(items),
        "items": items
    }
