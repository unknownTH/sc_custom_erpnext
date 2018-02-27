frappe.ui.form.on("Customer", "refresh", function(frm) {
	frm.add_custom_button(__('Open Items'), function() {
				frappe.set_route('query-report', 'Customer Open Items', {customer:frm.doc.name});
	});
	frm.add_custom_button(__('Return Open Items'), function() {
				frappe.set_route('query-report', 'Customer Open Items per Sales Order', {customer:frm.doc.name});
	});
});