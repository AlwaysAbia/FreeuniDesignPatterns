from enum import Enum
from typing import Dict, Tuple, TypedDict

class MovementStats(TypedDict):
    stamina_required: int
    stamina_cost: int
    speed: int

MOVEMENT_STATS: Dict[str, MovementStats] = {
    "crawl": {"stamina_required": 0, "stamina_cost": 1, "speed": 1},
    "hop": {"stamina_required": 20, "stamina_cost": 2, "speed": 3},
    "walk": {"stamina_required": 40, "stamina_cost": 2, "speed": 4},
    "run": {"stamina_required": 60, "stamina_cost": 4, "speed": 6},
    "fly": {"stamina_required": 80, "stamina_cost": 4, "speed": 8},
}

WORLD_MAX_POSITION: int = 1000
SIMULATION_COUNT: int = 100

class ClawSize(Enum):
    SMALL = 2
    MEDIUM = 3
    LARGE = 4

class TeethSharpness(Enum):
    DULL = 3
    SHARP = 6
    VERY_SHARP = 9

# Initial stat ranges
INITIAL_HEALTH_RANGE_PREDATOR: Tuple[int, int] = (50, 150)
INITIAL_STAMINA_RANGE_PREDATOR: Tuple[int, int] = (500, 800)
BASE_ATTACK_RANGE_PREDATOR: Tuple[int, int] = (30, 45)

INITIAL_HEALTH_RANGE_PRAY: Tuple[int, int] = (30, 100)
INITIAL_STAMINA_RANGE_PRAY: Tuple[int, int] = (300, 500)
BASE_ATTACK_RANGE_PRAY: Tuple[int, int] = (20, 25)