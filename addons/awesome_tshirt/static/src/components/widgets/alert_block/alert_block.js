/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

export class AlertBlock extends Component {
    setup() {
        console.log("Record: ", this.props.record)
    }
}

AlertBlock.template = "awesome_tshirt.alert_block"

registry.category("view_widgets").add("alert_block", AlertBlock);