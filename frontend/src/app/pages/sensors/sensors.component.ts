import { Component, OnInit } from '@angular/core';
import { SensorService } from '../../services/sensor.service';

@Component({
  selector: 'app-sensors',
  templateUrl: './sensors.component.html',
  styleUrls: ['./sensors.component.scss']
})
export class SensorsComponent implements OnInit {
  sensors: any[] = [];
  newSensor = { name: '', type: '', location: '' };
  editingSensor: any = null;

  constructor(private sensorService: SensorService) { }

  ngOnInit() {
    this.loadSensors();
  }

  loadSensors() {
    this.sensorService.getSensors().subscribe(data => this.sensors = data);
  }

  addSensor() {
    this.sensorService.createSensor(this.newSensor).subscribe(() => {
      this.loadSensors();
      this.newSensor = { name: '', type: '', location: '' };
    });
  }

  editSensor(sensor: any) {
    this.editingSensor = { ...sensor };
  }

  updateSensor() {
    this.sensorService.updateSensor(this.editingSensor.id, this.editingSensor).subscribe(() => {
      this.loadSensors();
      this.editingSensor = null;
    });
  }

  deleteSensor(id: number) {
    this.sensorService.deleteSensor(id).subscribe(() => {
      this.loadSensors();
    });
  }
}