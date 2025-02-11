from unittest.mock import patch

from DPAssignment3.weather_observer import (
    HumidityAlert,
    TemperatureAlert,
    WeatherDisplay,
    WindSpeedAlert,
)


def test_weather_display_output() -> None:
    display = WeatherDisplay()
    with patch('builtins.print') as mock_print:
        display.update(28.5, 72.3, 15.8)
        mock_print.assert_called_with(
            "WeatherDisplay: Showing Temperature = 28.5°C, "
            "Humidity = 72.3%, Wind Speed = 15.8 km/h"
        )

def test_temperature_alert_triggered() -> None:
    alert = TemperatureAlert(threshold=30.0)
    with patch('builtins.print') as mock_print:
        alert.update(35.0, 50.0, 10.0)
        mock_print.assert_called_with(
            "TemperatureAlert: **Alert! Temperature exceeded 30.0°C: 35.0°C**"
        )

def test_temperature_alert_not_triggered() -> None:
    alert = TemperatureAlert(threshold=30.0)
    with patch('builtins.print') as mock_print:
        alert.update(25.0, 50.0, 10.0)
        mock_print.assert_not_called()

def test_wind_speed_alert_increasing() -> None:
    alert = WindSpeedAlert()
    alert.previous_wind_speed = 10.0
    with patch('builtins.print') as mock_print:
        alert.update(25.0, 50.0, 15.0)
        mock_print.assert_called_with(
            "WindSpeedAlert: **Alert! Wind speed is increasing: 10.0 km/h → 15.0 km/h**"
        )

def test_wind_speed_alert_not_increasing() -> None:
    alert = WindSpeedAlert()
    alert.previous_wind_speed = 15.0
    with patch('builtins.print') as mock_print:
        alert.update(25.0, 50.0, 10.0)
        mock_print.assert_called_with(
            "WindSpeedAlert: No alert (No upward trend detected)")



def test_humidity_alert_triggered() -> None:
    alert = HumidityAlert(threshold=80.0)
    with patch('builtins.print') as mock_print:
        alert.update(25.0, 85.0, 10.0)
        mock_print.assert_called_with(
            "HumidityAlert: **Alert! Humidity exceeded 80.0%: 85.0%**"
        )

def test_humidity_alert_not_triggered() -> None:
    alert = HumidityAlert(threshold=80.0)
    with patch('builtins.print') as mock_print:
        alert.update(25.0, 75.0, 10.0)
        mock_print.assert_not_called()