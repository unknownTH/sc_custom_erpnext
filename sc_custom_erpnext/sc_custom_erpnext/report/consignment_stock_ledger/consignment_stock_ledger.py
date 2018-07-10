# Copyright (c) 2013, unknownTH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_consignment_stock_ledger_entries(filters)
	return columns, data

def get_columns():
	return [
			_("Date") + ":Date:80",
			_("Time") + ":Time:80",
			_("Item") + ":Link/Item:240",
			_("Qty") + ":Int:50",
			_("Rate") + ":Currency:80",
			_("Amount") + ":Currency:80",
			_("Remark") + "::80",
			_("Voucher Type") + "::160",
			_("Voucher Nr") + ":Dynamic Link/" + _("Voucher Type") + ":100"
	]		

def get_consignment_stock_ledger_entries(filters):
	data = frappe.db.sql("""
		SELECT
			posting_date, posting_time, item_code, qty, rate, amount, remark, voucher_type, voucher_no
		FROM 
			`tabConsignment Stock Ledger Entry` 
		WHERE 
			customer = '{0}' AND posting_date > '{1}'
		""".format(filters.customer, filters.from_date))
	
	return data