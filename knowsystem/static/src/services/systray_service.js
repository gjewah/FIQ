/** @odoo-module **/

import { SystrayQuickLink } from "@knowsystem/components/systray_quick_link/systray_quick_link";
import { registry } from "@web/core/registry";
const systrayRegistry = registry.category("systray");

export const kmsSystrayService = {
    start() {
        systrayRegistry.add("knowsystem.QuickLink", { Component: SystrayQuickLink }, { sequence: 40 });
    },
};

registry.category("services").add("kmsSystrayService", kmsSystrayService);
