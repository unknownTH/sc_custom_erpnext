frappe.ui.form.on("Customer", "refresh", function(frm) {
	frm.add_custom_button(__('Cons. Ledger'), function() {
		frappe.set_route('query-report', 'Consignment Stock Ledger', {customer:frm.doc.name});
	});
	frm.add_custom_button(__('Cons. Balance'), function() {
		frappe.set_route('query-report', 'Consignment Stock Balance', {customer:frm.doc.name});
	});
});