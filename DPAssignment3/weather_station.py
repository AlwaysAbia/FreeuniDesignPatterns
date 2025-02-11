from abc import ABC, abstractmethod
from typing import List

from .weather_observer import WeatherObserver


class IWeatherStation(ABC):
    @abstractmethod
    def add_observer(self, observer: WeatherObserver) -> None:
        pass

    @abstractmethod
    def remove_observer(self, observer: WeatherObserver) -> None:
        pass

    @abstractmethod
    def notify_observers(self) -> None:
        pass


class WeatherStation(IWeatherStation):
    def __init__(self) -> None:
        self._observers: List[WeatherObserver] = []
        self.temperature: float = 0.0
        self.humidity: float = 0.0
        self.wind_speed: float = 0.0

    def add_observer(self, observer: WeatherObserver) -> None:
        if observer not in self._observers:
            # Initialize WindSpeedAlert's previous wind speed to current value
            if hasattr(observer, "previous_wind_speed"):
                observer.previous_wind_speed = self.wind_speed
            self._observers.append(observer)

    def remove_observer(self, observer: WeatherObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update(self.temperature, self.humidity, self.wind_speed)

    def update_weather(
            self, temperature: float, humidity: float, wind_speed: float) -> None:
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.notify_observers()