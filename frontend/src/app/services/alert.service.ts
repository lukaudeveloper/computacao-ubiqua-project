import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AlertService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient, private authService: AuthService) { }

  getAlerts(): Observable<any> {
    return this.http.get(`${this.apiUrl}/alerts`, { headers: this.authService.getHeaders() });
  }

  resolveAlert(id: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/alerts/${id}/resolve`, {}, { headers: this.authService.getHeaders() });
  }
}