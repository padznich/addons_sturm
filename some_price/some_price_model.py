# -*- coding: utf-8 -*-

from math import ceil

import openerp.addons.decimal_precision as dp
from openerp import api, models, fields


class SomePrice(models.Model):
    _inherit = 'product.template'

    @api.one
    @api.onchange('cost_price')
    def _compute_list_price(self, quantity=1):

        try:
            partner_id = int(self.seller_id.id)
        except IndexError:
            partner_id = 1

        partner = self.env.user.partner_id.browse([partner_id])
        pricelist = partner.property_product_pricelist

        if not pricelist:
            return 0.0

        # sql = 'UPDATE product_template ' \
        #       'SET list_price = {list_price} ' \
        #       'WHERE id = {id}'
        #
        _price = ceil(pricelist.price_get(self.id, quantity, partner)[pricelist.id])
        #
        # self._cr.execute(sql.format(list_price=_price,
        #                             id=self.id))

        self.write({'list_price': _price,
                    'some_price': _price})

    some_price = fields.Float(compute='_compute_list_price', string='Some price',
                              digits_compute=dp.get_precision('Product Price'))

    @api.one
    def update_list_prices(self):

        quantity = 1

        for record in self:

            try:
                partner_id = int(record.seller_id.id)
            except IndexError:
                partner_id = 1

            partner = self.env.user.partner_id.browse([partner_id])
            pricelist = partner.property_product_pricelist

            # must use pricelist
            if not pricelist:
                return 0.0

            sql = 'UPDATE product_template ' \
                  'SET list_price = {list_price} ' \
                  'WHERE id = {id}'

            _price = ceil(pricelist.price_get(record.id, quantity, partner)[pricelist.id])

            record._cr.execute(sql.format(list_price=_price,
                                          id=record.id))
            self.env.invalidate_all()

            # self.write({'list_price': _price})


# class res_partner(models.Model):
#     _inherit = 'res.partner'
#
#     @api.one
#     # @api.depends('property_product_pricelist')
#     def update_list_prices(self):
#
#         products = self.env['product.template']
#
#         quantity = 1
#
#         for record in products:
#
#             try:
#                 partner_id = int(record.seller_id.id)
#             except IndexError:
#                 partner_id = 1
#
#             partner = self.env.user.partner_id.browse([partner_id])
#             pricelist = partner.property_product_pricelist
#
#             # must use pricelist
#             if not pricelist:
#                 return 0.0
#
#             _price = ceil(pricelist.price_get(record.id, quantity, partner)[pricelist.id])
#
#             # record.write({'list_price': _price})
#             sql = 'UPDATE product_template ' \
#                   'SET list_price={list_price} ' \
#                   'WHERE id={id}'.format(list_price=_price, id=record.id)
#
#             self._cr.execute(sql)
#             self.env.invalidate_all()



'''
#
#CURSOR for updating DB
#
sql = 'UPDATE product_template '\
      'SET list_price = {list_price} '\
      'WHERE id = {id}'
self._cr.execute(sql.format(list_price=(pricelist.price_get(self.id, quantity, partner)[pricelist.id]),
                            id=self.id))
'''
