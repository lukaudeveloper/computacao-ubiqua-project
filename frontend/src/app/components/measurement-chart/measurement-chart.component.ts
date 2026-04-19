import { Component, Input, OnChanges } from "@angular/core";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

@Component({
  selector: "app-measurement-chart",
  templateUrl: "./measurement-chart.component.html",
  styleUrls: ["./measurement-chart.component.scss"],
})
export class MeasurementChartComponent implements OnChanges {
  @Input() measurements: any[] = [];
  chart: Chart | null = null;

  ngOnChanges() {
    this.updateChart();
  }

  updateChart() {
    if (this.chart) {
      this.chart.destroy();
    }
    const ctx = document.getElementById(
      "measurementChart",
    ) as HTMLCanvasElement;
    if (ctx) {
      this.chart = new Chart(ctx, {
        type: "line",
        data: {
          labels: this.measurements.map((m) => m.timestamp),
          datasets: [
            {
              label: "Measurements",
              data: this.measurements.map((m) => m.value),
              borderColor: "rgb(75, 192, 192)",
              tension: 0.1,
            },
          ],
        },
      });
    }
  }
}
