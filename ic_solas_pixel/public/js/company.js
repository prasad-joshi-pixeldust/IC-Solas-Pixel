// Copyright (c) 2026, Prasad Joshi and contributors
// Client script to filter Account link fields in Intercompany Account Mapping child table.

frappe.ui.form.on("Company", {
	refresh(frm) {
		const account_fields = [
			"ic_receivable",
			"ic_payable",
			"ic_revenue",
			"ic_cogs",
			"inventory_in_transit",
			"ic_transfer_clearing",
		];

		account_fields.forEach((fieldname) => {
			frm.set_query(fieldname, "intercompany_account_mapping", (doc, cdt, cdn) => {
				const row = locals[cdt][cdn];
				const filters = { company: frm.doc.name };
				if (row.currency) {
					filters.account_currency = row.currency;
				}
				return { filters };
			});
		});
	},
});
