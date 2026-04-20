import { Component, OnInit } from "@angular/core";
import { SensorService } from "../../services/sensor.service";

@Component({
  selector: "app-sensors",
  templateUrl: "./sensors.component.html",
  styleUrls: ["./sensors.component.scss"],
})
export class SensorsComponent implements OnInit {
  sensors: any[] = [];
  newSensor: any = {
    name: "",
    type: "",
    location: "",
    threshold_min: null,
    threshold_max: null,
  };
  editingSensor: any = null;
  simulationMessage = "";

  constructor(private sensorService: SensorService) {}

  ngOnInit() {
    this.loadSensors();
  }

  loadSensors() {
    this.sensorService.getSensors().subscribe((data) => (this.sensors = data));
  }

  addSensor() {
    this.sensorService.createSensor(this.newSensor).subscribe(() => {
      this.loadSensors();
      this.newSensor = {
        name: "",
        type: "",
        location: "",
        threshold_min: null,
        threshold_max: null,
      };
    });
  }

  editSensor(sensor: any) {
    this.editingSensor = { ...sensor };
  }

  updateSensor() {
    this.sensorService
      .updateSensor(this.editingSensor.id, this.editingSensor)
      .subscribe(() => {
        this.loadSensors();
        this.editingSensor = null;
      });
  }

  activateSensor(sensor: any) {
    this.sensorService.activateSensor(sensor.id, !sensor.is_active).subscribe(() => {
      this.loadSensors();
    });
  }

  simulateSensor(sensor: any) {
    this.sensorService.simulateSensor(sensor.id).subscribe((data) => {
      this.simulationMessage = `Sensor ${sensor.name} simulou ${data.value} em ${new Date(data.timestamp).toLocaleString()}`;
      this.loadSensors();
    });
  }

  deleteSensor(id: number) {
    this.sensorService.deleteSensor(id).subscribe(() => {
      this.loadSensors();
    });
  }
}
