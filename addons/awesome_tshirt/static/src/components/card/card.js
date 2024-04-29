/** @odoo-module **/

import { Component, useSubEnv } from "@odoo/owl";

export class Card extends Component { }

Card.template = "awesome_tshirt.card";
Card.props = {
    slots: {
        type: Object,
        shape: {
            default: Object,
            title: { type: Object, optional: true },
        },
    },
    className: {
        type: String,
        optional: true,
    },
};
