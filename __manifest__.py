{
    'name': 'Agenda Estudiantil',
    'version': '1.0',
    'summary': 'Gestión de agenda estudiantil para enviar comunicados',
    'category': 'Education',
    'author': 'grupo 33',
    'depends': ['base'],
    'data': [        
        'security/ir.model.access.csv',        
        'views/views.xml',
        'views/templates.xml',
        'data/data_seed.xml',
    ],
    'installable': True,
    'application': True,
}
