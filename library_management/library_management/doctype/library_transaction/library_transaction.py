import frappe
from frappe.model.document import Document
from frappe.utils import add_days, nowdate, getdate, date_diff


class LibraryTransaction(Document):

    def validate(self):
        if self.transaction_type not in ["Issue", "Return", "Renew"]:
            frappe.throw("Transaction Type must be Issue, Return or Renew.")

        if not self.member:
            frappe.throw("Member is required.")
        if not self.book:
            frappe.throw("Book is required.")

        if self.transaction_type == "Issue" and not self.issue_date:
            self.issue_date = nowdate()

        if self.transaction_type == "Return" and not self.return_date:
            self.return_date = nowdate()

        self.settings = frappe.get_single("Library Settings")

        if self.transaction_type == "Issue":
            self.check_manual_block()
            self.check_member_block_status()
            self.check_borrow_limit()

        if self.transaction_type == "Return":
            self.calculate_penalty()

    # ---------------- STRICT BLOCK IF PENALTY EXISTS ----------------
    def check_member_block_status(self):
        if not getattr(self.settings, "block_on_overdue", 0):
            return

        unpaid = self.get_unpaid_penalty_total()
        member = frappe.get_doc("Library Member", self.member)

        if unpaid > 0:
            member.is_blocked = 1
            member.save()
            frappe.throw(f"Issue not allowed — penalty of {unpaid} is not cleared.")

        if unpaid == 0 and member.is_blocked:
            member.is_blocked = 0
            member.save()

    # ---------------- MANUAL BLOCK ----------------
    def check_manual_block(self):
        if frappe.db.get_value("Library Member", self.member, "is_blocked"):
            frappe.throw("Issue not allowed — this member is blocked.")

    # ---------------- UNPAID PENALTY TOTAL ----------------
    def get_unpaid_penalty_total(self):
        total = frappe.db.sql(
            """
            SELECT SUM(penalty)
            FROM `tabLibrary Transaction`
            WHERE member=%s AND transaction_type='Return'
              AND docstatus=1 AND penalty > 0
              AND IFNULL(penalty_cleared, 0) = 0
            """,
            (self.member,),
        )[0][0]
        return total or 0

    # ---------------- LIMIT ACTIVE ISSUES ----------------
    def check_borrow_limit(self):
        max_books = getattr(self.settings, "max_books_issue", 0)
        if not max_books:
            return

        issued = frappe.db.count(
            "Library Transaction",
            {"member": self.member, "transaction_type": "Issue", "docstatus": 1}
        )
        returned = frappe.db.count(
            "Library Transaction",
            {"member": self.member, "transaction_type": "Return", "docstatus": 1}
        )

        active = max(0, issued - returned)
        if active >= max_books:
            frappe.throw(f"Limit reached. Max allowed = {max_books} active issues.")

    # ---------------- PENALTY CALCULATION ----------------
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

    # ---------------- MAIN ACTIONS ----------------
    def before_submit(self):
        settings = frappe.get_single("Library Settings")
        book = frappe.get_doc("Library Book", self.book)
        member = frappe.get_doc("Library Member", self.member)

        email = member.email

        # ===== ISSUE =====
        if self.transaction_type == "Issue":
            if (book.available_copies or 0) <= 0:
                frappe.throw("No copies available.")

            if not self.due_date:
                self.due_date = add_days(self.issue_date, settings.issue_duration or 7)

            book.available_copies -= 1
            book.save()

            msg = f"📚 Book Issued Successfully\nBook: {self.book}\nDue Date: {self.due_date}"

        # ===== RETURN =====
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

            msg = f"📗 Book Returned\nBook: {self.book}\nPenalty: {self.penalty or 0}"

        # ===== RENEW =====
        elif self.transaction_type == "Renew":
            self.due_date = add_days(self.due_date, settings.issue_duration or 7)
            book.save()
            msg = f"🔄 Book Renewed\nBook: {self.book}\nNew Due Date: {self.due_date}"

        # ===== SEND EMAIL ONLY =====
        if email:
            frappe.sendmail(
                recipients=[email],
                subject="Library Transaction Update",
                message=msg,
                now=True,
            )

    # ---------------- UNBLOCK AFTER PENALTY CLEARED ----------------
    def on_update_after_submit(self):
        if self.transaction_type == "Return" and self.penalty == 0:
            member = frappe.get_doc("Library Member", self.member)
            if member.is_blocked:
                member.is_blocked = 0
                member.save()

    # ---------------- CANCEL ----------------
    def on_cancel(self):
        book = frappe.get_doc("Library Book", self.book)

        if self.transaction_type == "Issue":
            book.available_copies += 1
        elif self.transaction_type == "Return":
            book.available_copies -= 1

        book.available_copies = max(0, min(book.available_copies, book.total_copies or book.available_copies))
        book.save()
