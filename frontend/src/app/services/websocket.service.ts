import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  private socket: WebSocket | null = null;
  private subject = new Subject<any>();

  constructor() { }

  connect(url: string): Observable<any> {
    this.socket = new WebSocket(url);
    this.socket.onmessage = (event) => {
      this.subject.next(JSON.parse(event.data));
    };
    this.socket.onerror = (error) => {
      this.subject.error(error);
    };
    this.socket.onclose = () => {
      this.subject.complete();
    };
    return this.subject.asObservable();
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
    }
  }

  send(data: any) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(data));
    }
  }
}