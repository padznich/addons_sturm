# -*- coding: utf-8 -*-
##############################################
#
###############################################

{
    "name": "List price for PrestaShop",
    "summary": "Recalculate Sale price in product template",
    "version": "8.0.1.0",
    "category": "Products",
    "website": "softin.cloud",
    "author": "padznich",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase",
    ],
    "data": [
        "views/product_template_extend.xml",
        "views/partner_extend.xml",
    ],
}
