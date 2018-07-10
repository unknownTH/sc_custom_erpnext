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
			_("Item") + ":Link/Item:200",
			_("Qty") + ":Int:50",
			_("Rate") + ":Currency:100",
			_("Amount") + ":Currency:100"
	]		

def get_consignment_stock_ledger_entries(filters):
	data = frappe.db.sql("""
		SELECT
			item_code, SUM(qty), rate, SUM(qty) * rate AS amount
		FROM 
			`tabConsignment Stock Ledger Entry` 
		WHERE 
			customer = '{0}'
		GROUP BY
			item_code
		""".format(filters.customer))
	
	return data