# Copyright (c) 2026, Prasad Joshi and contributors
# For license information, please see license.txt

"""Install and verify IC Solas Pixel COA templates.

ERPNext discovers COA templates by scanning its own ``verified/`` folder for
JSON files whose filename starts with the country code.  We create symlinks
from ERPNext's ``verified/`` directory to our template JSONs so that ERPNext
picks them up automatically when the country is set to UAE (country_code "ae").

Both ``install_coa_symlink`` and ``verify_template_visible`` are idempotent —
safe to call repeatedly (after_install, after_migrate, or manually).
"""

import os

import frappe

TEMPLATE_NAME = "IC Solas Pixel 6-Digit"
TEMPLATE_FILENAME = "ae_ic_solas_pixel_6_digit.json"

COA_TEMPLATES = [
    (TEMPLATE_NAME, TEMPLATE_FILENAME),
]


def _source_path(filename=None):
    """Absolute path to a COA JSON inside our app."""
    return os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "chart_of_accounts",
        filename or TEMPLATE_FILENAME,
    )


def _target_dir():
    """ERPNext's ``verified/`` COA template directory."""
    import erpnext

    return os.path.join(
        os.path.dirname(erpnext.__file__),
        "accounts",
        "doctype",
        "account",
        "chart_of_accounts",
        "verified",
    )


def _create_symlink(source_path, target_path, label=""):
    """Create a single symlink. Returns True on success."""
    source = os.path.realpath(source_path)
    if not os.path.isfile(source):
        frappe.log_error(f"IC Solas Pixel COA template not found at {source}", "COA Setup")
        print(f"[coa_setup] ERROR: source template not found: {source}")
        return False

    if os.path.islink(target_path):
        if os.path.realpath(target_path) == source:
            print(f"[coa_setup] Symlink already correct: {label}")
            return True
        os.unlink(target_path)

    if os.path.isfile(target_path):
        print(f"[coa_setup] WARNING: replacing real file with symlink: {label}")
        os.unlink(target_path)

    os.symlink(source, target_path)
    print(f"[coa_setup] Created symlink: {label}")
    return True


def install_coa_symlink():
    """Create symlinks so ERPNext discovers IC Solas Pixel COA templates for UAE.

    Idempotent: skips if the links already exist and point to the right files.
    """
    target_dir = _target_dir()
    ok = True
    for name, filename in COA_TEMPLATES:
        source = _source_path(filename)
        target = os.path.join(target_dir, filename)
        if not _create_symlink(source, target, label=name):
            ok = False
    return ok


def verify_template_visible():
    """Confirm ERPNext discovers IC Solas Pixel COA templates for UAE companies.

    Returns True if the primary template is visible, False otherwise.
    """
    from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import (
        get_charts_for_country,
    )

    charts = get_charts_for_country("United Arab Emirates", with_standard=True)
    all_ok = True
    for name, _ in COA_TEMPLATES:
        if name in charts:
            print(f"[coa_setup] OK — '{name}' visible in UAE templates")
        else:
            print(f"[coa_setup] MISSING — '{name}' NOT in UAE templates: {charts}")
            all_ok = False
    return all_ok


# ---------------------------------------------------------------------------
# Fallback registration via override when symlinks aren't possible
# (e.g. Frappe Cloud deployed environments where ERPNext is read-only).
# ---------------------------------------------------------------------------

@frappe.whitelist()
def override_get_charts_for_country(country, with_standard=False):
    """Wrapper that appends IC Solas Pixel COA templates for UAE countries.

    This is registered as an override_whitelisted_method so that even without
    symlinks the templates appear in the Company creation wizard.
    """
    from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import (
        get_charts_for_country as _original,
    )

    charts = _original(country, with_standard=with_standard)
    if not isinstance(charts, list):
        charts = list(charts) if charts else []

    # Only inject for UAE / ae countries
    country_lower = (country or "").lower()
    if country_lower in ("united arab emirates", "ae", "uae"):
        for name, filename in COA_TEMPLATES:
            if name not in charts:
                charts.append(name)

    return charts
