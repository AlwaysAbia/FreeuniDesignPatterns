import pytest

from creature import (
    Creature,
    CrawlStrategy,
    FlyHandler,
    FlyStrategy,
    HopHandler,
    HopStrategy,
    MovementHandler,
    RunHandler,
    RunStrategy,
    WalkHandler,
    WalkStrategy,
)


class TestMovementStrategies:
    @pytest.fixture
    def high_stamina(self) -> int:
        return 100

    @pytest.fixture
    def low_stamina(self) -> int:
        return 0

    def test_crawl_strategy(self, high_stamina: int, low_stamina: int) -> None:
        strategy = CrawlStrategy()
        assert strategy.move(high_stamina) == (1, 1)
        assert strategy.move(low_stamina) == (1, 1)

    def test_hop_strategy(self, high_stamina: int, low_stamina: int) -> None:
        strategy = HopStrategy()
        assert strategy.move(high_stamina) == (3, 2)
        assert strategy.move(low_stamina) == (0, 0)

    def test_walk_strategy(self, high_stamina: int, low_stamina: int) -> None:
        strategy = WalkStrategy()
        assert strategy.move(high_stamina) == (4, 2)
        assert strategy.move(low_stamina) == (0, 0)

    def test_run_strategy(self, high_stamina: int, low_stamina: int) -> None:
        strategy = RunStrategy()
        assert strategy.move(high_stamina) == (6, 4)
        assert strategy.move(low_stamina) == (0, 0)

    def test_fly_strategy(self, high_stamina: int, low_stamina: int) -> None:
        strategy = FlyStrategy()
        assert strategy.move(high_stamina) == (8, 4)
        assert strategy.move(low_stamina) == (0, 0)


class TestMovementChain:
    @pytest.fixture
    def movement_chain(self) -> MovementHandler:
        return FlyHandler(RunHandler(WalkHandler(HopHandler())))

    def test_fly_capable_creature(self, movement_chain: MovementHandler) -> None:
        creature = Creature(wings=2, stamina=100)
        strategy = movement_chain.handle(creature)
        assert isinstance(strategy, FlyStrategy)

    def test_run_capable_creature(self, movement_chain: MovementHandler) -> None:
        creature = Creature(legs=2, stamina=100)
        strategy = movement_chain.handle(creature)
        assert isinstance(strategy, RunStrategy)

    def test_walk_capable_creature(self, movement_chain: MovementHandler) -> None:
        creature = Creature(legs=2, stamina=30)
        strategy = movement_chain.handle(creature)
        assert isinstance(strategy, WalkStrategy)

    def test_hop_capable_creature(self, movement_chain: MovementHandler) -> None:
        creature = Creature(legs=1, stamina=100)
        strategy = movement_chain.handle(creature)
        assert isinstance(strategy, HopStrategy)

    def test_crawl_only_creature(self, movement_chain: MovementHandler) -> None:
        creature = Creature(stamina=100)
        strategy = movement_chain.handle(creature)
        assert isinstance(strategy, CrawlStrategy)

    def test_chain_order(self, movement_chain: MovementHandler) -> None:
        creature = Creature(legs=2, wings=2, stamina=100)
        strategy = movement_chain.handle(creature)
        assert isinstance(strategy, FlyStrategy)  # Should choose fly over run

    def test_insufficient_stamina_movement(
        self, movement_chain: MovementHandler
    ) -> None:
        creature = Creature(legs=2, wings=2, stamina=0)
        strategy = movement_chain.handle(creature)
        speed, cost = strategy.move(creature.stamina)
        assert speed == 0
        assert cost == 0