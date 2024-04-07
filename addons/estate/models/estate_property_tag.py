# -*- coding: utf-8 -*-
from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tag"
    _order = "name"

    active = fields.Boolean("Active", default=True)
    name = fields.Char(string="Tag", required=True, translate=True, help="The tag name")
    color = fields.Integer(string='Color')

    _sql_constraints = [
        ("property_tag_name_field_unique",
         "unique(name)",
         "The property tag name has to be unique!")
    ]
