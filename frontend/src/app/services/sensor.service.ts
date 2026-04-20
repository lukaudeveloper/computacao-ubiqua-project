import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { AuthService } from "./auth.service";

@Injectable({
  providedIn: "root",
})
export class SensorService {
  private apiUrl = "http://localhost:8000/api";

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) {}

  getSensors(): Observable<any> {
    return this.http.get(`${this.apiUrl}/sensors`, {
      headers: this.authService.getHeaders(),
    });
  }

  createSensor(sensor: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/sensors`, sensor, {
      headers: this.authService.getHeaders(),
    });
  }

  updateSensor(id: number, sensor: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/sensors/${id}`, sensor, {
      headers: this.authService.getHeaders(),
    });
  }

  activateSensor(id: number, isActive: boolean): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/sensors/${id}/activate`,
      { is_active: isActive },
      { headers: this.authService.getHeaders() },
    );
  }

  simulateSensor(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/sensors/${id}/simulate`, {}, {
      headers: this.authService.getHeaders(),
    });
  }

  deleteSensor(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/sensors/${id}`, {
      headers: this.authService.getHeaders(),
    });
  }
}
