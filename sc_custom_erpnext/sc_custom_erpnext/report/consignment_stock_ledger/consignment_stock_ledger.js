// Copyright (c) 2016, unknownTH and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Consignment Stock Ledger"] = {
	"filters": [
		{
            "fieldname":"customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer"
        },
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date"
		}
	]
}
