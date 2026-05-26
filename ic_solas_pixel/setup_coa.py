# Copyright (c) 2026, Prasad Joshi and contributors
# For license information, please see license.txt

"""COA template installation helper.

Run via:
    bench --site <site-name> execute ic_solas_pixel.setup_coa.execute
"""

from ic_solas_pixel.setup.coa_setup import install_coa_symlink, verify_template_visible


def execute():
    """Install COA symlinks and verify the template is visible."""
    install_coa_symlink()
    verify_template_visible()
