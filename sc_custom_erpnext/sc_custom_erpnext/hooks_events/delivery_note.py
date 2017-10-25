# Copyright (c) 2017, unknownTH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt

def on_submit(doc,method):
	sales_orders = frappe.db.sql("""
		SELECT against_sales_order
		FROM `tabDelivery Note Item`
		WHERE parent = %(parent)s
		GROUP BY against_sales_order
		""", {"parent":doc.name}, as_dict=True)
		
	for sales_order in sales_orders:
		update_sales_order_status(sales_order.against_sales_order)
		
	return None

def update_sales_order_status(so_name):	
	sales_order_items = frappe.db.sql("""
		SELECT *
		FROM `tabSales Order Item`
		WHERE parent = %(parent)s
		""", {"parent":so_name}, as_dict=True)
	
	billed_amount = 0
	returned_amount = 0
	
	for item in sales_order_items:
		billed_amount = flt(billed_amount) + flt(item.billed_amt)
		returned_amount = flt(returned_amount) + flt(item.returned_qty) * flt(item.base_net_rate)
		
	base_net_total = frappe.db.get_value("Sales Order", {"name":so_name}, "base_net_total")
	
	per_billed = (flt(billed_amount) + flt(returned_amount)) / flt(base_net_total) * 100
	
	frappe.db.sql("""
		UPDATE `tabSales Order`
		SET per_billed = %(per_billed)s
		WHERE name = %(name)s
		""", {"per_billed":per_billed, "name":so_name})
	
	per_delivered = frappe.db.get_value("Sales Order", {"name":so_name}, "per_delivered")
		
	if per_billed == 100 and per_delivered < 100:
		frappe.db.sql("""
		UPDATE `tabSales Order`
		SET status = 'To Deliver', billing_status = 'Fully Billed'
		WHERE name = %(name)s
		""", {"name":so_name})
	elif per_billed == 100 and per_delivered == 100:
		frappe.db.sql("""
		UPDATE `tabSales Order`
		SET status = 'Completed', billing_status = 'Fully Billed'
		WHERE name = %(name)s
		""", {"name":so_name})
	
	return None