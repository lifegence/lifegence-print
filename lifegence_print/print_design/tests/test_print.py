# Copyright (c) 2026, Lifegence and contributors
# For license information, please see license.txt

"""
Tests for Lifegence Print App

Covers Print Design Settings defaults, Paper Format JP seeding,
template creation with elements, company stamp, and print batch.
"""

import frappe
from frappe.tests.utils import FrappeTestCase


def _ensure_roles():
	"""Ensure Print Designer and Print User roles exist."""
	for role_name in ("Print Designer", "Print User"):
		if not frappe.db.exists("Role", role_name):
			frappe.get_doc({
				"doctype": "Role",
				"role_name": role_name,
				"desk_access": 1,
			}).insert(ignore_permissions=True)


def _ensure_paper_formats():
	"""Ensure paper formats are seeded for tests."""
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


def _ensure_settings():
	"""Ensure Print Design Settings singleton has defaults."""
	settings = frappe.get_single("Print Design Settings")
	if not settings.default_paper_format:
		settings.default_paper_format = "A4"
		settings.default_margin_top = 10
		settings.default_margin_bottom = 10
		settings.default_margin_left = 15
		settings.default_margin_right = 15
		settings.enable_company_stamp = 1
		settings.save(ignore_permissions=True)


class TestPrintDesignSettings(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		_ensure_roles()
		_ensure_paper_formats()
		_ensure_settings()

	def test_settings_defaults(self):
		"""Verify Print Design Settings has correct default values."""
		settings = frappe.get_single("Print Design Settings")
		self.assertEqual(settings.default_paper_format, "A4")
		self.assertEqual(settings.default_orientation or "Portrait", "Portrait")
		self.assertEqual(settings.default_margin_top, 10)
		self.assertEqual(settings.default_margin_bottom, 10)
		self.assertEqual(settings.default_margin_left, 15)
		self.assertEqual(settings.default_margin_right, 15)
		self.assertEqual(settings.enable_company_stamp, 1)


class TestPaperFormatJP(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		_ensure_roles()
		_ensure_paper_formats()

	def test_paper_format_seed(self):
		"""Verify all 6 paper formats are seeded correctly."""
		expected = ["A4", "A3", "B5", "B4", "\u306f\u304c\u304d", "\u9577\u5f623\u53f7"]
		for name in expected:
			self.assertTrue(
				frappe.db.exists("Paper Format JP", name),
				f"Paper format '{name}' should exist",
			)

		a4 = frappe.get_doc("Paper Format JP", "A4")
		self.assertEqual(a4.width_mm, 210)
		self.assertEqual(a4.height_mm, 297)
		self.assertEqual(a4.is_default, 1)

		hagaki = frappe.get_doc("Paper Format JP", "\u306f\u304c\u304d")
		self.assertEqual(hagaki.width_mm, 100)
		self.assertEqual(hagaki.height_mm, 148)


class TestPrintTemplateJP(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		_ensure_roles()
		_ensure_paper_formats()

	def test_template_creation(self):
		"""Create a template with elements and verify it persists."""
		doc = frappe.get_doc({
			"doctype": "Print Template JP",
			"template_name": "\u30c6\u30b9\u30c8\u8acb\u6c42\u66f8",
			"template_type": "\u8acb\u6c42\u66f8",
			"paper_format": "A4",
			"orientation": "Portrait",
			"is_active": 1,
			"elements": [
				{
					"element_type": "Text",
					"label": "\u8acb\u6c42\u66f8",
					"static_value": "\u8acb\u6c42\u66f8",
					"pos_x": 80,
					"pos_y": 10,
					"width": 50,
					"height": 10,
					"font_size": 18,
					"font_weight": "Bold",
					"text_align": "Center",
				},
				{
					"element_type": "Field",
					"label": "\u5408\u8a08\u91d1\u984d",
					"field_name": "grand_total",
					"pos_x": 120,
					"pos_y": 80,
					"width": 60,
					"height": 10,
					"font_size": 14,
					"font_weight": "Bold",
					"text_align": "Right",
				},
			],
		})
		doc.insert(ignore_permissions=True)
		self.addCleanup(lambda: frappe.delete_doc("Print Template JP", doc.name, force=True))

		self.assertTrue(doc.name.startswith("TPL-"))
		self.assertEqual(doc.template_name, "\u30c6\u30b9\u30c8\u8acb\u6c42\u66f8")
		self.assertEqual(len(doc.elements), 2)
		self.assertEqual(doc.elements[0].element_type, "Text")
		self.assertEqual(doc.elements[1].field_name, "grand_total")


class TestCompanyStamp(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		_ensure_roles()

	def test_company_stamp_creation(self):
		"""Create a company stamp and verify fields."""
		# Ensure a test company exists
		company_name = "_Test Company"
		if not frappe.db.exists("Company", company_name):
			company_name = frappe.db.get_value("Company", {}, "name")

		if not company_name:
			self.skipTest("No Company record available for testing")

		doc = frappe.get_doc({
			"doctype": "Company Stamp",
			"stamp_name": "\u30c6\u30b9\u30c8\u4ee3\u8868\u5370",
			"stamp_type": "\u4ee3\u8868\u5370",
			"company": company_name,
			"stamp_image": "/files/test-stamp.png",
			"stamp_width_mm": 25,
			"stamp_height_mm": 25,
		})
		doc.insert(ignore_permissions=True)
		self.addCleanup(lambda: frappe.delete_doc("Company Stamp", doc.name, force=True))

		self.assertTrue(doc.name.startswith("STAMP-"))
		self.assertEqual(doc.stamp_name, "\u30c6\u30b9\u30c8\u4ee3\u8868\u5370")
		self.assertEqual(doc.stamp_type, "\u4ee3\u8868\u5370")
		self.assertEqual(doc.stamp_width_mm, 25)
		self.assertEqual(doc.stamp_height_mm, 25)


class TestPrintBatch(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		_ensure_roles()
		_ensure_paper_formats()

	def test_print_batch_creation(self):
		"""Create a print batch and verify default status."""
		# Create a template first
		tpl = frappe.get_doc({
			"doctype": "Print Template JP",
			"template_name": "\u30d0\u30c3\u30c1\u30c6\u30b9\u30c8\u7528\u30c6\u30f3\u30d7\u30ec\u30fc\u30c8",
			"template_type": "\u8acb\u6c42\u66f8",
			"paper_format": "A4",
			"is_active": 1,
		})
		tpl.insert(ignore_permissions=True)
		self.addCleanup(lambda: frappe.delete_doc("Print Template JP", tpl.name, force=True))

		doc = frappe.get_doc({
			"doctype": "Print Batch",
			"batch_name": "\u30c6\u30b9\u30c8\u30d0\u30c3\u30c1",
			"template": tpl.name,
			"source_doctype": "Sales Invoice",
		})
		doc.insert(ignore_permissions=True)
		self.addCleanup(lambda: frappe.delete_doc("Print Batch", doc.name, force=True))

		self.assertTrue(doc.name.startswith("BATCH-"))
		self.assertEqual(doc.batch_name, "\u30c6\u30b9\u30c8\u30d0\u30c3\u30c1")
		self.assertEqual(doc.status, "Draft")
		self.assertEqual(doc.source_doctype, "Sales Invoice")
