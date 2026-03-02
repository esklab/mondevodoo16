{
    'name': 'Stock report',
    'version': '1.0',
    'description': 'Stock report',
    'summary': 'Stock report',
    'author': 'maono',
    'license': 'LGPL-3',
    'category': 'Tools',
    'depends': [
        'base',
        'stock',
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_report_wizard_views.xml",
        "wizards/stock_report_action.xml",
        "reports/stock_report_wizard_report.xml"
    ],
    'auto_install': False,
    'application': True,
}