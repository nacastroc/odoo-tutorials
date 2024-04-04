# -*- coding: utf-8 -*-
from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "sequence, name, id"

    active = fields.Boolean("Active", default=True)
    name = fields.Char(string="Type", required=True, translate=True, help="The property type")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types.")

    _sql_constraints = [
        ("property_type_name_field_unique",
         "unique(name)",
         "Choose another value - property type name has to be unique!")
    ]
