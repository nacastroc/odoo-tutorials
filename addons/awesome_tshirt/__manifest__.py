# -*- coding: utf-8 -*-
{
    'name': "Awesome Shirt",

    'summary': "The Awesome T-Shirt company's system to manage orders",

    'description': """
        This app helps you to manage a business of printing customized t-shirts
        for online customers. It offers a public page allowing customers to make
        t-shirt orders.

        Note that this is just a toy app intended to learn the javascript
        framework.
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com/",

    'category': 'Productivity',
    'version': '0.1',
    'application': True,
    'installable': True,


    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail', 'awesome_gallery'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'awesome_tshirt/static/src/**/*',
        ],
    }
}
