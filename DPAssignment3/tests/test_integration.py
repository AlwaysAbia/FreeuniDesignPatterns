from unittest.mock import Mock, patch

from DPAssignment3.weather_observer import (
    TemperatureAlert,
    WeatherDisplay,
    WindSpeedAlert,
)
from DPAssignment3.weather_station import WeatherStation


def test_full_system_integration() -> None:
    station = WeatherStation()
    display = WeatherDisplay()
    temp_alert = TemperatureAlert(30.0)
    wind_alert = WindSpeedAlert()

    station.add_observer(display)
    station.add_observer(temp_alert)
    station.add_observer(wind_alert)

    with patch('builtins.print') as mock_print:
        # First update
        station.update_weather(28.0, 70.0, 12.0)
        assert mock_print.call_count == 2
        mock_print.reset_mock()

        # Second update with alerts
        station.update_weather(32.0, 75.0, 15.0)
        assert mock_print.call_count == 3
        calls = [call.args[0] for call in mock_print.mock_calls]
        assert any("TemperatureAlert" in call for call in calls)
        assert any("WindSpeedAlert: **Alert!" in call for call in calls)


def test_observer_removal() -> None:
    station = WeatherStation()
    mock_obs = Mock()
    station.add_observer(mock_obs)
    station.remove_observer(mock_obs)
    station.update_weather(25.0, 50.0, 10.0)
    mock_obs.update.assert_not_called()