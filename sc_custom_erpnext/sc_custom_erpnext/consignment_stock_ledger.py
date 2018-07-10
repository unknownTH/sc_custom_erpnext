# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

# future reposting
#class NegativeStockError(frappe.ValidationError): pass

#_exceptions = frappe.local('stockledger_exceptions')
# _exceptions = []


def validate_negative_stock(voucher, reverse_qty=False):
	csl_entries = voucher.get("items")
	for item in csl_entries:
		if reverse_qty == True:
			item.quantity = item.qty * -1
		else:
			item.quantity = item.qty
		
		csl_qty_after_transaction = get_consignment_stock_ledger_balance(item, voucher) + item.quantity
		
		if csl_qty_after_transaction < 0:
			# negative stock!
			frappe.throw('Consignment Stock for "{0}" would be {1}.'.format(item.item_code, csl_qty_after_transaction))

			
def get_consignment_stock_ledger_balance(item, voucher):
	data = frappe.db.sql("""
		SELECT
			SUM(qty)
		FROM 
			`tabConsignment Stock Ledger Entry` 
		WHERE 
			customer = '{0}' AND item_code ='{1}'
		GROUP BY
			item_code
		""".format(voucher.customer, item.item_code))
	
	if data: 
		data = int(data[0][0])
	else:
		data = 0
		
	return data
			

def make_consignment_stock_ledger_entries(voucher, remark=False, reverse_qty=False):
	csl_entries = voucher.get("items")
	
	if remark == False:
		voucher.remark = ""
	
	for item in csl_entries:
		if reverse_qty == True:
			item.quantity = item.qty * -1
		else:
			item.quantity = item.qty
	
		make_consignment_stock_ledger_entry(item, voucher)
			
			
def make_consignment_stock_ledger_entry(item, voucher):
	csl_entry_dict = { 
		"doctype": "Consignment Stock Ledger Entry",
		"item_code": item.item_code,
		"posting_date": voucher.posting_date,
		"posting_time": voucher.posting_time,
		"voucher_type": voucher.doctype,
		"voucher_no": voucher.name,
		"company": voucher.company,
		"customer": voucher.customer,
		"qty": item.quantity,
		"rate": item.rate,
		"amount": item.amount,
		"currency": voucher.currency,
		"remark": voucher.remark
	}
	
	new_csle = frappe.get_doc(csl_entry_dict)
	new_csle.insert()

	
def delete_related_consignment_stock_ledger_entries(voucher):
	csles = frappe.get_all("Consignment Stock Ledger Entry", fields=["name"], filters = {"voucher_no":voucher.name})
	
	for csle in csles:
		frappe.delete_doc("Consignment Stock Ledger Entry", csle.name)