# 📦 Invoice with Stock Validation, Automatic Picking & Stock Automation

An Odoo add-on that enables real-time **automatic stock validation** when invoices or bills are confirmed, ensuring inventory and accounting are always in sync without manual overhead.

---

## 📦 Module Information

| Key          | Value                                    |
|--------------|------------------------------------------|
| **Name**     | Invoice with Stock Validation            |
| **Version**  | 18.0.0.0.0                               |
| **Author**   | CodeTrade India Pvt. Ltd.                |
| **Category** | Inventory/Inventory                      |
| **License**  | LGPL-3                                   |
| **Odoo**     | v18.0                                    |
| **Support**  | support@codetrade.io                     |

---

## 📖 Overview

Efficiency is key to business operations. This module automates the link between accounting and inventory by instantly validating stock movements upon invoice confirmation.

- **Instant Stock Updates**: Real-time stock reduction or increase when validating invoices/bills.
- **Automated Workflow**: Automatically creates and validates Delivery Orders or Receipts.
- **Refund Synchronization**: Correctly handles Credit Notes by creating and validating return pickings.
- **Improved Efficiency**: Removes the manual step of going to the Inventory app to validate deliveries or receipts for simple, direct invoicing flows.

---

## ⚡ Key Features

- 📦 **Automated Delivery Picking** – For direct customer invoices, an outgoing stock picking is automatically created and validated upon invoice validation.
- 📦 **Automated Receipt Invoicing** – Validating vendor bills automatically generates an incoming stock picking (Receipt).
- 🔄 **Graceful Refund Handling** – Customer refunds and vendor refunds create the appropriate return stock moves.
- ⚡ **No Duplicates** – Intelligently skips invoices derived from Sales Orders or Purchase Orders to prevent double stock movements.
- ⏱️ **Automatic Calculations** – Stock movements are calculated and validated instantly on invoice confirmation.

---

## 🎯 Use Cases

- Retailers performing direct invoicing where stock needs to be updated immediately without warehouse intervention.
- Small businesses with simplified workflows that don't use separate picking/packing processes.
- Accounting departments that want to ensure every validated invoice has a corresponding stock move.
- Service companies selling physical goods occasionally through direct billing.

---

## 🛠️ Installation

1. Download or clone the repository into your Odoo `addons` folder.

2. Restart Odoo server:

```bash
./odoo-bin -c odoo.conf -u invoice_with_stock_move_18
```

3. Activate the module from the **Apps** menu.

---

## 📂 Module Structure

```
invoice_with_stock_move_18/
├── __init__.py
├── __manifest__.py
│
├── models/
│   ├── __init__.py
│   └── account_move.py
│
├── static/
│   └── description/
│       └── index.html
│
└── README.md
```

---

## 📜 License

This module is licensed under the **LGPL-3 License**.

## ⚡ This version is **ready-to-use on Odoo 18**
