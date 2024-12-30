#Model for the Unit item
from typing import Optional
from uuid import UUID, uuid4


class Unit:
    def __init__(self, name: str, id: Optional[UUID] = None) -> None:
        self.id : UUID = id or uuid4()
        self.name : str = name

    #For Testing
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Unit):
            return False
        return self.id == other.id and self.name == other.name