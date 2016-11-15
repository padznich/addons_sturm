# -*- coding: utf-8 -*-

from math import ceil
import logging

from openerp import api, models


_logger = logging.getLogger(__name__)


class SomePrice(models.Model):
    _inherit = 'product.product'

    @api.multi
    def update_list_prices(self):
        _logger.info('\033[1;32m{}\033[1;m'.format('___start from product.template'))

        quantity = 1

        for record in self.search([('active', '=', True)]):
            _logger.info('\033[1;32m{}\033[1;m'.format('___start iterate from product.template'))

            try:
                partner_id = int(record.seller_id.id)
            except IndexError:
                partner_id = 1

            partner = self.env.user.partner_id.browse([partner_id])
            pricelist = partner.property_product_pricelist

            product_id = None
            try:
                erp_product_ids = self.env['prestashop.product'].search([('erp_template_id', '=', record.id)])
                presta_product_ids = []
                for item in erp_product_ids:
                    presta_product_ids.append(item.erp_product_id)

                _logger.info('\033[1;32m{}\033[1;m'.format("^" * 50 + "erp_product_ids " + str(presta_product_ids)))

                if presta_product_ids:
                    product_id = presta_product_ids[-1]
                else:
                    product_id = record.id
                _logger.info('\033[1;32m{}\033[1;m'.format("=" * 50 + "product_id " + str(product_id)))
                _logger.info('\033[1;32m{}\033[1;m'.format("=" * 50 + "product_id_type " + str(type(product_id))))
            except KeyError:
                pass

            if not pricelist:
                continue

            _price = ceil(pricelist.price_get(product_id or record.id, quantity, partner)[pricelist.id])

            record.write({'list_price': _price})
            _logger.info('\033[1;32m{}\033[1;m'.format(_price) + '\t_price')
            _logger.info('\033[1;32m{}\033[1;m'.format(record.list_price) + '\tSale Price')


class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def update_list_prices(self):
        _logger.info('\033[1;32m{}\033[1;m'.format('\nstart from res.partner'))

        products = self.env['product.product'].search([('active', '=', True)])

        quantity = 1

        for record in products:
            _logger.info('\033[1;32m{}\033[1;m'.format('\nstart iterate from res.partner'))

            try:
                partner_id = int(record.seller_id.id)
            except IndexError:
                partner_id = 1

            partner = self.env.user.partner_id.browse([partner_id])
            pricelist = partner.property_product_pricelist

            product_id = None
            try:
                erp_product_ids = self.env['prestashop.product'].search([('erp_template_id', '=', record.id)])
                presta_product_ids = []
                for item in erp_product_ids:
                    presta_product_ids.append(item.erp_product_id)

                _logger.info('\033[1;32m{}\033[1;m'.format("^" * 50 + "erp_product_ids " + str(presta_product_ids)))

                if presta_product_ids:
                    product_id = presta_product_ids[-1]
                else:
                    product_id = record.id
                _logger.info('\033[1;32m{}\033[1;m'.format("\nproduct_id " + str(product_id)))
            except KeyError:
                pass

            if not pricelist:
                continue

            _price = ceil(pricelist.price_get(product_id or record.id, quantity, partner)[pricelist.id])

            record.write({'list_price': _price})
            _logger.info('\033[1;32m{}\033[1;m'.format(record.list_price) + '\tSale Price')
            _logger.info('\033[1;32m{}\033[1;m'.format(_price) + '\t_price')
