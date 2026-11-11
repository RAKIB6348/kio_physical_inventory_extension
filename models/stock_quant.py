# -*- coding: utf-8 -*-

from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_categ_id = fields.Many2one(
        "product.category",
        string="Product Category",
        related="product_id.categ_id",
        store=True,
        readonly=True,
        index=True,
    )
