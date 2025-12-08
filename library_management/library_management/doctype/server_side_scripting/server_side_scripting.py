# Copyright (c) 2025, Dakshit and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class ServerSideScripting(Document):

    def autoname(self):
        # Custom Name Format
        self.name = f"SSS-{frappe.generate_hash(length=6)}"



    def after_insert(self):
        frappe.msgprint("After Insert Triggered")
        # Example: send email or create log
        frappe.logger().info("Document Inserted Successfully")

    def validate(self):
        # frappe.msgprint("Validate Triggered")
        # # Example validation
        # if self.age and self.age < 0:
        #     frappe.throw("Age cannot be negative")
        frappe.msgprint(_("Hello My Name Is '{0}' ").format(
            self.first_name + " " + self.middle_name + " " + self.last_name))

    def before_save(self):
        frappe.msgprint("Before Save Triggered")
        # Example: Auto full name
        if self.first_name and self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}"

    def after_save(self):
        frappe.msgprint("After Save Triggered")
        # Example: Activity log
        frappe.logger().info("Document Saved")


    def on_submit(self):
        frappe.msgprint("On Submit Triggered")
        # Example: Update linked data
        self.status = "Submitted"

    def on_cancel(self):
        frappe.msgprint("On Cancel Triggered")
        # Example: Reverse operations
        self.status = "Cancelled"

    def on_trash(self):
        frappe.msgprint("On Trash Triggered")
        # Example: Clean dependencies
        frappe.logger().info("Document Deleted")

    def after_delete(self):
        frappe.msgprint("After Delete Triggered")
        frappe.logger().info("Delete Action Completed")

    def on_update(self):
        frappe.msgprint("On Update Triggered")
        frappe.logger().info("Document Updated")

    def before_update_after_submit(self):
        frappe.msgprint("Before Update After Submit Triggered")

    def on_update_after_submit(self):
        frappe.msgprint("On Update After Submit Triggered")
