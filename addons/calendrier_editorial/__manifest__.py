{
    'name': 'calendrier_editorial',
    'version': '1.0',
    'description': 'Calendrier d\'Edition',
    'summary': 'calendrier_edition',
    'author': 'Esklab',
    'license': 'LGPL-3',
    'category': 'Calendrier',
    'depends': [
        'base','project','hr'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/calendrier_view.xml',
        'views/publication_view.xml',
    ],

    'auto_install': False,
    'application': False,
}