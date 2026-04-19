import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { AuthService } from "./auth.service";

@Injectable({
  providedIn: "root",
})
export class MeasurementService {
  private apiUrl = "/api";

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) {}

  getMeasurements(sensorId?: number): Observable<any> {
    const url = sensorId
      ? `${this.apiUrl}/measurements?sensor_id=${sensorId}`
      : `${this.apiUrl}/measurements`;
    return this.http.get(url, { headers: this.authService.getHeaders() });
  }

  createMeasurement(measurement: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/measurements`, measurement, {
      headers: this.authService.getHeaders(),
    });
  }
}
