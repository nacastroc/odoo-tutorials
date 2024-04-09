from odoo import models


class Property(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # Create invoice with provided values
        self.env['account.move'].sudo().with_context(default_move_type="out_invoice").create({
            "partner_id": self.partner_id.id,
            "invoice_line_ids": [
                (0, 0, {
                    'name': 'Selling Price (6%)',
                    'quantity': 1,
                    'price_unit': self.selling_price * 6 / 100,
                }),
                (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
            ]
        })
        super().action_sold()
