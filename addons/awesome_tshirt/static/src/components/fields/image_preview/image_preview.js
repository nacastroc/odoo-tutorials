/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _lt } from "@web/core/l10n/translation";
import { CharField } from "@web/views/fields/char/char_field";
import { Component } from "@odoo/owl";

export class ImagePreviewField extends Component {}

ImagePreviewField.template = "awesome_tshirt.image_preview";
ImagePreviewField.supportedTypes = ["char"];
ImagePreviewField.displayName = _lt("Image Preview");
ImagePreviewField.components = { CharField };

registry.category("fields").add("image_preview", ImagePreviewField);