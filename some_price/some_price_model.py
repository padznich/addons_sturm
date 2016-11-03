# -*- coding: utf-8 -*-

from math import ceil

import openerp.addons.decimal_precision as dp
from openerp import api, models, fields

import logging


_logger = logging.getLogger(__name__)


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
            _logger.error('\033[1;32m{}\033[1;m'.format("." * 10 + "list_price wrote in compute_list_price"))
            _logger.error('\033[1;32m{}\033[1;m'.format(self.seller_id.id))
            _logger.error('\033[1;32m{}\033[1;m'.format(self.list_price) + '\tSale Price')

    @api.multi
    def update_list_prices(self):
        _logger.error('\033[1;32m{}\033[1;m'.format('___start from product.template'))

        quantity = 1

        for record in self.search([('active', '=', True)]):
            _logger.error('\033[1;32m{}\033[1;m'.format('___start iterate from product.template'))

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
            _logger.error('\033[1;32m{}\033[1;m'.format("=" * 10 + "list_price wrote in update_list_prices"))
            _logger.error('\033[1;32m{}\033[1;m'.format(record.list_price) + '\tSale Price')


class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def update_list_prices(self):
        _logger.error('\033[1;32m{}\033[1;m'.format('___start from res.partner'))

        products = self.env['product.template'].search([('active', '=', True)])

        quantity = 1

        for record in products:
            _logger.error('\033[1;32m{}\033[1;m'.format('___start iterate from res.partner'))

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
            _logger.error('\033[1;32m{}\033[1;m'.format("+" * 10 + "list_price wrote in update_list_prices"))
            _logger.error('\033[1;32m{}\033[1;m'.format(record.list_price) + '\tSale Price')
