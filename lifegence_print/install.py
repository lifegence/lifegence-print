import frappe


def after_install():
	_create_roles()
	_seed_paper_formats()
	_init_settings()
	frappe.db.commit()
	print("Lifegence Print: Installation complete.")


def _init_settings():
	frappe.reload_doc("print_design", "doctype", "print_design_settings")
	settings = frappe.get_single("Print Design Settings")
	if not settings.default_paper_format:
		settings.default_paper_format = "A4"
		settings.default_margin_top = 10
		settings.default_margin_bottom = 10
		settings.default_margin_left = 15
		settings.default_margin_right = 15
		settings.enable_company_stamp = 1
		settings.save(ignore_permissions=True)


def _create_roles():
	for role_name in ("Print Designer", "Print User"):
		if not frappe.db.exists("Role", role_name):
			frappe.get_doc({
				"doctype": "Role",
				"role_name": role_name,
				"desk_access": 1,
			}).insert(ignore_permissions=True)


def _seed_paper_formats():
	formats = [
		{"format_name": "A4", "width_mm": 210, "height_mm": 297, "is_default": 1},
		{"format_name": "A3", "width_mm": 297, "height_mm": 420},
		{"format_name": "B5", "width_mm": 182, "height_mm": 257},
		{"format_name": "B4", "width_mm": 257, "height_mm": 364},
		{"format_name": "\u306f\u304c\u304d", "width_mm": 100, "height_mm": 148},
		{"format_name": "\u9577\u5f623\u53f7", "width_mm": 120, "height_mm": 235},
	]
	for fmt in formats:
		if not frappe.db.exists("Paper Format JP", fmt["format_name"]):
			doc = frappe.new_doc("Paper Format JP")
			doc.update(fmt)
			doc.insert(ignore_permissions=True)
