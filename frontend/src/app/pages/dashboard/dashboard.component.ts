import { Component, OnDestroy, OnInit } from "@angular/core";
import { Subscription } from "rxjs";
import { AlertService } from "../../services/alert.service";
import { MeasurementService } from "../../services/measurement.service";
import { SensorService } from "../../services/sensor.service";
import { WebsocketService } from "../../services/websocket.service";

@Component({
  selector: "app-dashboard",
  templateUrl: "./dashboard.component.html",
  styleUrls: ["./dashboard.component.scss"],
})
export class DashboardComponent implements OnInit, OnDestroy {
  sensors: any[] = [];
  measurements: any[] = [];
  alerts: any[] = [];
  private wsSubscription: Subscription | null = null;

  constructor(
    private sensorService: SensorService,
    private measurementService: MeasurementService,
    private alertService: AlertService,
    private websocketService: WebsocketService,
  ) {}

  ngOnInit() {
    this.loadSensors();
    this.loadMeasurements();
    this.loadAlerts();
    this.connectWebSocket();
  }

  ngOnDestroy() {
    if (this.wsSubscription) {
      this.wsSubscription.unsubscribe();
    }
    this.websocketService.disconnect();
  }

  loadSensors() {
    this.sensorService.getSensors().subscribe((data) => (this.sensors = data));
  }

  loadMeasurements() {
    this.measurementService
      .getMeasurements()
      .subscribe((data) => (this.measurements = data));
  }

  loadAlerts() {
    this.alertService.getAlerts().subscribe((data) => (this.alerts = data));
  }

  connectWebSocket() {
    const wsUrl = `ws://${window.location.host}/ws`;
    this.wsSubscription = this.websocketService.connect(wsUrl).subscribe({
      next: (data) => {
        if (data.type === "measurement") {
          this.measurements.unshift(data.data);
        } else if (data.type === "alert") {
          this.alerts.unshift(data.data);
        }
      },
      error: (error) => console.error("WebSocket error:", error),
    });
  }

  resolveAlert(id: number) {
    this.alertService.resolveAlert(id).subscribe(() => {
      this.loadAlerts();
    });
  }
}
