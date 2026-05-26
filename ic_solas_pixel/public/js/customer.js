// Copyright (c) 2026, Prasad Joshi and contributors
// Filter "Allowed To Transact With" child table to exclude represents_company.

frappe.ui.form.on("Customer", {
	refresh(frm) {
		frm.set_query("company", "companies", () => ({
			filters: { name: ["!=", frm.doc.represents_company] },
		}));
	},
});
