# 📊 Flexible Chatter - Adjustable & Collapsible

An Odoo add-on that enables **dynamic resizing, repositioning, and collapsing** of the Odoo chatter panel, providing a more flexible and distraction-free workspace for every user.

---

## 📦 Module Information

| Key          | Value                                    |
|--------------|------------------------------------------|
| **Name**     | Flexible Chatter - Adjustable & Collapsible |
| **Version**  | 18.0.0.0.0                               |
| **Author**   | CodeTrade India Pvt. Ltd.                |
| **Category** | Extra Tools                              |
| **License**  | LGPL-3                                   |
| **Odoo**     | v18.0                                    |
| **Support**  | support@codetrade.io                     |

---

## 📖 Overview

The default Odoo chatter is static and can sometimes feel restrictive. This module turns the chatter into a dynamic, user-configurable panel — giving every team member the workspace they prefer without changing anything for anyone else.

- **Dynamic Workspace**: Switch between side and bottom layouts instantly from user preferences.
- **Improved Focus**: Collapse the chatter with one click to focus on data entry, or expand it for deep communication.
- **Personalized Experience**: Remembers your preferred width, position, and collapsed state per record.
- **Sleek UI**: Modern resizer handles and floating buttons for a seamless and premium feel.

---

## ⚡ Key Features

- ↕ **Dynamic Positioning** – Switch between Side and Bottom chatter modes instantly from your user settings.
- ↔ **Resizable Side Panel** – Drag to adjust the chatter width from 300px to 1000px. Perfect for reading long message threads.
- 👁 **One-Click Collapse** – Hide the chatter instantly. A floating action button remains for quick restoration.
- 🖥 **Full-Width Bottom Mode** – Form and chatter expand to fill the entire screen for better readability.
- 💾 **User Persistence** – Your preferred layout settings are saved automatically and restored across sessions.
- 🛠 **Native Odoo Feel** – Seamlessly integrated into Odoo 18's FormRenderer and Chatter components.

---

## 🎯 Use Cases

- **Focus Mode**: Collapse the chatter when doing heavy data entry to avoid distractions.
- **Large Screens**: Use 'Bottom' mode on ultra-wide monitors to prevent the chatter from being too far from the form.
- **Review Mode**: Use the 'Side' mode and expand the width to read long log notes and emails side-by-side with the record.

---

## 🛠️ Installation

1. Download or clone the repository into your Odoo `addons` folder.

2. Restart Odoo server:

```bash
./odoo-bin -c odoo.conf -u flexible_chatter_18
```

3. Activate the module from the **Apps** menu.

---

## 📂 Module Structure

```
flexible_chatter_18/
├── __init__.py
├── __manifest__.py
│
├── models/
│   ├── __init__.py
│   └── res_users.py
│
├── static/
│   ├── description/
│   │   ├── icon.png
│   │   ├── index.html
│   │   └── images/
│   │       ├── setup.png
│   │       ├── side.png
│   │       └── bottom.png
│   └── src/
│       ├── js/
│       │   └── chatter.js
│       ├── scss/
│       │   └── chatter.scss
│       └── xml/
│           └── chatter.xml
│
└── views/
    └── res_users_views.xml
```

---

## 📜 License

This module is licensed under the **LGPL-3 License**.

## ⚡ This version is **ready-to-use on Odoo 18**
