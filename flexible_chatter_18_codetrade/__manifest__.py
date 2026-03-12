{
    'name': 'Flexible Chatter - Adjustable & Collapsible',
    'version': '18.0.0.0.0',        
    'summary': 'Resize, Move and Collapse Odoo Chatter for a distraction-free experience.',
    'description': """
Modern & Flexible Chatter Experience
=====================================
Take full control of your Odoo chatter with this intuitive and lightweight module. Designed to enhance productivity by allowing users to customize their workspace on the fly.

✨ Key Features
--------------
* ↕ **Dynamic Positioning**: Switch between Side and Bottom chatter modes instantly from your user settings.
* ↔ **Resizable Side Panel**: Drag to adjust the chatter width. Perfect for reading long message threads without squeezing the form.
* 👁 **One-Click Collapse**: Hide the chatter with a single click to focus entirely on the form data. A floating button allows you to bring it back instantly.
* 🖥 **Full-Width Bottom Mode**: In bottom mode, the form and chatter expand to fill the entire screen, making it ideal for high-resolution displays.
* 💾 **User Persistence**: Your preferred position, width, and collapsed state are saved automatically for every record you visit.
* 🛠 **Modern Aesthetics**: Sleek resizer handles and floating Action Buttons (FAB) for a premium feel.

🚀 Setup Guide
--------------
1. Install the module from the Odoo Apps menu.
2. Go to your **User Profile** (Top right menu -> My Profile).
3. Navigate to the **Technical Settings** or **Chatter Settings** tab (depending on your Odoo configuration).
4. Set your preferred **Chatter Position** (Side or Bottom).
5. Open any record (Sales, CRM, etc.) and enjoy your new flexible workspace!

💡 Use Cases
------------
* **Focus Mode**: Collapse the chatter when doing heavy data entry to avoid distractions.
* **Large Screens**: Use 'Bottom' mode on ultra-wide monitors to prevent the chatter from being too far from the form.
* **Review Mode**: Use the 'Side' mode and expand the width to read long log notes and emails side-by-side with the record.

Technical Support
-----------------
Developed by codetrade.io. For support or custom features, visit our website at https://www.codetrade.io/
    """,
    'category': 'Extra Tools',
    'author': 'codetrade.io',
    'website': 'https://www.codetrade.io/',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'views/res_users_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'flexible_chatter_18_codetrade/static/src/scss/chatter.scss',
            'flexible_chatter_18_codetrade/static/src/js/chatter.js',
            'flexible_chatter_18_codetrade/static/src/xml/chatter.xml',
        ],
    },
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 40.00,
    'currency': 'USD',
}
