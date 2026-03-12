# -*- coding: utf-8 -*-
{
    'name': 'Invoice with Stock Validation',
    'version': '18.0.0.0.0',
    'summary': 'Automatically creates and validates stock pickings upon invoice/bill validation.',
    'description': """
Stock Validation with Invoice
=============================
This module automates stock operations when an invoice is validated.
Key Features:
- Direct Invoice Validation: Automatically creates a Delivery Picking and validates it to reduce stock.
- Vendor Bill Validation: Automatically creates an Incoming Picking and validates it to increase stock.
- Customer Refund (Credit Note): Automatically creates a Return Picking to add items back to stock.
- Vendor Refund: Automatically creates a Return Picking to reduce stock for returned items.
    """,
    'author': 'CodeTrade India Pvt. Ltd.',
    'website': 'https://www.codetrade.io',
    'category': 'Inventory/Inventory',
    'depends': ['account', 'stock'],
    'data': [
        'views/account_move_views.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'price': 40.00,
    'currency': 'EUR',
  
}
