# -*- coding: utf-8 -*-
# Copyright (c) 2018, unknownTH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from sc_custom_erpnext.sc_custom_erpnext.consignment_stock_ledger import validate_negative_stock
from sc_custom_erpnext.sc_custom_erpnext.consignment_stock_ledger import make_consignment_stock_ledger_entries
from sc_custom_erpnext.sc_custom_erpnext.consignment_stock_ledger import delete_related_consignment_stock_ledger_entries


class ConsignmentStockEntry(Document):
	def validate(self):
		validate_negative_stock(self)

		
	def on_submit(self):
		make_consignment_stock_ledger_entries(self)
		
	
	def on_cancel(self):
		delete_related_consignment_stock_ledger_entries(self)