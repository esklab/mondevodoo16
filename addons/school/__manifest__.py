{
    'name': 'Gestion d\'ecole',
    'version': '1.0',
    'description': 'Gestion d\'ecole',
    'summary': 'Gestion d\'ecole',
    'author': 'Esk Lab',
    'license': 'LGPL-3',
    'category': 'Ecole',
    'depends': [
        'base','sale_management'
    ],
    "data": [
        "views/eleve_view.xml",
        "security/ir.model.access.csv",
        "views/sale_order.xml",
        "views/ecole_eleve_views.xml"
    ],
    'auto_install': False,
    'application': False,
    'assets': {
        
    }
}