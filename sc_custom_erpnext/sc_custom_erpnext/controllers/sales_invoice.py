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
		validate_negative_stock(doc, reverse_qty=True)

	
def on_submit(doc,method):
	if doc.is_consignment_transaction == 1: 	
		make_consignment_stock_ledger_entries(doc, reverse_qty=True)


def on_cancel(doc,method):
	if doc.is_consignment_transaction == 1: 
		delete_related_consignment_stock_ledger_entries(doc)