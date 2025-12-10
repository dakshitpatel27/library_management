# Copyright (c) 2025
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.pdf import get_pdf
import qrcode
from io import BytesIO


class LibraryMember(Document):

    def after_insert(self):

        email = getattr(self, "email", None)

        
        message = f"""
                    🎉 Welcome {self.first_name}!
                    Your Library Membership has been created successfully.
                    Member ID: {self.member_id}
                   """
        

        if email:
            frappe.sendmail(
                recipients=[email],
                subject="Welcome to Library",
                message=message,
                now=True,
            )


        try:
            qr_data = f"Member ID: {self.name}\nName: {self.first_name} {self.last_name}"
            qr_img = qrcode.make(qr_data)
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            qr_bytes = buffer.getvalue()


            qr_file = frappe.get_doc({
                "doctype": "File",
                "file_name": f"{self.name}_qr.png",
                "is_private": 0,
                "content": qr_bytes,
                "attached_to_doctype": "Library Member",
                "attached_to_name": self.name
            }).insert(ignore_permissions=True)


            self.qr_code = qr_file.file_url
            self.save()

        except Exception as e:
            frappe.log_error(f"QR Code Error: {e}", "QR Generation Failed")
            return
        
        
        try:
            html = frappe.render_template(
                "library_management/library_management/doctype/library_member/qr_template.html",
                {"doc": self}
            )
            pdf = get_pdf(html)

            pdf_file = frappe.get_doc({
                "doctype": "File",
                "file_name": f"{self.name}_card.pdf",
                "is_private": 1,
                "content": pdf,
                "attached_to_doctype": "Library Member",
                "attached_to_name": self.name,
            }).insert(ignore_permissions=True)

            # Send Email with PDF attachment
            if email:
                frappe.sendmail(
                    recipients=[email],
                    subject="Your Library Membership QR Card",
                    message="Please find your Membership Card attached.",
                    attachments=[{"fname": f"{self.name}_card.pdf", "fcontent": pdf}],
                    now=True,
                )

        except Exception as e:
            frappe.log_error(f"QR PDF Error: {e}", "QR PDF Generation Failed")
