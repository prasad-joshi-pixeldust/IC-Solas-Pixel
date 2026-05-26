// Copyright (c) 2026, Prasad Joshi and contributors
// Auto-suggest account_number based on the default COA Numbering Scheme.

const SUGGEST_METHOD =
	"ic_solas_pixel.ic_solas_pixel.doctype.coa_numbering_scheme.coa_numbering_scheme.suggest_next_account_code";

function suggest_account_number(frm) {
	if (frm.doc.account_number || !frm.doc.parent_account || !frm.doc.company) return;
	frappe.call({
		method: SUGGEST_METHOD,
		args: {
			parent_account: frm.doc.parent_account,
			company: frm.doc.company,
		},
		callback: (r) => {
			if (r.message) {
				frm.set_value("account_number", r.message);
			}
		},
	});
}

frappe.ui.form.on("Account", {
	setup(frm) {
		// When a new Account is opened with parent_account pre-filled (e.g. via URL params)
		if (frm.is_new()) {
			suggest_account_number(frm);
		}
	},
	refresh(frm) {
		// Catch pre-filled parent_account on new records after form renders
		if (frm.is_new() && frm.doc.parent_account && !frm.doc.account_number) {
			suggest_account_number(frm);
		}
	},
	parent_account(frm) {
		suggest_account_number(frm);
	},
});
