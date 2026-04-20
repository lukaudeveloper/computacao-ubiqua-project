import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { AuthService } from "./auth.service";

@Injectable({
  providedIn: "root",
})
export class AlertService {
  private apiUrl = "http://localhost:8000/api";

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) {}

  getAlerts(page: number = 1, limit: number = 20): Observable<any> {
    const url = `${this.apiUrl}/alerts?page=${page}&limit=${limit}`;
    return this.http.get(url, {
      headers: this.authService.getHeaders(),
    });
  }

  resolveAlert(id: number): Observable<any> {
    return this.http.put(
      `${this.apiUrl}/alerts/${id}/resolve`,
      {},
      { headers: this.authService.getHeaders() },
    );
  }
}
