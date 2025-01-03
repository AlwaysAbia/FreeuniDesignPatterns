import random

from constants import SIMULATION_COUNT, WORLD_MAX_POSITION, ClawSize, TeethSharpness, \
    INITIAL_HEALTH_RANGE_PREDATOR, INITIAL_STAMINA_RANGE_PREDATOR, BASE_ATTACK_RANGE_PREDATOR, \
    INITIAL_HEALTH_RANGE_PRAY, INITIAL_STAMINA_RANGE_PRAY, BASE_ATTACK_RANGE_PRAY
from creature import (
    Creature,
    CreatureBuilder,
    FlyHandler,
    HopHandler,
    RunHandler,
    WalkHandler,
)


class Simulation:
    def __init__(self) -> None:
        # Set up movement chain
        self.movement_chain = FlyHandler(RunHandler(WalkHandler(HopHandler())))
        # Maximum iterations to prevent infinite loops
        self.MAX_ITERATIONS = 1000

    def simulate_chase(self, predator: Creature, prey: Creature) -> bool:
        """
        Simulates chase phase. Returns True if predator catches prey, False otherwise.
        Only ends when predator runs out of stamina or catches prey.
        """
        iterations = 0

        while iterations < self.MAX_ITERATIONS:
            iterations += 1

            # Get movement capabilities
            pred_speed, pred_stamina_cost = predator.move(self.movement_chain)
            prey_speed, prey_stamina_cost = prey.move(self.movement_chain)

            # If neither can move and predator hasn't caught prey, chase ends
            if pred_speed == 0 and prey_speed == 0:
                print("Pray ran into infinity")
                return False

            # Update stamina
            predator.stamina -= pred_stamina_cost
            prey.stamina -= prey_stamina_cost

            # Update positions
            predator.position += pred_speed
            prey.position += prey_speed

            # Check win/lose conditions
            if predator.stamina <= 0:
                print("Pray ran into infinity")
                return False

            if predator.position >= prey.position:
                return True

        # If we reach max iterations, prey escapes
        print("Pray ran into infinity")
        return False

    def simulate_fight(self, predator: Creature, prey: Creature) -> bool:
        """
        Simulates fight phase. Returns True if predator wins, False if prey wins.
        Only ends when either creature runs out of health.
        """
        iterations = 0

        while iterations < self.MAX_ITERATIONS:
            iterations += 1

            # Both creatures attack simultaneously
            predator.health -= prey.get_attack_power()
            prey.health -= predator.get_attack_power()

            if predator.health <= 0:
                print("Pray ran into infinity")
                return False

            if prey.health <= 0:
                print("Some R-rated things have happened")
                return True

        # If we reach max iterations, consider it a prey escape
        print("Pray ran into infinity")
        return False

    def create_random_creature(self, type: int, position: int = 0) -> Creature:
        builder = CreatureBuilder()

        # Randomly assign characteristics
        if (type == 0):
            builder.add_legs(random.randint(0, 4))
            builder.add_wings(random.randint(0, 2))
            builder.add_claws(random.choice(list(ClawSize)))
            builder.add_teeth(random.choice(list(TeethSharpness)))

            return (
                builder.set_health(random.randint(INITIAL_HEALTH_RANGE_PREDATOR[0], INITIAL_HEALTH_RANGE_PREDATOR[1]))
                .set_stamina(random.randint(INITIAL_STAMINA_RANGE_PREDATOR[0], INITIAL_STAMINA_RANGE_PREDATOR[1]))
                .set_base_attack(random.randint(BASE_ATTACK_RANGE_PREDATOR[0], BASE_ATTACK_RANGE_PREDATOR[1]))
                .set_position(position)
                .build()
            )
        else:
            builder.add_legs(random.randint(0, 3))
            builder.add_wings(random.randint(0, 1))
            builder.add_claws(random.choice(list(ClawSize)))
            builder.add_teeth(random.choice(list(TeethSharpness)))

            return (
                builder.set_health(random.randint(INITIAL_HEALTH_RANGE_PRAY[0], INITIAL_HEALTH_RANGE_PRAY[1]))
                .set_stamina(random.randint(INITIAL_STAMINA_RANGE_PRAY[0], INITIAL_STAMINA_RANGE_PRAY[1]))
                .set_base_attack(random.randint(BASE_ATTACK_RANGE_PRAY[0], BASE_ATTACK_RANGE_PRAY[1]))
                .set_position(position)
                .build()
            )

    def run_simulation(self) -> None:
        for i in range(SIMULATION_COUNT):
            print(f"\nSimulation {i + 1}")

            # Evolution phase
            predator = self.create_random_creature(0,0)
            prey = self.create_random_creature(1, random.randint(0, WORLD_MAX_POSITION))

            print(
                f"Predator evolved at position 0 with {predator.legs} legs, "
                f"{predator.wings} wings, attack power {predator.get_attack_power()}"
            )
            print(
                f"Prey evolved at position {prey.position} with {prey.legs} legs, "
                f"{prey.wings} wings, attack power {prey.get_attack_power()}"
            )

            # Chase phase - if successful, enter fight phase
            if self.simulate_chase(predator, prey):
                self.simulate_fight(predator, prey)


def main() -> None:
    simulation = Simulation()
    simulation.run_simulation()


if __name__ == "__main__":
    main()