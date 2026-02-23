{
    'name': 'geschool',
    'version': '1.0',
    'description': 'Gestion Ecole',
    'summary': 'gesecole',
    'author': 'Esklab',
    'license': 'LGPL-3',
    'category': 'School',
    'depends': [
        'base',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/etudiant_view.xml', 
        'views/classe_view.xml',
        'views/cours_view.xml',
        'views/enseignant_view.xml',
        'views/notes_view.xml',
        'views/parent_view.xml',
    ],
    
    'images': ['static\school_img.png'],
    'auto_install': False,
    'application': False,
}