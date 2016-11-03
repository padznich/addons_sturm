# -*- coding: utf-8 -*-

from math import ceil

import openerp.addons.decimal_precision as dp
from openerp import api, models, fields


class SomePrice(models.Model):
    _inherit = 'product.template'

    some_price = fields.Float(compute='compute_list_price', string='Some price',
                              digits_compute=dp.get_precision('Product Price'))

    @api.one
    @api.depends('seller_id')
    def compute_list_price(self, quantity=1):

        try:
            partner_id = int(self.seller_id.id)
        except IndexError:
            partner_id = 1

        partner = self.env.user.partner_id.browse([partner_id])
        pricelist = partner.property_product_pricelist

        if not pricelist:
            return 0.0

        _price = ceil(pricelist.price_get(self.id, quantity, partner)[pricelist.id])

        if self.list_price != _price:
            self.write({'list_price': _price})

    @api.multi
    def update_list_prices(self):

        quantity = 1

        for record in self.search([('active', '=', True)]):

            try:
                partner_id = int(record.seller_id.id)
            except IndexError:
                partner_id = 1

            partner = self.env.user.partner_id.browse([partner_id])
            pricelist = partner.property_product_pricelist

            if not pricelist:
                continue

            _price = ceil(pricelist.price_get(record.id, quantity, partner)[pricelist.id])

            record.write({'list_price': _price})


class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def update_list_prices(self):

        products = self.env['product.template'].search([('active', '=', True)])

        quantity = 1

        for record in products:

            try:
                partner_id = int(record.seller_id.id)
            except IndexError:
                partner_id = 1

            partner = self.env.user.partner_id.browse([partner_id])
            pricelist = partner.property_product_pricelist

            if not pricelist:
                continue

            _price = ceil(pricelist.price_get(record.id, quantity, partner)[pricelist.id])

            record.write({'list_price': _price})
