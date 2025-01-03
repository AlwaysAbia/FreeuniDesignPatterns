import pytest

from constants import INITIAL_HEALTH_RANGE_PREDATOR, INITIAL_STAMINA_RANGE_PREDATOR, BASE_ATTACK_RANGE_PREDATOR, \
    INITIAL_HEALTH_RANGE_PRAY, INITIAL_STAMINA_RANGE_PRAY, BASE_ATTACK_RANGE_PRAY
from creature import ClawSize, Creature, TeethSharpness
from simulate import Simulation


class TestSimulation:
    @pytest.fixture
    def simulation(self) -> Simulation:
        return Simulation()

    def test_create_random_creature(self, simulation: Simulation) -> None:
        creature1 = simulation.create_random_creature(0, 10)
        creature2 = simulation.create_random_creature(1, 15)
        assert isinstance(creature1, Creature)
        assert isinstance(creature2, Creature)
        assert creature1.position == 10
        assert 0 <= creature1.legs <= 4
        assert 0 <= creature1.wings <= 2
        assert creature1.health >= INITIAL_HEALTH_RANGE_PREDATOR[0]
        assert creature1.health <= INITIAL_HEALTH_RANGE_PREDATOR[1]
        assert creature1.stamina >= INITIAL_STAMINA_RANGE_PREDATOR[0]
        assert creature1.stamina <= INITIAL_STAMINA_RANGE_PREDATOR[1]
        assert creature1.base_attack >= BASE_ATTACK_RANGE_PREDATOR[0]
        assert creature1.base_attack <= BASE_ATTACK_RANGE_PREDATOR[1]

        assert creature2.position == 15
        assert 0 <= creature2.legs <= 4
        assert 0 <= creature2.wings <= 2
        assert creature2.health >= INITIAL_HEALTH_RANGE_PRAY[0]
        assert creature2.health <= INITIAL_HEALTH_RANGE_PRAY[1]
        assert creature2.stamina >= INITIAL_STAMINA_RANGE_PRAY[0]
        assert creature2.stamina <= INITIAL_STAMINA_RANGE_PRAY[1]
        assert creature2.base_attack >= BASE_ATTACK_RANGE_PRAY[0]
        assert creature2.base_attack <= BASE_ATTACK_RANGE_PRAY[1]

    def test_simulate_chase_predator_catches(self, simulation: Simulation) -> None:
        # Fast predator, slow prey
        predator = Creature(legs=4, stamina=100, position=0)
        prey = Creature(legs=1, stamina=100, position=5)

        assert simulation.simulate_chase(predator, prey) is True

    def test_simulate_chase_prey_escapes(self, simulation: Simulation) -> None:
        # Low stamina predator
        predator = Creature(legs=2, stamina=20, position=0)
        prey = Creature(wings=2, stamina=100, position=50)

        assert simulation.simulate_chase(predator, prey) is False

    def test_simulate_fight_predator_wins(self, simulation: Simulation) -> None:
        predator = Creature(
            base_attack=20,
            claw_multiplier=ClawSize.LARGE.value,
            teeth_bonus=TeethSharpness.VERY_SHARP.value,
            health=100,
        )
        prey = Creature(base_attack=5, health=50)

        assert simulation.simulate_fight(predator, prey) is True

    def test_simulate_fight_prey_wins(self, simulation: Simulation) -> None:
        predator = Creature(base_attack=5, health=50)
        prey = Creature(
            base_attack=20,
            claw_multiplier=ClawSize.LARGE.value,
            teeth_bonus=TeethSharpness.VERY_SHARP.value,
            health=100,
        )

        assert simulation.simulate_fight(predator, prey) is False

    def test_full_simulation_run(self, simulation: Simulation) -> None:
        try:
            simulation.run_simulation()
            assert True
        except Exception as e:
            pytest.fail(f"Simulation failed with error: {e}")