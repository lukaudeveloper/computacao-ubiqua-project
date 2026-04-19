import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class SensorService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient, private authService: AuthService) { }

  getSensors(): Observable<any> {
    return this.http.get(`${this.apiUrl}/sensors`, { headers: this.authService.getHeaders() });
  }

  createSensor(sensor: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/sensors`, sensor, { headers: this.authService.getHeaders() });
  }

  updateSensor(id: number, sensor: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/sensors/${id}`, sensor, { headers: this.authService.getHeaders() });
  }

  deleteSensor(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/sensors/${id}`, { headers: this.authService.getHeaders() });
  }
}