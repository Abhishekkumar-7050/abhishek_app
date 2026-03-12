/** @odoo-module **/

import { Chatter } from "@mail/chatter/web_portal/chatter";
import { FormRenderer } from "@web/views/form/form_renderer";
import { patch } from "@web/core/utils/patch";
import { onMounted, onWillStart, onWillUnmount, useState, useEffect } from "@odoo/owl";
import { user } from "@web/core/user";
import { rpc } from "@web/core/network/rpc";

async function loadChatterPrefs() {
    const defaults = { chatter_position: "side", chatter_width: 450, chatter_collapsed: false };
    try {
        const result = await rpc("/web/dataset/call_kw/res.users/read", {
            model: "res.users",
            method: "read",
            args: [[user.userId], ["chatter_position", "chatter_width", "chatter_collapsed"]],
            kwargs: {},
        });
        if (result && result.length) {
            defaults.chatter_position = result[0].chatter_position || "side";
            defaults.chatter_width = result[0].chatter_width || 450;
            defaults.chatter_collapsed = result[0].chatter_collapsed || false;
        }
    } catch (e) {
        console.warn("[FlexibleChatter] Prefs load failed", e);
    }
    return defaults;
}

async function saveChatterPrefs(vals) {
    try {
        await rpc("/web/dataset/call_kw/res.users/write", {
            model: "res.users",
            method: "write",
            args: [[user.userId], vals],
            kwargs: {},
        });
    } catch (e) { }
}

patch(Chatter.prototype, {
    setup() {
        super.setup(...arguments);
        this.flexState = useState({
            isResizing: false,
            width: 450,
            collapsed: false,
            prefsLoaded: false,
            showToggle: false,
        });

        onMounted(async () => {
            const prefs = await loadChatterPrefs();
            this.flexState.width = prefs.chatter_width || 450;
            this.flexState.collapsed = prefs.chatter_collapsed || false;
            this.flexState.prefsLoaded = true;
            this._applyFlexStyle();
        });

        useEffect(
            () => {
                if (this.flexState.prefsLoaded) this._applyFlexStyle();
            },
            () => [this.flexState.width, this.flexState.collapsed, this.flexState.prefsLoaded, this.state?.aside]
        );
    },

    _applyFlexStyle() {
        const el = this.rootRef?.el;
        if (!el) return;

        const container = el.closest(".o-mail-ChatterContainer, .o-mail-Form-chatter");
        const formSheetBg = container?.parentElement?.querySelector(".o_form_sheet_bg");

        if (this.flexState.collapsed) {
            el.classList.add("o_flex_collapsed");
            if (container) {
                container.style.width = "0px";
                container.style.minWidth = "0px";
                container.style.flex = "0 0 0px";
                container.classList.add("o_flex_container_collapsed");
            }
            if (formSheetBg) {
                formSheetBg.style.flex = "1 1 100%";
                formSheetBg.style.maxWidth = "100%";
                formSheetBg.style.minWidth = "0";
            }
        } else {
            el.classList.remove("o_flex_collapsed");
            if (container) container.classList.remove("o_flex_container_collapsed");

            if (this.state?.aside) {
                const w = this.flexState.width + "px";
                el.style.width = w;
                if (container) {
                    container.style.width = w;
                    container.style.flex = `0 0 ${w}`;
                    container.style.minWidth = "";
                }
                if (formSheetBg) {
                    formSheetBg.style.flex = "1 1 auto";
                    formSheetBg.style.maxWidth = "none";
                    formSheetBg.style.minWidth = "0";
                }
            } else {
                el.style.width = "";
                if (container) {
                    container.style.width = "";
                    container.style.flex = "";
                    container.style.minWidth = "";
                }
                if (formSheetBg) {
                    formSheetBg.style.flex = "";
                    formSheetBg.style.maxWidth = "";
                }
            }
        }
    },

    flexToggleChatter() {
        this.flexState.collapsed = !this.flexState.collapsed;
        saveChatterPrefs({
            chatter_collapsed: this.flexState.collapsed
        });
    },

    flexOnResizeStart(ev) {
        ev.preventDefault();
        this.flexState.isResizing = true;
        this._flexStartX = ev.clientX;
        this._flexStartWidth = this.flexState.width;
        this._flexOnMouseMove = (e) => {
            const dx = this._flexStartX - e.clientX;
            this.flexState.width = Math.max(300, Math.min(1000, this._flexStartWidth + dx));
        };
        this._flexOnMouseUp = () => {
            this.flexState.isResizing = false;
            document.removeEventListener("mousemove", this._flexOnMouseMove);
            document.removeEventListener("mouseup", this._flexOnMouseUp);
            document.body.style.cursor = "";
            saveChatterPrefs({
                chatter_width: this.flexState.width
            });
        };
        document.addEventListener("mousemove", this._flexOnMouseMove);
        document.addEventListener("mouseup", this._flexOnMouseUp);
        document.body.style.cursor = "col-resize";
    },

    flexOnMouseEnter() {
        this.flexState.showToggle = true;
    },
    flexOnMouseLeave() {
        this.flexState.showToggle = false;
    },
});

patch(FormRenderer.prototype, {
    setup() {
        super.setup(...arguments);
        this.flexChatterPrefs = useState({
            position: "side",
            loaded: false
        });
        onWillStart(async () => {
            const prefs = await loadChatterPrefs();
            this.flexChatterPrefs.position = prefs.chatter_position || "side";
            this.flexChatterPrefs.loaded = true;
        });
    },

    mailLayout(hasAttachmentContainer) {
        const result = super.mailLayout(hasAttachmentContainer);
        if (!this.flexChatterPrefs.loaded) return result;

        if (this.flexChatterPrefs.position === "bottom") {
            if (["SIDE_CHATTER", "EXTERNAL_COMBO_XXL"].includes(result)) {
                return result === "SIDE_CHATTER" ? "BOTTOM_CHATTER" : "EXTERNAL_COMBO";
            }
            if (result === "COMBO") {
                return "BOTTOM_CHATTER";
            }
        }
        return result;
    },
});
