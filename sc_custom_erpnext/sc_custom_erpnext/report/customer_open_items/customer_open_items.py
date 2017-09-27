# Copyright (c) 2013, unknownTH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from erpnext.accounts.report.non_billed_report import get_ordered_to_be_billed_data

def execute(filters=None):
	columns = get_column()
	data = get_customer_open_items()
	return columns, data

def get_column():
	return [
		_("Customer") + ":Link/Item:120",
		_("Item") + ":Link/Item:120",
		_("Qty") + ":Int:50",
		_("Rate") + ":Currency:100",
		_("Amount") + ":Currency:100"
	]		

def get_customer_open_items():
	data = frappe.db.sql("""
		SELECT
			`tabSales Order`.customer,
			`tabSales Order Item`.item_name, 
			SUM((`tabSales Order Item`.qty - `tabSales Order Item`.returned_qty) * `tabSales Order Item`.rate - `tabSales Order Item`.billed_amt) / `tabSales Order Item`.rate AS open_qty,
			`tabSales Order Item`.rate,
			SUM((`tabSales Order Item`.qty - `tabSales Order Item`.returned_qty) * `tabSales Order Item`.rate - `tabSales Order Item`.billed_amt) AS amount
		FROM 
			`tabSales Order Item` 
		INNER JOIN 
			`tabSales Order` on `tabSales Order Item`.parent = `tabSales Order`.name
		WHERE 
			`tabSales Order`.status = 'To Bill'
		GROUP BY 
			`tabSales Order Item`.item_name
		""")
	
	return data