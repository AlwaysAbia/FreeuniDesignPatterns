import random

from DPAssignment3.weather_observer import (
    HumidityAlert,
    TemperatureAlert,
    WeatherDisplay,
    WindSpeedAlert,
)
from DPAssignment3.weather_station import WeatherStation


def run_simulation() -> None:
    weather_station = WeatherStation()
    weather_display = WeatherDisplay()
    weather_station.add_observer(weather_display)

    # Initial fixed updates (weeks 1-3)
    updates = [
        (28.0, 70.0, 12.0),
        (30.0, 72.0, 15.0),
        (32.0, 74.0, 18.0),
    ]
    # Add 17 random updates (total 20)
    for _ in range(17):
        temp = random.uniform(25.0, 45.0)
        humidity = random.uniform(60.0, 95.0)
        wind_speed = random.uniform(10.0, 35.0)
        updates.append((temp, humidity, wind_speed))

    week = 1
    active_alerts = []
    available_alert_types = [TemperatureAlert, WindSpeedAlert, HumidityAlert]

    for temp, hum, ws in updates:
        print(f"\n---\nWeek {week}:")

        # Randomly add a new alert (30% chance after week 3)
        if week > 3 and random.random() < 0.3 and available_alert_types:
            AlertClass = random.choice(available_alert_types)
            new_alert = AlertClass()
            weather_station.add_observer(new_alert)
            active_alerts.append(new_alert)
            print(f"Added: {AlertClass.__name__}")

            # Remove from available if each type should be added once
            # available_alert_types.remove(AlertClass)

        # Update weather data
        weather_station.update_weather(temp, hum, ws)

        # Randomly remove an alert (10% chance after week 5)
        if week > 5 and active_alerts and random.random() < 0.1:
            alert_to_remove = random.choice(active_alerts)
            weather_station.remove_observer(alert_to_remove)
            active_alerts.remove(alert_to_remove)
            print(f"Removed: {alert_to_remove.__class__.__name__}")

        week += 1


if __name__ == "__main__":
    run_simulation()