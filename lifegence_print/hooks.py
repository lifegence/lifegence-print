app_name = "lifegence_print"
app_title = "Lifegence Print"
app_publisher = "Lifegence"
app_description = "Japanese print templates for Lifegence Company OS"
app_email = "info@lifegence.co.jp"
app_license = "mit"

required_apps = ["frappe", "erpnext"]

export_python_type_annotations = True

after_install = "lifegence_print.install.after_install"

add_to_apps_screen = [
	{
		"name": "lifegence_print",
		"logo": "/assets/lifegence_print/images/print-logo.svg",
		"title": "\u5e33\u7968\u30c7\u30b6\u30a4\u30f3",
		"route": "/app/print-design",
	},
]

fixtures = [
	"Print Design Settings",
	{
		"dt": "Paper Format JP",
		"filters": [["format_name", "like", "%"]],
	},
]
