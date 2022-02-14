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
			_("Item") + ":Link/Item:300",
			_("Qty") + ":Int:50",
			_("Selling Price") + ":Currency:200"
	]		

def get_consignment_stock_ledger_entries(filters):
	data = frappe.db.sql(f"""
		SELECT
			csle.item_code, SUM(csle.qty), ip.price_list_rate AS selling_price
		FROM 
			`tabConsignment Stock Ledger Entry` AS csle
		LEFT JOIN 
			`tabItem Price` AS ip ON csle.item_code = ip.item_code 
		WHERE 
			csle.customer = '{filters.customer}'
		GROUP BY
			item_code
		""")
	
	return data