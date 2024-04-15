# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from dateutil import relativedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Real estate property advertisement"
    _order = "id desc"

    active = fields.Boolean("Active", default=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2, help="Number of bedrooms in the property")
    best_price = fields.Float("Best Offer", compute="_compute_best_price",
                              help="Best price of all offers made for the property")
    date_availability = fields.Date(string="Available From",
                                    default=fields.Datetime.today() + relativedelta.relativedelta(months=3), copy=False,
                                    help="Date when the property becomes available")
    description = fields.Text(string="Description", required=True, translate=True,
                              help="Brief description of the property")
    expected_price = fields.Float(string="Expected Price", required=True, help="Expected price of the property")
    facades = fields.Integer(string="Facades", help="Number of facades of the property")
    garage = fields.Boolean(string="Garage", help="Indicates whether the property has a garage")
    garden = fields.Boolean(string="Garden", help="Indicates whether the property has a garden")
    garden_area = fields.Integer(string="Garden Area (sqm)", default=0, help="Garden area size in square meters")
    garden_orientation = fields.Selection([
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West")],
        string="Garden Orientation", help="Orientation of the garden")
    living_area = fields.Integer(string="Living Area (sqm)", default=0, help="Living area size in square meters")
    name = fields.Char(string="Title", required=True, translate=True, help="The advertised property")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    partner_id = fields.Many2one("res.partner", copy=False, string="Buyer")
    postcode = fields.Char(string="Postcode", size=10, help="Postcode of the property location")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False,
                                 help="Selling price of the property")
    state = fields.Selection([
        ("new", "New"),
        ("received", "Offer Received"),
        ("accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("cancelled", "Cancelled"),
    ], string="Status", default="new", help="Status of the advertised property")
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area",
                                help="Total area between the living areas and gardens, if any")
    user_id = fields.Many2one("res.users", default=lambda self: self.env.user, string="Salesman")

    _sql_constraints = [
        ("property_expected_price_field_positive",
         "CHECK(expected_price > 0)",
         "The expected price must be strictly positive!"),
    ]

    @api.ondelete(at_uninstall=False)
    def _check_property_state(self):
        states = ["new", "cancelled"]
        for record in self:
            if record.state not in states:
                raise UserError(f"The {record.name} property cannot be deleted since its neither new nor cancelled")

    @api.ondelete(at_uninstall=False)
    def _unlink_offers(self):
        for record in self:
            record.offer_ids.unlink()

    @api.constrains("expected_price")
    def _check_expected_price(self):
        for record in self:
            percent90 = record.expected_price * 0.9
            if 0 < record.selling_price < percent90:
                raise ValidationError("The expected price cannot be over 10% higher than the selling price.")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            offers = record.offer_ids.mapped("price")
            record.best_price = 0 if len(offers) == 0 else max(offers)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if "accepted" not in record.offer_ids.mapped("status"):
                raise UserError("A property cannot be set as sold if no offer has been accepted.")
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be set as sold.")
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be set as cancelled.")
            record.state = "cancelled"
        return True
