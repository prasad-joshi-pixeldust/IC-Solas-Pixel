app_name = "ic_solas_pixel"
app_title = "IC Solas Pixel"
app_publisher = "Prasad Joshi"
app_description = "IC Solas Pixel - Custom Frappe App"
app_email = "prasad@pixeldust.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "ic_solas_pixel",
# 		"logo": "/assets/ic_solas_pixel/logo.png",
# 		"title": "IC Solas Pixel",
# 		"route": "/ic_solas_pixel",
# 		"has_permission": "ic_solas_pixel.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ic_solas_pixel/css/ic_solas_pixel.css"
app_include_js = "ic_solas_pixel.bundle.js"

# include js, css files in header of web template
# web_include_css = "/assets/ic_solas_pixel/css/ic_solas_pixel.css"
# web_include_js = "/assets/ic_solas_pixel/js/ic_solas_pixel.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ic_solas_pixel/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ic_solas_pixel/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ic_solas_pixel.utils.jinja_methods",
# 	"filters": "ic_solas_pixel.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ic_solas_pixel.install.before_install"
after_install = "ic_solas_pixel.setup.coa_setup.install_coa_symlink"
after_migrate = "ic_solas_pixel.setup.coa_setup.install_coa_symlink"

# Fixtures
# --------

fixtures = [
	{
		"dt": "Custom Field",
		"filters": [["module", "in", ["IC Solas Pixel"]]],
	},
]

# Uninstallation
# ------------

# before_uninstall = "ic_solas_pixel.uninstall.before_uninstall"
# after_uninstall = "ic_solas_pixel.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ic_solas_pixel.utils.before_app_install"
# after_app_install = "ic_solas_pixel.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ic_solas_pixel.utils.before_app_uninstall"
# after_app_uninstall = "ic_solas_pixel.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ic_solas_pixel.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

doc_events = {
	"Customer": {
		"on_update": "ic_solas_pixel.ic_solas_pixel.overrides.internal_party.sync_ic_mapping",
	},
	"Supplier": {
		"on_update": "ic_solas_pixel.ic_solas_pixel.overrides.internal_party.sync_ic_mapping",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ic_solas_pixel.tasks.all"
# 	],
# 	"daily": [
# 		"ic_solas_pixel.tasks.daily"
# 	],
# 	"hourly": [
# 		"ic_solas_pixel.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ic_solas_pixel.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ic_solas_pixel.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ic_solas_pixel.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts.get_charts_for_country": "ic_solas_pixel.setup.coa_setup.override_get_charts_for_country",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ic_solas_pixel.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ic_solas_pixel.utils.before_request"]
# after_request = ["ic_solas_pixel.utils.after_request"]

# Job Events
# ----------
# before_job = ["ic_solas_pixel.utils.before_job"]
# after_job = ["ic_solas_pixel.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ic_solas_pixel.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

