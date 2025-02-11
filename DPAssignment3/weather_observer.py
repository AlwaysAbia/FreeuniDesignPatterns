from abc import ABC, abstractmethod
from random import uniform
from typing import Optional


class WeatherObserver(ABC):
    @abstractmethod
    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        pass


class WeatherDisplay(WeatherObserver):
    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        print(
            f"WeatherDisplay: Showing Temperature = {temperature:.1f}°C, "
            f"Humidity = {humidity:.1f}%, Wind Speed = {wind_speed:.1f} km/h"
        )


class TemperatureAlert(WeatherObserver):
    def __init__(self, threshold: Optional[float] = None) -> None:
        self.threshold = threshold if threshold is not None else uniform(30.0, 35.0)

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if temperature >= self.threshold:
            print(
                f"TemperatureAlert: **Alert! Temperature exceeded {self.threshold:.1f}°C: "  # noqa: E501
                f"{temperature:.1f}°C**"
            )


class WindSpeedAlert(WeatherObserver):
    def __init__(self) -> None:
        self.previous_wind_speed: Optional[float] = None

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if (self.previous_wind_speed is not None
                and wind_speed > self.previous_wind_speed):
            print(
                f"WindSpeedAlert: **Alert! Wind speed is increasing: "
                f"{self.previous_wind_speed:.1f} km/h → {wind_speed:.1f} km/h**"
            )
        else:
            print("WindSpeedAlert: No alert (No upward trend detected)")
        self.previous_wind_speed = wind_speed


class HumidityAlert(WeatherObserver):
    def __init__(self, threshold: Optional[float] = None) -> None:
        self.threshold = threshold if threshold is not None else uniform(80.0, 90.0)

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if humidity >= self.threshold:
            print(
                f"HumidityAlert: **Alert! Humidity exceeded {self.threshold:.1f}%: "
                f"{humidity:.1f}%**"
            )