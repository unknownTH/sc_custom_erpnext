frappe.ui.form.on("Customer", "refresh", function(frm) {
	frm.add_custom_button(__('Consignment Stock Ledger'), function() {
				frappe.set_route('query-report', 'Consignment Stock Ledger', {customer:frm.doc.name});
	});
	frm.add_custom_button(__('Consignment Stock Balance'), function() {
				frappe.set_route('query-report', 'Consignment Stock Balance', {customer:frm.doc.name});
	});
	dashboard_link_doctype(frm, "Consignment Stock Entry");
});


function dashboard_link_doctype(frm, doctype){

	var parent = $('.form-dashboard-wrapper [data-doctype="Sales Invoice"]').closest('div').parent();
	
	parent.find('[data-doctype="'+doctype+'"]').remove();

	parent.append(frappe.render_template("dashboard_link_doctype", {doctype:doctype}));

	var self = parent.find('[data-doctype="'+doctype+'"]');

	set_open_count(frm, doctype);

	// bind links
	self.find(".badge-link").on('click', function() {
		frappe.route_options = {"customer": frm.doc.name}
		frappe.set_route("List", doctype);
	});

	// bind open notifications
	self.find('.open-notification').on('click', function() {
		frappe.route_options = {
			"customer": frm.doc.name,
			"status": "Draft"
		}
		frappe.set_route("List", doctype);
	});

	// bind new
	if(frappe.model.can_create(doctype)) {
		self.find('.btn-new').removeClass('hidden');
	}
	self.find('.btn-new').on('click', function() {
		frappe.new_doc(doctype,{
			"customer": frm.doc.name
		});
	});
}

function set_open_count(frm, doctype){
	frappe.call({
		method: 'sc_custom_erpnext.sc_custom_erpnext.doctype.consignment_stock_entry.consignment_stock_entry.get_open_count',
		args: {customer:frm.doc.name},
		callback: function(r) {
			frm.dashboard.set_badge_count("Consignment Stock Entry", r.message.open_count, r.message.total_count);
		}
	})
}

frappe.templates["dashboard_link_doctype"] = ' \
	<div class="document-link" data-doctype="{{ doctype }}"> \
		<a class="badge-link small">{{ __(doctype) }}</a> \
		<span class="text-muted small count"></span> \
		<span class="open-notification hidden" title="{{ __("Open {0}", [__(doctype)])}}"></span> \
		<button class="btn btn-new btn-default btn-xs hidden" data-doctype="{{ doctype }}"> \
				<i class="octicon octicon-plus" style="font-size: 12px;"></i> \
		</button>\
	</div>';