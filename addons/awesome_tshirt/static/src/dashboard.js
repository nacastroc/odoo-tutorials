/** @odoo-module **/

import { Component, useSubEnv, onWillStart } from "@odoo/owl";
import { getDefaultConfig } from "@web/views/view";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { Domain } from "@web/core/domain";
import { Card } from "./components/card/card";
import { PieChart } from "./components/pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    setup() {
        // Hook to import the 'action' service.
        this.action = useService("action");

        // Hook to import the 'statisticsService' service (for server requests)
        this.statisticsService = useService("statisticsService");

        // Prop to setup the Layout component's display
        this.display = {
            controlPanel: { "top-right": false, "bottom-right": false },
        };

        this.statKeys = {
            nb_new_orders: this.env._t("Number of new orders this month"),
            total_amount: this.env._t("Total amount of new orders this month"),
            average_quantity: this.env._t("Average amount of t-shirt by order this month"),
            nb_cancelled_orders: this.env._t("Number of cancelled orders this month"),
            average_time: this.env._t("Average time for an order to go from 'new' to 'sent' or 'cancelled'"),
        };

        // Hook to set up a sub-environment. It merges the default configuration with the environment configuration.
        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            },
        });

        onWillStart(async () => {
            this.statistics = await this.statisticsService.loadStatistics();
        });
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openOrdersView(title, domain) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: title,
            res_model: "awesome_tshirt.order",
            domain: new Domain(domain).toList(), // Parse odoo domain to JS OWL component
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    openNewOrdersView() {
        const title = this.env._t("New Orders");
        const domain = "[('create_date','>=', (context_today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'))]";
        this.openOrdersView(title, domain)
    }

    openCancelledOrdersView() {
        const title = this.env._t("Cancelled Orders");
        const domain = "[('create_date','>=', (context_today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')), ('state', '=', 'cancelled')]";
        this.openOrdersView(title, domain)
    }
}

AwesomeDashboard.components = { Layout, Card, PieChart };
AwesomeDashboard.template = "awesome_tshirt.clientaction";

registry.category("actions").add("awesome_tshirt.dashboard", AwesomeDashboard);
