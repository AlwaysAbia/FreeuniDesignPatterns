from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple

from constants import ClawSize, TeethSharpness

# Movement Strategy Pattern
class MovementStrategy(ABC):
    @abstractmethod
    def move(self, stamina: int) -> Tuple[int, int]:  # Returns (speed, stamina_cost)
        pass

class CrawlStrategy(MovementStrategy):
    def move(self, stamina: int) -> Tuple[int, int]:
        return (1, 1)

class HopStrategy(MovementStrategy):
    def move(self, stamina: int) -> Tuple[int, int]:
        return (3, 2) if stamina >= 20 else (0, 0)

class WalkStrategy(MovementStrategy):
    def move(self, stamina: int) -> Tuple[int, int]:
        return (4, 2) if stamina >= 40 else (0, 0)

class RunStrategy(MovementStrategy):
    def move(self, stamina: int) -> Tuple[int, int]:
        return (6, 4) if stamina >= 60 else (0, 0)

class FlyStrategy(MovementStrategy):
    def move(self, stamina: int) -> Tuple[int, int]:
        return (8, 4) if stamina >= 80 else (0, 0)

# Movement Chain of Responsibility
class MovementHandler(ABC):
    def __init__(self, successor: Optional["MovementHandler"] = None) -> None:
        self.successor = successor

    @abstractmethod
    def handle(self, creature: "Creature") -> MovementStrategy:
        pass

class FlyHandler(MovementHandler):
    def handle(self, creature: "Creature") -> MovementStrategy:
        if creature.wings >= 2:
            return FlyStrategy()
        if self.successor:
            return self.successor.handle(creature)
        return CrawlStrategy()

class RunHandler(MovementHandler):
    def handle(self, creature: "Creature") -> MovementStrategy:
        if creature.legs >= 2:
            return RunStrategy()
        if self.successor:
            return self.successor.handle(creature)
        return CrawlStrategy()

class WalkHandler(MovementHandler):
    def handle(self, creature: "Creature") -> MovementStrategy:
        if creature.legs >= 2:
            return WalkStrategy()
        if self.successor:
            return self.successor.handle(creature)
        return CrawlStrategy()

class HopHandler(MovementHandler):
    def handle(self, creature: "Creature") -> MovementStrategy:
        if creature.legs >= 1:
            return HopStrategy()
        if self.successor:
            return self.successor.handle(creature)
        return CrawlStrategy()

@dataclass
class Creature:
    legs: int = 0
    wings: int = 0
    claw_multiplier: int = 1
    teeth_bonus: int = 0
    health: int = 100
    stamina: int = 100
    base_attack: int = 10
    position: int = 0

    def get_attack_power(self) -> int:
        return (self.base_attack * self.claw_multiplier) + self.teeth_bonus

    def move(self, movement_chain: MovementHandler) -> Tuple[int, int]:
        strategy = movement_chain.handle(self)
        return strategy.move(self.stamina)

# Creature Builder Pattern
class CreatureBuilder:
    def __init__(self) -> None:
        self._creature: Creature
        self.reset()

    def reset(self) -> "CreatureBuilder":
        self._creature = Creature()
        return self

    def add_legs(self, count: int) -> "CreatureBuilder":
        self._creature.legs = count
        return self

    def add_wings(self, count: int) -> "CreatureBuilder":
        self._creature.wings = count
        return self

    def add_claws(self, size: ClawSize) -> "CreatureBuilder":
        self._creature.claw_multiplier = size.value
        return self

    def add_teeth(self, sharpness: TeethSharpness) -> "CreatureBuilder":
        self._creature.teeth_bonus = sharpness.value
        return self

    def set_health(self, health: int) -> "CreatureBuilder":
        self._creature.health = health
        return self

    def set_stamina(self, stamina: int) -> "CreatureBuilder":
        self._creature.stamina = stamina
        return self

    def set_base_attack(self, attack: int) -> "CreatureBuilder":
        self._creature.base_attack = attack
        return self

    def set_position(self, position: int) -> "CreatureBuilder":
        self._creature.position = position
        return self

    def build(self) -> Creature:
        creature = self._creature
        self.reset()
        return creature