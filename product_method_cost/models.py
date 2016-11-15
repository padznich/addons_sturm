# -*- coding: utf-8 -*-

import logging

from openerp import api, models


_logger = logging.getLogger(__name__)


class UpdateCostMethod(models.Model):
    _inherit = "product.template"

    @api.multi
    def update_cost_method_to_real(self):
        for record in self.env['product.product'].search([('active', '=', True)]):
            try:
                record.write({'cost_method': 'real'})
            except Exception as ex:
                _logger.error('{}'.format(ex.message))
            _logger.info('\033[1;32m{}\033[1;m'.format('\n--' +
                                                       str(record.cost_method) + " for product " +
                                                       str(record.id)))

    @api.multi
    def update_cost_method_to_standard(self):
        for record in self.env['product.product'].search([('active', '=', True)]):
            try:
                record.write({'cost_method': 'standard'})
            except Exception as ex:
                _logger.error('{}'.format(ex.message))
            _logger.info('\033[1;32m{}\033[1;m'.format('\n--' +
                                                       str(record.cost_method) + " for product " +
                                                       str(record.id)))

    @api.multi
    def update_cost_method_to_average(self):
        for record in self.env['product.product'].search([('active', '=', True)]):
            try:
                record.write({'cost_method':  'average'})
            except Exception as ex:
                _logger.error('{}'.format(ex.message))
            _logger.info('\033[1;32m{}\033[1;m'.format('\n--' +
                                                       str(record.cost_method) + " for product " +
                                                       str(record.id)))
