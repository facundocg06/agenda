{
    'name': 'Agenda Estudiantil',
    'version': '1.0',
    'summary': 'Gestión de agenda estudiantil para enviar comunicados',
    'category': 'Education',
    'author': 'grupo 33',
<<<<<<< HEAD
    'depends': ['base','web'],
=======
    'depends': ['base'],
>>>>>>> 378dedb5270908c731b1b8c1767827670dbdf092
    'data': [ 
        'data/data_seed.xml',       
        'security/ir.model.access.csv',        
        'views/views.xml',
        'views/templates.xml',
        
    ],
    
    'installable': True,
    'application': True,
<<<<<<< HEAD
    'external_dependencies': {
    'python': ['pyfcm'],
    },

    
=======
<<<<<<< HEAD
    
=======
    'post_init_hook': 'create_profesor',
>>>>>>> 03bee8c32dc4c30436ce5d3d5e4d48209881775c
>>>>>>> 378dedb5270908c731b1b8c1767827670dbdf092
}
