{
    'name': "Real Estate Advertisement",
    'version': '1.0',
    'depends': ['base'],
    'author': "Nestor Castro",
    'category': 'Marketing',
    'summary': 'Real estate properties advertisement',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3'
}
