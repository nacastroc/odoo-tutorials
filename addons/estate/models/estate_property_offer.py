# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate property offer"
    _order = "price desc"

    active = fields.Boolean("Active", default=True)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline",
                                help="Date on which the offer will expire")
    partner_id = fields.Many2one("res.partner", required=True, copy=False, string="Partner")
    price = fields.Float(string="Price", required=True, help="Price offered by the buyer")
    property_id = fields.Many2one("estate.property", required=True, copy=False, string="Property")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    status = fields.Selection([
        ("refused", "Refused"),
        ("accepted", "Accepted"),
    ], string="Status", help="Status of the offer")
    validity = fields.Integer("Validity (days)", default=7, help="Days the offer will be valid for")

    _sql_constraints = [
        ("property_offer_price_field_positive",
         "CHECK(price > 0)",
         "Offered price must be strictly positive!"),
    ]

    @api.model
    def create(self, vals):
        property_id = self.env["estate.property"].browse(vals["property_id"])
        best_price = property_id.best_price
        # Raise an error if the user tries to create an offer with a lower amount than an existing offer.
        if vals["price"] < best_price:
            raise ValidationError(f'The minimum amount required for new offers is ${best_price}')
        # At offer creation, set the property state to ‘Offer Received’.
        if len(property_id.offer_ids) == 0 or property_id.state == "new":
            property_id.state = "received"
        return super().create(vals)

    @api.constrains("date_deadline")
    def _check_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = fields.Datetime.from_string(record.create_date)
                deadline = fields.Datetime.from_string(record.date_deadline)
                if deadline < create_date:
                    raise ValidationError("Deadline cannot be set before creation date.")

    @api.constrains("status")
    def _check_valid_offer(self):
        for record in self:
            percent90 = record.property_id.expected_price * 0.9
            if record.status == "accepted" and record.price < percent90:
                raise ValidationError(
                    f"The offer by {record.partner_id.name} of ${record.price} is less than 90% of the expected price and cannot be accepted.")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = fields.Datetime.today()
            if type(record.create_date) is not bool:
                create_date = record.create_date
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            create_date = fields.Datetime.today().date()
            if type(record["create_date"]) is not bool:
                create_date = record["create_date"].date()
            record.validity = (record.date_deadline - create_date).days

    @api.onchange("status")
    def _onchange_status(self):
        for record in self:
            if record.status == "accepted":
                self._set_status_accepted()
            else:
                self._set_status_refused()

    def _set_status_accepted(self):
        query = [
            ("property_id", "=", self.property_id.id),
        ]

        # Validate for object edit
        if self.id:
            query.append(("id", "!=", self.id))

        # First, set all other records to "refused"
        other_records = self.env["estate.property.offer"].search(query)
        other_records.write({"status": "refused"})

        # Set property price, buyer and state
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id
        self.property_id.state = "accepted"

    def _set_status_refused(self):
        query = [
            ("property_id", "=", self.property_id.id),
            ("status", "=", "accepted"),
        ]

        # Validate object edit
        if self.id:
            query.append(("id", "!=", self.id))

        # First, search for records of status "accepted"
        accepted_records = self.env["estate.property.offer"].search(query)

        if len(accepted_records) <= 0:
            # Set property price, buyer and state
            self.property_id.selling_price = 0
            self.property_id.partner_id = False
            self.property_id.state = "received"

    def action_accept(self):
        for record in self:
            if not record.status:
                record.status = "accepted"
                self._set_status_accepted()
        return True

    def action_refuse(self):
        for record in self:
            if not record.status:
                record.status = "refused"
                self._set_status_refused()
        return True
