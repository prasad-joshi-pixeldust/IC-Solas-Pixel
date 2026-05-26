// Copyright (c) 2026, Prasad Joshi and contributors
// Override the Chart of Accounts tree "Add Child" dialog to auto-suggest
// the next account_number from the COA Numbering Scheme.

const SUGGEST_METHOD =
	"ic_solas_pixel.ic_solas_pixel.doctype.coa_numbering_scheme.coa_numbering_scheme.suggest_next_account_code";

// Patch the tree view to auto-suggest account numbers in the "Add Child" dialog.
// The COA tree dialog does NOT have a parent_account field — the parent comes
// from the selected tree node.  We intercept *after* the dialog is shown by
// monkey-patching frappe.ui.Dialog.prototype.show so that whenever a dialog
// with an account_number field appears on the Tree/Account route, we fire the
// suggest call.

(function () {
	const _origShow = frappe.ui.Dialog.prototype.show;
	frappe.ui.Dialog.prototype.show = function () {
		_origShow.apply(this, arguments);

		// Only act on the COA tree route
		if (frappe.get_route_str() !== "Tree/Account") return;

		const dlg = this;
		const number_field = dlg.fields_dict && dlg.fields_dict.account_number;
		if (!number_field) return;

		// Already has a value — skip
		if (number_field.get_value()) return;

		const me = frappe.views.trees && frappe.views.trees["Account"];
		if (!me) return;

		const selected = me.tree && me.tree.get_selected_node();
		if (!selected || !selected.label) return;

		const parent_account = selected.label;
		const company =
			me.args.company ||
			(dlg.fields_dict.company && dlg.fields_dict.company.get_value()) ||
			frappe.defaults.get_user_default("Company");

		if (parent_account && company) {
			frappe.call({
				method: SUGGEST_METHOD,
				args: { parent_account, company },
				callback: (r) => {
					if (r.message && !number_field.get_value()) {
						number_field.set_value(r.message);
					}
				},
			});
		}
	};
})();
