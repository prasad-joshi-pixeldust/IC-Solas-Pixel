# Copyright (c) 2026, Prasad Joshi and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class COANumberingScheme(Document):
	def validate(self):
		self.validate_total_digits()
		self.validate_single_default()
		self.validate_root_type_prefixes_unique()

	def validate_total_digits(self):
		if not self.level_config:
			return
		max_level = max(int(r.digits_used or 0) for r in self.level_config)
		if max_level > int(self.total_digits or 0):
			frappe.throw(
				_("Level uses {0} digits, which exceeds scheme total_digits = {1}").format(
					max_level, self.total_digits
				)
			)

	def validate_single_default(self):
		if not self.is_default:
			return
		existing = frappe.db.get_all(
			"COA Numbering Scheme",
			filters={"is_default": 1, "name": ["!=", self.name or ""]},
			pluck="name",
		)
		if existing:
			frappe.throw(_("Only one COA Numbering Scheme can be marked as default. Currently default: {0}").format(
				existing[0]
			))

	def validate_root_type_prefixes_unique(self):
		seen_roots, seen_prefixes = set(), set()
		for row in self.root_type_prefixes or []:
			if row.root_type in seen_roots:
				frappe.throw(_("Duplicate root_type: {0}").format(row.root_type))
			seen_roots.add(row.root_type)
			if row.prefix in seen_prefixes:
				frappe.throw(_("Duplicate prefix: {0}").format(row.prefix))
			seen_prefixes.add(row.prefix)


def get_default_scheme():
	name = frappe.db.get_value("COA Numbering Scheme", {"is_default": 1}, "name")
	if not name:
		return None
	return frappe.get_doc("COA Numbering Scheme", name)


def _level_for_code(code, scheme):
	"""Given an account_number string, return the level number it sits at in the scheme."""
	if not code:
		return 0
	stripped = str(code).rstrip("0")
	digits_populated = max(len(stripped), 1)
	# Find the level whose digits_used >= digits_populated with smallest gap.
	candidates = sorted(scheme.level_config, key=lambda r: int(r.digits_used))
	for row in candidates:
		if int(row.digits_used) >= digits_populated:
			return int(row.level)
	return int(candidates[-1].level)


@frappe.whitelist()
def suggest_next_account_code(parent_account, company, scheme_name=None):
	"""Suggest the next account number for a new child under the given parent account.

	Usage (client side):
		frappe.call({
			method: "ic_solas_pixel.ic_solas_pixel.doctype.coa_numbering_scheme.coa_numbering_scheme.suggest_next_account_code",
			args: { parent_account, company, scheme_name }
		})
	"""
	if not parent_account or not company:
		return None

	scheme = frappe.get_doc("COA Numbering Scheme", scheme_name) if scheme_name else get_default_scheme()
	if not scheme:
		return None

	parent_code = frappe.db.get_value("Account", parent_account, "account_number") or ""
	parent_level = _level_for_code(parent_code, scheme)
	next_level = parent_level + 1

	level_row = next((r for r in scheme.level_config if int(r.level) == next_level), None)
	# If parent is deeper than the configured levels, fall back to the last level's settings
	if not level_row:
		max_level_row = max(scheme.level_config, key=lambda r: int(r.level)) if scheme.level_config else None
		if not max_level_row:
			return None
		level_row = max_level_row

	existing = frappe.db.sql(
		"""
		SELECT account_number FROM `tabAccount`
		WHERE parent_account = %s AND company = %s AND ifnull(account_number, '') != ''
		ORDER BY LENGTH(account_number) DESC, account_number DESC
		LIMIT 1
		""",
		(parent_account, company),
	)

	total_digits = int(scheme.total_digits)
	increment = int(level_row.increment_by or 1)

	if existing and existing[0][0]:
		try:
			next_int = int(existing[0][0]) + increment
		except ValueError:
			return None
		return str(next_int).zfill(total_digits)

	# No siblings yet -- derive the first child code from parent_code.
	if parent_code:
		try:
			base = int(str(parent_code).ljust(total_digits, "0"))
			return str(base + increment).zfill(total_digits)
		except ValueError:
			return None

	# No parent code: find the root-type prefix.
	root_type = frappe.db.get_value("Account", parent_account, "root_type")
	prefix_row = next(
		(r for r in scheme.root_type_prefixes if r.root_type == root_type),
		None,
	)
	if not prefix_row:
		return None
	return str(prefix_row.prefix).ljust(total_digits, "0")
