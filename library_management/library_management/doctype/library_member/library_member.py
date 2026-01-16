# Copyright (c) 2025
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
class LibraryMember(Document):
    def after_insert(self):
        email = getattr(self, "email", None)        
        message = f"""
                    🎉 Welcome {self.first_name}!<br></br>
                    <b>Your Library Membership has been created successfully.</b><br></br>
                     Member ID: {self.member_id}<br></br>
                     <br></br>
                     <b>Library Management System</b>
                   """
        if email:
            frappe.sendmail(
                recipients=[email],
                subject="Welcome to Library",
                message=message
            )