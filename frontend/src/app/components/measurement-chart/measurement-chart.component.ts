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
      // Group measurements by sensor
      const sensorGroups: { [key: string]: any[] } = {};
      this.measurements.forEach((m) => {
        if (!sensorGroups[m.sensor_name]) {
          sensorGroups[m.sensor_name] = [];
        }
        sensorGroups[m.sensor_name].push(m);
      });

      // Get all unique timestamps
      const allTimestamps = Array.from(
        new Set(this.measurements.map((m) => m.timestamp))
      ).sort();

      // Create datasets
      const datasets = Object.keys(sensorGroups).map((sensorName, index) => {
        const sensorMeasurements = sensorGroups[sensorName];
        const data = allTimestamps.map((timestamp) => {
          const measurement = sensorMeasurements.find((m) => m.timestamp === timestamp);
          return measurement ? measurement.value : null;
        });
        const colors = [
          "rgb(75, 192, 192)",
          "rgb(255, 99, 132)",
          "rgb(54, 162, 235)",
          "rgb(255, 205, 86)",
          "rgb(153, 102, 255)",
        ];
        return {
          label: sensorName,
          data: data,
          borderColor: colors[index % colors.length],
          tension: 0.1,
          spanGaps: true,
        };
      });

      this.chart = new Chart(ctx, {
        type: "line",
        data: {
          labels: allTimestamps,
          datasets: datasets,
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: true,
            },
          },
        },
      });
    }
  }
}
