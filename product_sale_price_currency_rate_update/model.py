# -*- coding: utf-8 -*-

import logging

from openerp import api, models


_logger = logging.getLogger(__name__)


class ListPriceCurrencyUpdate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def update_list_prices_currency(self):

        # Currencies sorted From recent
        # Default is USD
        currency_objects = self.env['res.currency.rate'].search([('currency_id', '=', 3)]).sorted(key=lambda r: -r.id)

        for record in self.search([('active', '=', True)]):

            _logger.info('\033[1;32m{}\033[1;m'.format("\nproduct id={} {} updated on {}\n".format(
                record.id, record.name, record.write_date)))

            old_currency_rate = None
            for cur_rate in currency_objects:
                # finding the actual currency rate on the date when product was updated
                if cur_rate.write_date <= record.write_date:
                    old_currency_rate = cur_rate.rate
                    _logger.info('\033[1;32m\nCurrency rate date: {} \nProduct last update: {}\033[1;m'.format(
                        cur_rate.write_date,
                        record.write_date))
                    break

            old_currency_rate = old_currency_rate or currency_objects[0].rate
            currency_differences = (currency_objects[0].rate - old_currency_rate) / 100.0
            if currency_differences < 0:
                currency_differences = 0.0

            _logger.info('\033[1;32m\nOld currency rate: {}\nNew currency rate: {} \033[1;m'.format(
                old_currency_rate,
                currency_objects[0].rate) +
                         '\033[1;32m\ncurrency_differences: {} \033[1;m'.format(currency_differences))

            updated_price = record.standard_price * (1 + currency_differences)

            _logger.info('\033[1;32m\nCost price for {}: {} \033[1;m'.format(record.name, record.standard_price) +
                         '\033[1;32m\nUpdated Cost price for {}: {} \033[1;m'.format(record.name, updated_price))

            record.standard_price = updated_price

            _logger.info('\033[1;32m\nNew written Cost price for {}: {}\n\033[1;m'.format(
                record.name,
                record.standard_price))
