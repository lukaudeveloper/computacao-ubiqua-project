import { HttpClientModule } from "@angular/common/http";
import { NgModule } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { BrowserModule } from "@angular/platform-browser";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { MeasurementChartComponent } from "./components/measurement-chart/measurement-chart.component";
import { NavbarComponent } from "./components/navbar/navbar.component";
import { DashboardComponent } from "./pages/dashboard/dashboard.component";
import { HistoryComponent } from "./pages/history/history.component";
import { LoginComponent } from "./pages/login/login.component";
import { SensorsComponent } from "./pages/sensors/sensors.component";

import { AlertService } from "./services/alert.service";
import { AuthService } from "./services/auth.service";
import { MeasurementService } from "./services/measurement.service";
import { SensorService } from "./services/sensor.service";
import { WebsocketService } from "./services/websocket.service";

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent,
    SensorsComponent,
    HistoryComponent,
    NavbarComponent,
    MeasurementChartComponent,
  ],
  imports: [BrowserModule, AppRoutingModule, HttpClientModule, FormsModule],
  providers: [
    AuthService,
    SensorService,
    MeasurementService,
    AlertService,
    WebsocketService,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
