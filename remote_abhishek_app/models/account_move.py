import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="Warehouse",
        default=lambda self: self.env["stock.warehouse"].search(
            [("company_id", "=", self.env.company.id)], limit=1
        ),
    )

    picking_type_id = fields.Many2one(
        "stock.picking.type",
        string="Picking Type",
        compute="_compute_picking_type",
        store=True,
    )

    auto_picking = fields.Boolean(
        string="Auto Create Picking",
        default=True
    )

    picking_id = fields.Many2one(
        "stock.picking",
        string="Stock Picking",
        readonly=True,
        copy=False
    )

    picking_count = fields.Integer(
        compute="_compute_picking_count"
    )

    def _compute_picking_count(self):
        for move in self:
            move.picking_count = 1 if move.picking_id else 0

    @api.depends("warehouse_id", "move_type")
    def _compute_picking_type(self):
        for move in self:

            if not move.warehouse_id:
                move.picking_type_id = False
                continue

            if move.move_type == "out_invoice":
                move.picking_type_id = move.warehouse_id.out_type_id

            elif move.move_type == "in_invoice":
                move.picking_type_id = move.warehouse_id.in_type_id

            elif move.move_type == "out_refund":
                move.picking_type_id = move.warehouse_id.out_type_id

            elif move.move_type == "in_refund":
                move.picking_type_id = move.warehouse_id.in_type_id

            else:
                move.picking_type_id = False

    def _has_sale_or_purchase_origin(self):
        self.ensure_one()
        invoice_lines = self.invoice_line_ids
        if not invoice_lines:
            return False
        if "sale_line_ids" in invoice_lines._fields and any(invoice_lines.mapped("sale_line_ids")):
            return True
        if "purchase_line_id" in invoice_lines._fields and any(invoice_lines.mapped("purchase_line_id")):
            return True
        if "purchase_line_ids" in invoice_lines._fields and any(invoice_lines.mapped("purchase_line_ids")):
            return True
        return False

    def _should_auto_create_picking(self):
        self.ensure_one()
        if not self.auto_picking:
            return False
        if self.move_type not in {"out_invoice", "in_invoice", "out_refund", "in_refund"}:
            return False
        if self.picking_id:
            return False
        if self._has_sale_or_purchase_origin():
            return False
        stock_lines = self.invoice_line_ids.filtered(
            lambda l: l.product_id and (l.product_id.type == "product" or getattr(l.product_id, "is_storable", False)) and abs(l.quantity) > 0
        )
        return bool(stock_lines)

    def action_post(self):

        res = super().action_post()

        for move in self:

            if move._should_auto_create_picking():
                move._create_stock_picking()

        return res
        
    def _create_stock_picking(self):

        self.ensure_one()

        if self.picking_id:
            return

        if not self.picking_type_id:
            return

        lines = self.invoice_line_ids.filtered(
            lambda l: l.product_id and (l.product_id.type == "product" or getattr(l.product_id, "is_storable", False)) and abs(l.quantity) > 0
        )

        if not lines:
            return

        default_src = self.picking_type_id.default_location_src_id.id
        default_dest = self.picking_type_id.default_location_dest_id.id
        if self.move_type in {"out_refund", "in_refund"}:
            location_id = default_dest
            location_dest_id = default_src
        else:
            location_id = default_src
            location_dest_id = default_dest

        picking_vals = {
            "partner_id": self.partner_id.id,
            "picking_type_id": self.picking_type_id.id,
            "location_id": location_id,
            "location_dest_id": location_dest_id,
            "origin": self.name,
            "company_id": self.company_id.id,
            "move_type": "direct",
        }

        picking = self.env["stock.picking"].with_context(default_move_type=False).create(picking_vals)

        for line in lines:
            self.env["stock.move"].create({
                "name": line.product_id.display_name,
                "product_id": line.product_id.id,
                "product_uom_qty": abs(line.quantity),
                "product_uom": line.product_uom_id.id,
                "picking_id": picking.id,
                "location_id": picking.location_id.id,
                "location_dest_id": picking.location_dest_id.id,
                "company_id": self.company_id.id,
                "origin": self.name,
            })

        try:
            # Confirm picking
            picking.action_confirm()

            # Reserve stock (assign)
            picking.action_assign()

            # In Odoo 18, move_ids is the preferred field
            moves = picking.move_ids

            # Prepare move lines with quantities
            for move in moves:
                if move.state in ['assigned', 'partially_available', 'confirmed']:
                    if not move.move_line_ids:
                        self.env["stock.move.line"].create({
                            "move_id": move.id,
                            "picking_id": picking.id,
                            "product_id": move.product_id.id,
                            "product_uom_id": move.product_uom.id,
                            "location_id": move.location_id.id,
                            "location_dest_id": move.location_dest_id.id,
                            "quantity": move.product_uom_qty,
                            "picked": True,
                        })
                    else:
                        for move_line in move.move_line_ids:
                            move_line.quantity = move.product_uom_qty

            self._auto_validate_picking(
                picking.with_context(
                    skip_sms=True,
                    skip_picking_confirm_sms=True,
                    tracking_disable=True,
                )
            )

            self.picking_id = picking.id

        except Exception as e:
            # Log the error and keep the picking for manual review
            self.picking_id = picking.id
            _logger.error(f"Error validating picking {picking.name} for invoice {self.name}: {str(e)}")
            raise

    def _auto_validate_picking(self, picking):
        """Validate a picking and auto-handle the returned wizard action if any."""
        action = picking.button_validate()
        if not isinstance(action, dict):
            return

        for _i in range(10):
            if not isinstance(action, dict):
                return

            res_model = action.get("res_model")
            ctx = dict(self.env.context, **(action.get("context") or {}))
            res_id = action.get("res_id")

            if res_model == "stock.immediate.transfer":
                wizard = self.env[res_model].with_context(ctx).browse(res_id) if res_id else self.env[res_model].with_context(ctx).create({})
                action = wizard.process()
                continue

            if res_model == "stock.backorder.confirmation":
                wizard = self.env[res_model].with_context(ctx).browse(res_id) if res_id else self.env[res_model].with_context(ctx).create({})
                if hasattr(wizard, "action_create_backorder"):
                    action = wizard.action_create_backorder()
                elif hasattr(wizard, "process"):
                    action = wizard.process()
                elif hasattr(wizard, "process_cancel_backorder"):
                    action = wizard.process_cancel_backorder()
                else:
                    raise UserError(_("Unable to validate picking automatically (backorder wizard API changed)."))
                continue

            if res_model == "confirm.stock.sms":
                ctx.setdefault("button_validate_picking_ids", picking.ids)
                wizard = self.env[res_model].with_context(ctx).browse(res_id) if res_id else self.env[res_model].with_context(ctx).create({})
                if hasattr(wizard, "action_confirm"):
                    action = wizard.action_confirm()
                else:
                    action = wizard.send_sms()
                continue

            raise UserError(_("Picking validation requires manual action (%s).") % (res_model or _("unknown wizard")))

        raise UserError(_("Unable to validate picking automatically (too many wizard steps)."))

    def action_view_stock_picking(self):

        self.ensure_one()

        if not self.picking_id:
            return {}

        return {
            "name": _("Stock Picking"),
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "view_mode": "form",
            "res_id": self.picking_id.id,
        }
