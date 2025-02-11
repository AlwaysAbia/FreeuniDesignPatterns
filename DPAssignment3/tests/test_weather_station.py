from unittest.mock import Mock

import pytest

from DPAssignment3.weather_observer import WindSpeedAlert
from DPAssignment3.weather_station import WeatherStation


@pytest.fixture
def weather_station() -> WeatherStation:
    return WeatherStation()

@pytest.fixture
def mock_observer() -> Mock:
    return Mock()

def test_add_observer(
    weather_station: WeatherStation,
    mock_observer: Mock
) -> None:
    weather_station.add_observer(mock_observer)
    assert mock_observer in weather_station._observers

def test_remove_observer(
    weather_station: WeatherStation,
    mock_observer: Mock
) -> None:
    weather_station.add_observer(mock_observer)
    weather_station.remove_observer(mock_observer)
    assert mock_observer not in weather_station._observers

def test_notify_observers(
    weather_station: WeatherStation,
    mock_observer: Mock
) -> None:
    weather_station.add_observer(mock_observer)
    weather_station.update_weather(25.0, 60.0, 10.0)
    mock_observer.update.assert_called_once_with(25.0, 60.0, 10.0)

def test_wind_speed_alert_initialization(
    weather_station: WeatherStation
) -> None:
    weather_station.wind_speed = 15.0
    alert = WindSpeedAlert()
    weather_station.add_observer(alert)
    assert alert.previous_wind_speed == 15.0