# -*- coding: utf-8 -*-

from odoo import api, fields, models


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

    rpu = fields.Monetary(
        string="RPU",
        compute="_compute_pricing_details",
        compute_sudo=True,
        currency_field="currency_id",
        readonly=True,
    )
    total_rpu = fields.Monetary(
        string="Total RPU",
        default=0.0,
        readonly=True,
        currency_field="currency_id",
    )
    total_rpu_with_vat = fields.Monetary(
        string="Total RPU With VAT",
        default=0.0,
        readonly=True,
        currency_field="currency_id",
    )

    @api.depends(
        "product_id",
        "product_id.lst_price",
        "product_id.standard_price",
        "product_id.taxes_id",
        "company_id",
    )
    @api.depends_context("company")
    def _compute_pricing_details(self):
        cache = {}
        for quant in self:
            quant.currency_id = (
                quant.company_id.currency_id or self.env.company.currency_id
            )
            product = quant.product_id
            if not product:
                quant.cost_price = 0.0
                quant.rpu = 0.0
                quant.rpu_without_vat = 0.0
                quant.rpu_with_vat = 0.0
                quant.total_rpu = 0.0
                quant.total_rpu_with_vat = 0.0
                continue

            company = quant.company_id or self.env.company
            key = (product.id, company.id)
            if key not in cache:
                priced_product = product.with_company(company)
                cost_price = priced_product.standard_price
                rpu = priced_product.lst_price
                currency = (
                    quant.currency_id
                    or priced_product.currency_id
                    or company.currency_id
                )
                taxes = priced_product.taxes_id._filter_taxes_by_company(company)
                tax_values = taxes.compute_all(
                    rpu,
                    currency=currency,
                    quantity=1.0,
                    product=priced_product,
                    partner=self.env["res.partner"],
                )
                rpu_without_vat = tax_values["total_excluded"]
                rpu_with_vat = tax_values["total_included"]
                cache[key] = (cost_price, rpu, rpu_without_vat, rpu_with_vat)
            else:
                cost_price, rpu, rpu_without_vat, rpu_with_vat = cache[key]

            quant.cost_price = cost_price
            quant.rpu = rpu
            quant.rpu_without_vat = rpu_without_vat
            quant.rpu_with_vat = rpu_with_vat
            quant.total_rpu = 0.0
            quant.total_rpu_with_vat = 0.0

    @api.model
    def read_group(self, domain, fields, *args, **kwargs):
        # No automatic/footer aggregates for Total RPU columns.
        for name in ("cost_price", "rpu", "rpu_with_vat"):
            if name in fields:
                fields = [f"{name}:sum" if f == name else f for f in fields]
        fields = [
            f for f in fields
            if f not in ("total_rpu", "total_rpu_with_vat")
            and not (isinstance(f, str) and f.startswith("total_rpu:"))
            and not (isinstance(f, str) and f.startswith("total_rpu_with_vat:"))
        ]
        return super().read_group(domain, fields, *args, **kwargs)
