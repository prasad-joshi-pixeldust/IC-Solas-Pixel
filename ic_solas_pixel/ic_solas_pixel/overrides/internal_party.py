# Copyright (c) 2026, Prasad Joshi and contributors
# For license information, please see license.txt

import frappe


def sync_ic_mapping(doc, method):
	"""Auto-populate intercompany_account_mapping on the Company record
	when an internal Customer or Supplier is saved.

	Hooked to on_update for both Customer and Supplier.
	"""
	is_internal = (
		doc.get("is_internal_customer") or doc.get("is_internal_supplier")
	)
	if not is_internal or not doc.get("represents_company"):
		return

	counterparties = [row.company for row in (doc.get("companies") or [])]
	if not counterparties:
		return

	company_doc = frappe.get_doc("Company", doc.represents_company)
	existing = {
		row.company for row in (company_doc.get("intercompany_account_mapping") or [])
	}

	added = False
	for company in counterparties:
		if company not in existing:
			company_doc.append("intercompany_account_mapping", {"company": company})
			added = True

	if added:
		company_doc.flags.ignore_permissions = True
		company_doc.save()
