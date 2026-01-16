import frappe
import time

def cron():
    frappe.msgprint("CRON schedular task executed")
    
def all():
    frappe.msgprint("ALL scheduler task executed")

def daily():
    frappe.msgprint("DAILY scheduler task executed")

def hourly():
    frappe.msgprint("HOURLY scheduler task executed")

def weekly():
    frappe.msgprint("WEEKLY scheduler task executed")

def monthly():
    frappe.msgprint("MONTHLY scheduler task executed")

def test_job():
    time.sleep(5)
    frappe.logger().info("Test job executed")