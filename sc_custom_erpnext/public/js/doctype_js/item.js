frappe.ui.form.on("Item", "refresh", function(frm) {
    if (cur_frm.doc.has_variants == 1) {
        frm.add_custom_button(__('Rename Variants'), function() {
            frappe.call({
                "method": "sc_custom_erpnext.sc_custom_erpnext.rename_item_variants.rename_item_variants",
                args: {
                    erpnext_parent_item: frm.doc.name
                }
            })
        });
    }
});