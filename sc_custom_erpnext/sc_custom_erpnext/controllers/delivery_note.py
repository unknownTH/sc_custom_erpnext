# Copyright (c) 2017, unknownTH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from sc_custom_erpnext.sc_custom_erpnext.consignment_stock_ledger import validate_negative_stock
from sc_custom_erpnext.sc_custom_erpnext.consignment_stock_ledger import make_consignment_stock_ledger_entries
from sc_custom_erpnext.sc_custom_erpnext.consignment_stock_ledger import delete_related_consignment_stock_ledger_entries


def validate(doc,method):
	if doc.is_consignment_transaction == 1: 
		validate_negative_stock(doc)

		
def on_submit(doc,method):
	if doc.is_consignment_transaction == 1: 
		make_consignment_stock_ledger_entries(doc)
	
	frappe.db.set(doc, "status", "Closed")
		
	update_related_sales_order_status(doc)
	
		
def on_cancel(doc,method):
	if doc.is_consignment_transaction == 1: 
		delete_related_consignment_stock_ledger_entries(doc)
	
	
def update_related_sales_order_status(doc):
	for item in doc.get("items"):	
		sales_order = frappe.get_doc("Sales Order", item.against_sales_order)
		
		if sales_order.per_delivered == 100:
			frappe.db.set(sales_order, "status", "Closed")