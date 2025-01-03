import pytest

from creature import (
    ClawSize,
    Creature,
    CreatureBuilder,
    TeethSharpness,
)


class TestCreature:
    @pytest.fixture
    def default_creature(self) -> Creature:
        """Creates a creature with default values."""
        return Creature()

    @pytest.fixture
    def custom_creature(self) -> Creature:
        """Creates a creature with custom attributes."""
        return Creature(
            legs=2,
            wings=2,
            health=150,
            stamina=80,
            position=5,
        )

    @pytest.fixture
    def combat_creature(self) -> Creature:
        """Creates a creature with combat-focused attributes."""
        return Creature(
            base_attack=10,
            claw_multiplier=ClawSize.MEDIUM.value,
            teeth_bonus=TeethSharpness.SHARP.value,
        )

    def test_default_creature_creation(self, default_creature: Creature) -> None:
        assert default_creature.legs == 0
        assert default_creature.wings == 0
        assert default_creature.health == 100
        assert default_creature.stamina == 100
        assert default_creature.position == 0

    def test_get_attack_power(self, combat_creature: Creature) -> None:
        assert combat_creature.get_attack_power() == 36  # (10 * 3) + 6

    def test_creature_custom_attributes(self, custom_creature: Creature) -> None:
        assert custom_creature.legs == 2
        assert custom_creature.wings == 2
        assert custom_creature.health == 150
        assert custom_creature.stamina == 80
        assert custom_creature.position == 5


class TestCreatureBuilder:
    @pytest.fixture
    def builder(self) -> CreatureBuilder:
        """Creates a fresh CreatureBuilder instance."""
        return CreatureBuilder()

    @pytest.fixture
    def fully_equipped_creature(self, builder: CreatureBuilder) -> Creature:
        """Creates a creature with all attributes set."""
        return (
            builder.add_legs(2)
            .add_wings(2)
            .add_claws(ClawSize.LARGE)
            .add_teeth(TeethSharpness.VERY_SHARP)
            .set_health(120)
            .set_stamina(90)
            .set_base_attack(15)
            .set_position(5)
            .build()
        )

    def test_builder_basic_creation(self, builder: CreatureBuilder) -> None:
        creature = builder.build()
        assert isinstance(creature, Creature)

    def test_builder_with_attributes(
        self, fully_equipped_creature: Creature
    ) -> None:
        assert fully_equipped_creature.legs == 2
        assert fully_equipped_creature.wings == 2
        assert fully_equipped_creature.claw_multiplier == ClawSize.LARGE.value
        assert fully_equipped_creature.teeth_bonus == TeethSharpness.VERY_SHARP.value
        assert fully_equipped_creature.health == 120
        assert fully_equipped_creature.stamina == 90
        assert fully_equipped_creature.base_attack == 15
        assert fully_equipped_creature.position == 5

    def test_builder_reset(self, builder: CreatureBuilder) -> None:
        first_creature = builder.add_legs(2).build()
        second_creature = builder.build()

        assert first_creature.legs == 2
        assert second_creature.legs == 0

    def test_builder_chaining(self, builder: CreatureBuilder) -> None:
        creature = builder.add_legs(1).add_wings(1).build()

        assert creature.legs == 1
        assert creature.wings == 1