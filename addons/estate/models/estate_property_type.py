# -*- coding: utf-8 -*-
from odoo import fields, models, api


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "sequence, name, id"

    active = fields.Boolean("Active", default=True)
    name = fields.Char(string="Type", required=True, translate=True, help="The property type")
    offer_ids = fields.One2many("estate.property.offer", compute="_compute_offer_ids", inverse_name="property_type_id")
    offer_ids_count = fields.Integer(string="Offers", compute="_compute_offer_ids_count")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types.")

    _sql_constraints = [
        ("property_type_name_field_unique",
         "unique(name)",
         "The property type name has to be unique!")
    ]

    @api.depends("property_ids.offer_ids")
    def _compute_offer_ids(self):
        for record in self:
            offers = record.property_ids.mapped("offer_ids")
            record.offer_ids = offers

    @api.depends("offer_ids")
    def _compute_offer_ids_count(self):
        for record in self:
            record.offer_ids_count = len(record.offer_ids)
