import enum
from dataclasses import dataclass
from typing import Self

from temporal import Time

class Direction(enum.Enum):
    Down = enum.auto()
    Up = enum.auto()

@dataclass(frozen=  True)
class Velocity:
    direction: Direction
    delay: Time

    @classmethod
    def down(cls, delay: Time) -> Self:
        return cls(Direction.Down, delay)
    
    @classmethod
    def up(cls, delay: Time) -> Self:
        return cls(Direction.Up, delay)
    