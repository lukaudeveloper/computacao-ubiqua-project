import { Component, OnInit } from "@angular/core";
import { MeasurementService } from "../../services/measurement.service";
import { SensorService } from "../../services/sensor.service";

@Component({
  selector: "app-history",
  templateUrl: "./history.component.html",
  styleUrls: ["./history.component.scss"],
})
export class HistoryComponent implements OnInit {
  measurements: any[] = [];
  allMeasurements: any[] = []; // Para o gráfico
  sensors: any[] = [];
  chartKey = 0;
  currentPage = 1;
  limit = 20;
  pagination: any = {};

  constructor(
    private measurementService: MeasurementService,
    private sensorService: SensorService,
  ) {}

  ngOnInit() {
    this.loadSensors();
    this.loadAllMeasurements();
    this.loadMeasurements();
  }

  loadSensors() {
    this.sensorService.getSensors().subscribe((data) => (this.sensors = data));
  }

  loadMeasurements() {
    this.measurementService
      .getMeasurements(undefined, this.currentPage, this.limit)
      .subscribe((data) => {
        console.log("Measurements loaded:", data); // Log para verificar os dados
        this.measurements = data.measurements;
        this.pagination = data.pagination;
      });
  }

  loadAllMeasurements() {
    // Carrega uma quantidade maior de dados para o gráfico (últimas 200 medições)
    this.measurementService
      .getMeasurements(undefined, 1, 200)
      .subscribe((data) => {
        this.allMeasurements = data.measurements;
        this.chartKey++;
      });
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.loadMeasurements();
  }

  get visiblePages(): number[] {
    const pages = [];
    for (let i = 1; i <= this.pagination.pages; i++) {
      pages.push(i);
    }
    const start = Math.max(0, this.currentPage - 3);
    const end = this.currentPage + 2;
    return pages.slice(start, end);
  }

  exportToCSV() {
    const csv = this.measurements
      .map((m) => `${m.timestamp},${m.value},${m.sensor_name}`)
      .join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "measurements.csv";
    a.click();
    window.URL.revokeObjectURL(url);
  }
}
