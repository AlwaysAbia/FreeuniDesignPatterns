#Model for the Unit item
from typing import Optional
from uuid import UUID, uuid4


class Unit:
    def __init__(self, name: str, id: Optional[UUID] = None):
        self.id : UUID = id or uuid4()
        self.name : str = name