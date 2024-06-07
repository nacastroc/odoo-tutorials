/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

export class AlertBlock extends Component {}

AlertBlock.template = "awesome_tshirt.alert_block"

registry.category("view_widgets").add("alert_block", AlertBlock);