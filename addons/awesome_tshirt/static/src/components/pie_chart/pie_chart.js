/** @odoo-module **/

import { Component, onWillStart, onMounted, useRef, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { getColor } from "@web/views/graph/colors";

export class PieChart extends Component {
    setup() {
        // Create a reference to the canvas element in the DOM, which will be used to draw the chart.
        this.canvasRef = useRef("canvas");

        // Extract the labels for the pie chart from the 'data' prop passed to the component.
        this.labels = Object.keys(this.props.data);
        // Extract the corresponding data values for the pie chart from the 'data' prop.
        this.data = Object.values(this.props.data);
        // Assign a color to each label using the getColor function, which maps an index to a color.
        this.color = this.labels.map((_, index) => {
            return getColor(index);
        });

        // Before the component is mounted, load the Chart.js library.
        onWillStart(() => {
            return loadJS(["/web/static/lib/Chart/Chart.js"]);
        });

        // Once the component is mounted, call the renderChart method to draw the chart.
        onMounted(() => {
            this.renderChart();
        });

        // Before the component is unmounted, call the disposeChart method to clean up.
        onWillUnmount(() => {
            this.disposeChart();
        });
    }

    /**
    * Initialize the chart using the Chart.js library.
    */
    renderChart() {
        this.disposeChart();
        // Create a new chart instance with the specified configuration.
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie", // Specify the type of chart to create.
            data: {
                labels: this.labels, // Use the labels defined in setup.
                datasets: [
                    {
                        label: this.props.label, // Use the label provided as a prop.
                        data: this.data, // Use the data values defined in setup.
                        backgroundColor: this.color, // Use the colors assigned to each label.
                    },
                ],
            },
        });
    }

    /**
    * Destroy the chart instance if it exists.
    */
    disposeChart() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

}

PieChart.template = "awesome_tshirt.pie_chart";


