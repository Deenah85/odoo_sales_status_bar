from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Sale'),
        ('sent', 'Reserved'),
        ('reservation_approved', 'Reservation Approved'),
        ('contracted', 'Contract'),
        ('contract_approved', 'Contract Approved'),
        ('done', 'Collected'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', readonly=True, copy=False, tracking=True)

    def action_confirm_sale(self):
        # Logic to confirm sale
        self.write({'state': 'sent'})

    def action_approve_reservation(self):
        # Logic to approve reservation
        self.write({'state': 'reservation_approved'})

    def action_approve_contract(self):
        # Logic to approve contract
        self.write({'state': 'contract_approved'})

    def action_done(self):
        # Logic to mark as collected
        self.write({'state': 'done'})

    def action_cancel(self):
        # Logic to cancel the sale
        self.write({'state': 'cancel'})

    # Define visibility conditions for buttons based on state
    @api.depends('state')
    def _compute_button_visibility(self):
        for rec in self:
            rec.show_confirm_sale_button = True if rec.state == 'draft' else False
            rec.show_approve_reservation_button = True if rec.state == 'sent' else False
            rec.show_approve_contract_button = True if rec.state == 'reservation_approved' else False
            rec.show_done_button = True if rec.state in ['contracted', 'contract_approved'] else False

    show_confirm_sale_button = fields.Boolean(compute='_compute_button_visibility')
    show_approve_reservation_button = fields.Boolean(compute='_compute_button_visibility')
    show_approve_contract_button = fields.Boolean(compute='_compute_button_visibility')
    show_done_button = fields.Boolean(compute='_compute_button_visibility')
