# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import frappe

# Rename all Variants with: bench execute sc_custom_erpnext.sc_custom_erpnext.rename_item_variants.rename_item_variants

@frappe.whitelist()
def rename_item_variants(erpnext_parent_item=None):
    for variant_item in get_variant_items(erpnext_parent_item):
        erpnext_item = frappe.get_doc("Item", variant_item.get("name"))

        new_item_name = get_new_item_name(erpnext_item)
        erpnext_item.item_name = new_item_name
        erpnext_item.flags.ignore_mandatory = True
        erpnext_item.save()

        frappe.rename_doc("Item", erpnext_item.get("name"), new_item_name)
        
        frappe.db.commit()

def get_variant_items(erpnext_parent_item):
    if erpnext_parent_item:
        variant_items_querry = f"""SELECT name FROM tabItem WHERE variant_of = '{erpnext_parent_item}'"""

    else:
        variant_items_querry = """SELECT name FROM tabItem WHERE variant_of IS NOT NULL"""
    
    return frappe.db.sql(variant_items_querry, as_dict=1)

def get_new_item_name(erpnext_item):
    new_item_name = f'{erpnext_item.get("variant_of")}:'

    for variant_attribute_value in get_variant_attribute_values(erpnext_item):
        if variant_attribute_value.get("attribute") == "Gift Card Value":
            new_item_name += f' {variant_attribute_value.get("abbr")}'

    for variant_attribute_value in get_variant_attribute_values(erpnext_item):
        if variant_attribute_value.get("attribute") == "Material":
            new_item_name += f' {variant_attribute_value.get("abbr")}'
    
    for variant_attribute_value in get_variant_attribute_values(erpnext_item):
        if variant_attribute_value.get("attribute") == "Color":
            new_item_name += f' - {variant_attribute_value.get("abbr")}'
    
    for variant_attribute_value in get_variant_attribute_values(erpnext_item):
        if variant_attribute_value.get("attribute") == "Stone":
            new_item_name += f' - {variant_attribute_value.get("abbr")}'
    
    for variant_attribute_value in get_variant_attribute_values(erpnext_item):
        if variant_attribute_value.get("attribute") == "Size":
            new_item_name += f' - {variant_attribute_value.get("abbr")}'

    for variant_attribute_value in get_variant_attribute_values(erpnext_item):
        if variant_attribute_value.get("attribute") == "Design":
            new_item_name += f' - {variant_attribute_value.get("abbr")}'

    return new_item_name

def get_variant_attribute_values(erpnext_item):
    variant_attribute_values_querry = f"""SELECT iva.attribute, iav.abbr FROM `tabItem Variant Attribute` as iva,
        `tabItem Attribute Value` as iav WHERE iva.parent = '{erpnext_item.get("name")}' AND iav.attribute_value = iva.attribute_value
        AND iav.parent = iva.attribute"""

    return frappe.db.sql(variant_attribute_values_querry, as_dict=1)


