from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from DPAssignment2.src.db.repository.unit_repository import UnitRepository
from DPAssignment2.src.models.unit import Unit


class IUnitService(ABC):
    @abstractmethod
    def create_unit(self, name:str) -> Unit:
        pass

    @abstractmethod
    def read_unit(self, id: UUID) -> Unit:
        pass

    @abstractmethod
    def list_units(self) -> List[Unit]:
        pass

#This Service Layer class adds nothing to the
#Existing repo layer, but I added it for consistency
#Since I added the layer for other classes
class UnitService(IUnitService):
    def __init__(self, unit_repo: UnitRepository) -> None:
        self.unit_repo = unit_repo

    def create_unit(self, name:str) -> Unit:
        if name == "":
            raise ValueError("Can't create unit with no name")
        return self.unit_repo.create_unit(name)

    def read_unit(self, id: UUID) -> Optional[Unit]:
        return self.unit_repo.read_unit(id)

    def list_units(self) -> List[Unit]:
        return self.unit_repo.list_units()