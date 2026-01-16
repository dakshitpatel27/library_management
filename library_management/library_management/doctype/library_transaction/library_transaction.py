import frappe
from frappe.model.document import Document
from frappe.utils import add_days, nowdate, getdate, date_diff

class LibraryTransaction(Document):
    def validate(self):
        if self.transaction_type not in ["Issue", "Return"]:
            frappe.throw("Transaction Type must be Issue, Return or Renew.")
        if not self.member:
            frappe.throw("Member is required.")
        if not self.book:
            frappe.throw("Book is required.")

        if self.transaction_type == "Issue" and not self.issue_date and not self.due_date:
            self.issue_date = nowdate()
            frappe.throw("Due Date is mandatory for Issue transactions")

        if self.transaction_type == "Return" and not self.return_date:
            frappe.throw("Return Date is mandatory for Return transactions")

        self.settings = frappe.get_single("Library Settings")
        if self.transaction_type == "Issue":
            self.check_manual_block()
        if self.transaction_type == "Return":
            self.calculate_penalty()

    def check_manual_block(self):
        if frappe.db.get_value("Library Member", self.member, "is_blocked"):
            frappe.throw("Issue not allowed — this member is blocked.")

    def calculate_penalty(self):
        self.penalty = 0
        if self.transaction_type != "Return":
            return

        rate = getattr(self.settings, "penalty_per_day", 0)
        if not rate or not self.due_date or not self.return_date:
            return

        if getdate(self.return_date) > getdate(self.due_date):
            late_days = date_diff(self.return_date, self.due_date)
            self.penalty = late_days * rate

    def before_submit(self):
        settings = frappe.get_single("Library Settings")
        book = frappe.get_doc("Library Book", self.book)
        member = frappe.get_doc("Library Member", self.member)
        email = member.email
        if self.transaction_type == "Issue":
            if (book.available_copies or 0) <= 0:
                frappe.throw("No copies available.")
            if not self.due_date:
                self.due_date = add_days(self.issue_date, settings.issue_duration or 7)
            book.available_copies -= 1
            book.save()
            msg = f"""📚Book Issued Successfully <br></br>
                        Member Name : {self.member} <br></br>
                        Book: {self.book} <br></br>
                        Issue Date : {self.issue_date} <br></br>
                        Due Date: {self.due_date} <br></br>
                        <br></br>
                        <b>NOTE:</b> Please Return It By The Due Date To Avoid Late Fees.<br></br>
                        <br></br>
                        <b>Library Management System</b>"""

        elif self.transaction_type == "Return":
            self.calculate_penalty()
            issued_count = frappe.db.count(
                "Library Transaction",
                {"member": self.member, "book": self.book, "transaction_type": "Issue", "docstatus": 1}
            )
            returned_count = frappe.db.count(
                "Library Transaction",
                {"member": self.member, "book": self.book, "transaction_type": "Return", "docstatus": 1}
            )
            if returned_count >= issued_count:
                frappe.throw("No pending issued copy to return.")
            book.available_copies = min(book.available_copies + 1, book.total_copies or book.available_copies + 1)
            book.save()

            msg = f"""📚Book Returned Successfully <br></br>
                        Member Name : {self.member} <br></br>
                        Book: {self.book} <br></br>
                        Issue Date : {self.issue_date} <br></br>
                        Due Date : {self.due_date}<br></br>
                        Return Date: {self.return_date} <br></br>
                        Penalty : {self.penalty or 0}<br></br>
                        <br></br>
                        <b>Library Management System</b>"""
            
        if email:
            frappe.sendmail(
                recipients=[email],
                subject="Library Transaction Update | Library Management System",
                message=msg
            )

    def on_update_after_submit(self):
        if self.transaction_type == "Return" and self.penalty == 0:
            member = frappe.get_doc("Library Member", self.member)
            if member.is_blocked:
                member.is_blocked = 0
                member.save()

    def on_cancel(self):
        book = frappe.get_doc("Library Book", self.book)
        if self.transaction_type == "Issue":
            book.available_copies += 1
        elif self.transaction_type == "Return":
            book.available_copies -= 1
        book.available_copies = max(0, min(book.available_copies, book.total_copies or book.available_copies))
        book.save()