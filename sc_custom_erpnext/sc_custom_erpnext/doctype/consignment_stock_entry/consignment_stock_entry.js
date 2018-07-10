// Copyright (c) 2018, unknownTH and contributors
// For license information, please see license.txt

{% include 'erpnext/selling/sales_common.js' %};

frappe.provide("sc_custom_erpnext");
frappe.ui.form.on('Consignment Stock Entry', {
	refresh: function(frm) {
	}
});

sc_custom_erpnext.ConsignmentStockController = erpnext.selling.SellingController.extend({
	setup: function(doc) {
		this.setup_posting_date_time_check();
		this._super(doc);
	},
});

$.extend(cur_frm.cscript, new sc_custom_erpnext.ConsignmentStockController({frm: cur_frm}));
