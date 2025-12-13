import frappe
from frappe.model.document import Document

class LibraryBook(Document):
   
   def before_insert(self):
    if not self.available_copies:
        self.available_copies = self.total_copies

   def validate(self):
    self.total_copies = int(self.total_copies or 0)
    if not self.available_copies:
        self.available_copies = self.total_copies

    if self.available_copies > self.total_copies:
        frappe.throw("Available Copies cannot be greater than Total Copies.")
