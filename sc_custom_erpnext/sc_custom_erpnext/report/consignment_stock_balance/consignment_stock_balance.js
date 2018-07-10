// Copyright (c) 2016, unknownTH and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Consignment Stock Balance"] = {
	"filters": [
		{
            "fieldname":"customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer"
        }
	]
}
