# Copyright (c) 2026, Prasad Joshi and contributors
# For license information, please see license.txt

"""Seed the default 'IC Solas Pixel 6-Digit' COA Numbering Scheme."""

import frappe


SCHEME_NAME = "IC Solas Pixel 6-Digit"


def execute():
	if frappe.db.exists("COA Numbering Scheme", SCHEME_NAME):
		return

	doc = frappe.new_doc("COA Numbering Scheme")
	doc.scheme_name = SCHEME_NAME
	doc.total_digits = 6
	doc.is_default = 1
	doc.description = (
		"UAE BRD 6-digit account numbering: "
		"1=Assets, 2=Liabilities, 3=Equity, 4=Revenue, 5=Direct Costs."
	)

	levels = [
		{"level": 1, "level_name": "Root Type", "digits_used": 1, "increment_by": 1, "pad_remaining_with": "0"},
		{"level": 2, "level_name": "Group", "digits_used": 2, "increment_by": 10000, "pad_remaining_with": "0"},
		{"level": 3, "level_name": "Sub-group", "digits_used": 3, "increment_by": 1000, "pad_remaining_with": "0"},
		{"level": 4, "level_name": "Leaf", "digits_used": 6, "increment_by": 5, "pad_remaining_with": "0"},
	]
	for row in levels:
		doc.append("level_config", row)

	prefixes = [
		{"root_type": "Asset", "prefix": "1"},
		{"root_type": "Liability", "prefix": "2"},
		{"root_type": "Equity", "prefix": "3"},
		{"root_type": "Income", "prefix": "4"},
		{"root_type": "Expense", "prefix": "5"},
	]
	for row in prefixes:
		doc.append("root_type_prefixes", row)

	doc.insert(ignore_permissions=True)
	frappe.db.commit()
