/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _lt } from "@web/core/l10n/translation";
import { BooleanField } from "@web/views/fields/boolean/boolean_field";

export class LateOrderBooleanField extends BooleanField {}

LateOrderBooleanField.template = "awesome_tshirt.late_order"

registry.category("fields").add("late_order_boolean", LateOrderBooleanField);