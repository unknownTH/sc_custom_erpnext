// Copyright (c) 2017, unknownTH and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Open Items per Sales Order"] = {
	"filters": [
        {
            "fieldname":"customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer"
        }
	]
}
