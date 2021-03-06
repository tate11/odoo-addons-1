# coding: utf-8
#   @author Giacom Grasso <giacomo.grasso.82@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_amount_invoiced = fields.Float(
        compute='_get_order_invoice_amount',
        string='Invoiced',
        store=True)

    order_amount_to_invoice = fields.Float(
        compute='_get_order_invoice_amount',
        string='To Invoice',
        store=True)

    order_amount_paid = fields.Float(
        compute='_get_order_paid_amount',
        string='Paid',
        store=True)

    order_amount_to_pay = fields.Float(
        compute='_get_order_paid_amount',
        string='To be paid',
        store=True)

    # key sale orders indicators
    invoiced_on_ordered = fields.Float(
        compute='_get_indicators',
        string='Inv/Ord',
        store=True)
    paid_on_ordered = fields.Float(
        compute='_get_indicators',
        string='Paid/Ord',
        store=True)
    paid_on_invoiced = fields.Float(
        compute='_get_indicators',
        string='Paid/Inv',
        store=True)

    @api.multi
    @api.depends('amount_total', 'order_amount_invoiced', 'order_amount_paid')
    def _get_indicators(self):
        for order in self:

            order.invoiced_on_ordered = 0.0
            order.paid_on_ordered = 0.0
            order.paid_on_invoiced = 0.0

            if order.amount_total > 0:
                order.invoiced_on_ordered = round(order.order_amount_invoiced / order.amount_total, 2)
                order.paid_on_ordered = round(order.order_amount_paid / order.amount_total, 2)

            if order.order_amount_invoiced > 0:
                order.paid_on_invoiced = round(order.order_amount_paid / order.order_amount_invoiced, 2)

    @api.multi
    @api.depends('order_line.amount_invoiced', 'order_line.amount_to_invoice')
    def _get_order_invoice_amount(self):
        """
        Compute the total amount invoiced and the remaining amount to be
        invoiced of the entire sale order
        """
        for order in self:
            amount_invoiced = 0.0
            amount_to_invoice = 0.0

            for line in order.order_line:
                amount_invoiced += line.amount_invoiced
                amount_to_invoice += line.amount_to_invoice

            order.order_amount_invoiced = amount_invoiced
            order.order_amount_to_invoice = amount_to_invoice

    @api.depends('invoice_ids.move_id.line_ids.amount_residual', 'order_line')
    def _get_order_paid_amount(self):
        """
        Compute the total amount paid and the remaining amount
        """
        for order in self:
            amount_paid = 0.0

            for invoice in order.invoice_ids:
                for line in invoice.move_id.line_ids:
                    if line.account_id == invoice.account_id:
                        amount_paid += line.debit - line.amount_residual

            order.order_amount_paid = amount_paid
            order.order_amount_to_pay = order.amount_total - amount_paid