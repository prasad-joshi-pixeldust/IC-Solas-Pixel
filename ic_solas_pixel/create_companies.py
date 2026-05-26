"""Create company structure matching Solas Cloud.

Run via:
    bench --site ic-solas-pixel.local execute ic_solas_pixel.create_companies.execute
"""

import frappe


# Companies that have children (must be marked is_group=1)
GROUP_COMPANIES = {
    "Solas Global (Consolidated)",
    "United Arab Emirates (Consolidated)",
    "Dubai & Northern Emirates (Consolidated)",
    "Abu Dhabi (Consolidated)",
    "Qatar (Consolidated)",
    "Bahrain (Consolidated)",
    "Saudi Arabia (Consolidated)",
    "Oman (Consolidated)",
    "Kuwait (Consolidated)",
    "Singapore (Consolidated)",
    "Regional Entities (Consolidated)",
    "Test Consolidation",
    "Test Group 2",
}

# Ordered by hierarchy level (parents first)
COMPANIES = [
    # Level 0 — root
    {"name": "Solas Global (Consolidated)", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": None, "abbr": "SGLB", "chart_of_accounts": "IC Solas Pixel 6-Digit"},

    # Level 1 — direct children of Solas Global
    {"name": "United Arab Emirates (Consolidated)", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Solas Global (Consolidated)", "abbr": "UAEC"},
    {"name": "Qatar (Consolidated)", "country": "Qatar", "default_currency": "QAR", "parent_company": "Solas Global (Consolidated)", "abbr": "QTC"},
    {"name": "Bahrain (Consolidated)", "country": "Bahrain", "default_currency": "BHD", "parent_company": "Solas Global (Consolidated)", "abbr": "BHC"},
    {"name": "Saudi Arabia (Consolidated)", "country": "Saudi Arabia", "default_currency": "SAR", "parent_company": "Solas Global (Consolidated)", "abbr": "SAC"},
    {"name": "Oman (Consolidated)", "country": "Oman", "default_currency": "OMR", "parent_company": "Solas Global (Consolidated)", "abbr": "OMC"},
    {"name": "Kuwait (Consolidated)", "country": "Kuwait", "default_currency": "KWD", "parent_company": "Solas Global (Consolidated)", "abbr": "KWC"},
    {"name": "Singapore (Consolidated)", "country": "Singapore", "default_currency": "SGD", "parent_company": "Solas Global (Consolidated)", "abbr": "SGC"},
    {"name": "Regional Entities (Consolidated)", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Solas Global (Consolidated)", "abbr": "REC"},
    {"name": "Solas Global - Elimination Subsidiary", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Solas Global (Consolidated)", "abbr": "SOLGE"},
    {"name": "Test Consolidation", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Solas Global (Consolidated)", "abbr": "TC"},
    {"name": "Test Group 2", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Solas Global (Consolidated)", "abbr": "TG2"},

    # Level 2 — sub-groups
    {"name": "Dubai & Northern Emirates (Consolidated)", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "United Arab Emirates (Consolidated)", "abbr": "DNEC"},
    {"name": "Abu Dhabi (Consolidated)", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "United Arab Emirates (Consolidated)", "abbr": "ADC"},
    {"name": "UAE Elimination Subsidiary", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "United Arab Emirates (Consolidated)", "abbr": "UAEE"},

    # Level 3 — operating & elimination entities under Dubai & NE
    {"name": "Dubai & Northern Emirates Elimination Subsidiary", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Dubai & Northern Emirates (Consolidated)", "abbr": "DNEE"},
    {"name": "Solas Marine Services L.L.C.", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Dubai & Northern Emirates (Consolidated)", "abbr": "SMSDXB"},
    {"name": "Solas Marine Group Limited", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Dubai & Northern Emirates (Consolidated)", "abbr": "SMGL"},
    {"name": "Hydrosol Technologies L.L.C.", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Dubai & Northern Emirates (Consolidated)", "abbr": "HTDXB"},

    # Level 3 — operating & elimination entities under Abu Dhabi
    {"name": "Abu Dhabi Elimination Subsidiary", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Abu Dhabi (Consolidated)", "abbr": "ADE"},
    {"name": "Arkan Holding Limited", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Abu Dhabi (Consolidated)", "abbr": "AKHL"},
    {"name": "Solas Marine Services L.L.C. Abu Dhabi", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Abu Dhabi (Consolidated)", "abbr": "SMSAD"},

    # Level 2/3 — Qatar
    {"name": "Qatar Elimination Subsidiary", "country": "Qatar", "default_currency": "QAR", "parent_company": "Qatar (Consolidated)", "abbr": "QTE"},
    {"name": "Solas Marine Services L.L.C. Qatar", "country": "Qatar", "default_currency": "QAR", "parent_company": "Qatar (Consolidated)", "abbr": "SMSQAT"},

    # Level 2/3 — Bahrain
    {"name": "Bahrain Elimination Subsidiary", "country": "Bahrain", "default_currency": "BHD", "parent_company": "Bahrain (Consolidated)", "abbr": "BHE"},
    {"name": "Solas Marine Services (Foreign Branch) Bahrain", "country": "Bahrain", "default_currency": "BHD", "parent_company": "Bahrain (Consolidated)", "abbr": "SMSBAH"},
    {"name": "Bahrain Same Currency", "country": "Bahrain", "default_currency": "BHD", "parent_company": "Bahrain (Consolidated)", "abbr": "TB"},
    {"name": "Bahrain Different Currency", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Bahrain (Consolidated)", "abbr": "BDC"},

    # Level 2/3 — Saudi Arabia
    {"name": "Saudi Arabia Elimination Subsidiary", "country": "Saudi Arabia", "default_currency": "SAR", "parent_company": "Saudi Arabia (Consolidated)", "abbr": "SAE"},
    {"name": "Al Salamah International Trading Co.", "country": "Saudi Arabia", "default_currency": "SAR", "parent_company": "Saudi Arabia (Consolidated)", "abbr": "ASITC"},

    # Level 2/3 — Oman
    {"name": "Oman Elimination Subsidiary", "country": "Oman", "default_currency": "OMR", "parent_company": "Oman (Consolidated)", "abbr": "OME"},
    {"name": "Solas Technical and Marine Co. W.L.L.", "country": "Oman", "default_currency": "OMR", "parent_company": "Oman (Consolidated)", "abbr": "STMOM"},

    # Level 2/3 — Kuwait
    {"name": "Kuwait Elimination Subsidiary", "country": "Kuwait", "default_currency": "KWD", "parent_company": "Kuwait (Consolidated)", "abbr": "KWE"},
    {"name": "Solas Marine Services L.L.C. SP", "country": "Kuwait", "default_currency": "KWD", "parent_company": "Kuwait (Consolidated)", "abbr": "SMSKUW"},
    {"name": "Bahrain Currency in Kuwait", "country": "Kuwait", "default_currency": "BHD", "parent_company": "Kuwait (Consolidated)", "abbr": "BCK"},

    # Level 2/3 — Singapore
    {"name": "Singapore Elimination Subsidiary", "country": "Singapore", "default_currency": "SGD", "parent_company": "Singapore (Consolidated)", "abbr": "SGE"},
    {"name": "Solas Marine Services Pte Ltd", "country": "Singapore", "default_currency": "SGD", "parent_company": "Singapore (Consolidated)", "abbr": "SMSSG"},

    # Level 2/3 — Regional Entities
    {"name": "Regional Elimination Subsidiary", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Regional Entities (Consolidated)", "abbr": "REE"},
    {"name": "Solas Regional Services L.L.C.", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Regional Entities (Consolidated)", "abbr": "SRSRGN"},

    # Level 2/3 — Test companies
    {"name": "Test A", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Test Consolidation", "abbr": "TA"},
    {"name": "Test B", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Test Consolidation", "abbr": "TSB"},
    {"name": "Test Elimination", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Test Consolidation", "abbr": "TE"},
    {"name": "Test C", "country": "United States", "default_currency": "USD", "parent_company": "Test Consolidation", "abbr": "TSC"},
    {"name": "Test D", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Test Group 2", "abbr": "TD"},
    {"name": "Test E", "country": "United Arab Emirates", "default_currency": "USD", "parent_company": "Test Group 2", "abbr": "TES"},
    {"name": "Test Elimination 2", "country": "United Arab Emirates", "default_currency": "AED", "parent_company": "Test Group 2", "abbr": "TE2"},
]


def execute():
    """Create all 46 companies in hierarchy order."""
    root_company = "Solas Global (Consolidated)"
    created = 0
    skipped = 0
    errors = 0

    for c in COMPANIES:
        if frappe.db.exists("Company", c["name"]):
            # Ensure group companies are marked as is_group
            if c["name"] in GROUP_COMPANIES:
                frappe.db.set_value("Company", c["name"], "is_group", 1, update_modified=False)
                frappe.db.commit()
            print(f"  SKIP (exists): {c['name']}")
            skipped += 1
            continue

        try:
            print(f"  Creating: {c['name']} ...")
            doc = frappe.new_doc("Company")
            doc.company_name = c["name"]
            doc.abbr = c["abbr"]
            doc.country = c["country"]
            doc.default_currency = c["default_currency"]
            doc.is_group = 1 if c["name"] in GROUP_COMPANIES else 0

            if c.get("parent_company"):
                doc.parent_company = c["parent_company"]

            # Root company uses the template; all others copy from root
            if c.get("chart_of_accounts"):
                doc.chart_of_accounts = c["chart_of_accounts"]
            else:
                doc.existing_company = root_company

            doc.flags.ignore_permissions = True
            doc.flags.ignore_mandatory = True
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            created += 1
            print(f"  OK: {c['name']}")
        except Exception as e:
            frappe.db.rollback()
            errors += 1
            print(f"  ERROR: {c['name']} — {e}")

    print(f"\nDone. Created: {created}, Skipped: {skipped}, Errors: {errors}, Total: {len(COMPANIES)}")
