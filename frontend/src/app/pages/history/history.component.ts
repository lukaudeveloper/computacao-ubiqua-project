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
  selectedSensorId: number | null = null;
  sensors: any[] = [];

  constructor(
    private measurementService: MeasurementService,
    private sensorService: SensorService,
  ) {}

  ngOnInit() {
    this.loadSensors();
    this.loadMeasurements();
  }

  loadSensors() {
    this.sensorService.getSensors().subscribe((data) => (this.sensors = data));
  }

  loadMeasurements() {
    this.measurementService
      .getMeasurements(this.selectedSensorId || undefined)
      .subscribe((data) => (this.measurements = data));
  }

  onSensorChange() {
    this.loadMeasurements();
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
