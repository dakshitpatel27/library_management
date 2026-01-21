app_name = "library_management"
app_title = "Library Management"
app_publisher = "Dakshit"
app_description = "Library"
app_email = "dakshitgajipara@gmail.com"
app_license = "mit"


# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
	{
		"name": "library_management",
		"logo": "/assets/library_management/images/logo.png" ,
		"title": "Library Management",
		"route": "/app/library_management",
		"has_permission": "library_management.events.has_app_permission"
	}
]    

# Includes in <head>
# ------------------
# # include js, css files in header of desk.html

# app_include_css = "/assets/library_management/css/test_css.css"
app_include_js = "/assets/library_management/js/test_js.js"



# include js, css files in header of web template
# web_include_css = "/assets/library_management/css/web_css.css"
# web_include_js = "/assets/library_management/js/web_js.js"



# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "library_management/public/scss/website"



# include js, css files in header of web form
# webform_include_js = {"Student": "public/js/student_custom.js"}
# webform_include_css = {"Student": "public/css/student_custom.css"}



# include js in page
# page_js = {"page" : "public/js/file.js"}



# include js in doctype views
doctype_js = {"Student" : "public/js/student_js.js"}
doctype_list_js = {
    "Student": "public/js/student_list.js",
    "Customer": "public/js/customer_list.js"
}


# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
doctype_calendar_js = {"Library Transaction" : "public/js/library_transaction_calender.js"}



# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "library_management/public/icons.svg" 



# Home Pages
# ----------
# application home page (will override Website Settings)
home_page = "login"



# website user home page (by Role)
# role_home_page = {
#     "Customer": "orders",  #If a user has role Customer, /orders will be their homepage.
#     "Supplier": "invoices"    #If a user has role Supplier, /bills will be their homepage.
# }



# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------
# add methods and filters to jinja environment
jinja = {
	"methods": "library_management.jinja_methods",
	"filters": "library_management.jinja_filters"
}

# Installation
# ------------
# bench --site sigzen.local install-app library_management
before_install = "library_management.events.before_install" # Just before the app is installed on the site
after_install = "library_management.events.after_install" # Immediately after the app is installed

# Uninstallation
# ------------
# bench --site sigzen.local uninstall-app library_management
before_uninstall = "library_management.events.before_uninstall" #Just before the app is uninstalled from the site
after_uninstall = "library_management.events.after_uninstall"  # Immediately after the app is uninstalled

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument
before_app_install = "library_management.events.before_app_install" #Before app is installed
after_app_install = "library_management.events.after_app_install"   #After app is installed

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument
before_app_uninstall = "library_management.events.before_app_uninstall"
after_app_uninstall = "library_management.events.after_app_uninstall"

before_migrate = "library_management.events.before_migrate"
after_migrate = "library_management.events.after_migrate"
# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

notification_config = "library_management.events.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
    "Student":"library_management.events.student_query"
}
#
has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
    "Student":"library_management.events.student_has_permission"
}

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events
doc_events = {
    "Student": {
        "validate": "library_management.events.student_validate"
    },
    "Customer": {
        "validate": [
            "library_management.events.customer_address"
            ],
        "after_insert":[
            "library_management.events.customer_validate"
        ],
        "on_update":[
            "library_management.events.customer_validate"
        ],
        "after_delete":[
            "library_management.events.customer_validate"
        ]
    }
}

scheduler_events = {
    "cron":{     
        "0 14 * * *":[
            "library_management.tasks.cron"
        ]
    },
	"all": [     #Runs Every 4 Minutes
		"library_management.tasks.insert_note_all"
	],
	"daily": [   #Runs Daily Once
		"library_management.tasks.daily"
	],
	"hourly": [  #Runs Hourly Once
		"library_management.tasks.hourly"
	],
	"weekly": [  #Runs Weekly Once Most Sunday
		"library_management.tasks.weekly"
	],
	"monthly": [ #Runs Monthly Once
		"library_management.tasks.monthly"
	]
}

# Testing   
# -------
# bench --site sigzen.local run-tests
before_tests = "library_management.events.before_tests"

# Overriding Methods
# ------------------------------
override_whitelisted_methods = {
	# "frappe.desk.doctype.event.event.get_events": "library_management.event.get_events"
    "frappe.auth.get_logged_user":"library_management.api.rest_api.get_logged_user"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "library_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
auto_cancel_exempted_doctypes = ["Payment Entry"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
before_request = ["library_management.events.before_request"]
after_request = ["library_management.events.after_request"]

# Job Events
# ----------
before_job = ["library_management.events.before_job"]
after_job = ["library_management.events.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

auth_hooks = [
	"library_management.events.validate"
]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

default_log_clearing_doctypes = {
	# "Logging DocType Name": 30  # days to retain logs
    "Error Log": 30,
    "Activity Log": 15
}

on_login = "library_management.events.successful_login"
on_logout = "library_management.events.logout"

default_mail_footer = """
 <div>
 Sent via <a href="https://dakshit.vercel.app" target="_blank">ERP</a>
 </div>
"""

fixtures = [
    {
        "doctype": "Library Member"
    }
]

test_string = "value"
test_list = ["value"]
test_dict = {
    "key": "value"
}