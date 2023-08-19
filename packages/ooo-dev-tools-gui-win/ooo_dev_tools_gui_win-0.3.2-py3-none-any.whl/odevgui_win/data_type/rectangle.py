from dataclasses import dataclass


@dataclass(frozen=True)
class Rectangle:
    left: int
    right: int
    top: int
    bottom: int
