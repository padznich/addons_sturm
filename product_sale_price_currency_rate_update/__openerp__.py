# -*- coding: utf-8 -*-
##############################################
#
###############################################

{
    "name": "Product Sale Price update with Currency rate",
    "summary": "Recalculate Sale price in product template. "
               "Depending on currency rate.",
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
        "views.xml",
        "rules.xml",
    ],
}
