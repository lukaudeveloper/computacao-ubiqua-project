import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { AuthService } from "./auth.service";

@Injectable({
  providedIn: "root",
})
export class MeasurementService {
  private apiUrl = "http://localhost:8000/api";

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) {}

  getMeasurements(
    sensorId?: number,
    page: number = 1,
    limit: number = 50,
  ): Observable<any> {
    let url = `${this.apiUrl}/measurements?page=${page}&limit=${limit}`;
    if (sensorId) {
      url += `&sensor_id=${sensorId}`;
    }
    return this.http.get(url, { headers: this.authService.getHeaders() });
  }

  createMeasurement(measurement: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/measurements`, measurement, {
      headers: this.authService.getHeaders(),
    });
  }
}
