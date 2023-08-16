from dataclasses import dataclass
from typing import Self


@dataclass
class Point:
    x: int = 0
    y: int = 0

    @property
    def decoding(self):
        return self.x, self.y

    def move(self, value: int):
        self.x += value
        self.y += value

    def __str__(self):
        return F'<{self.x},{self.y}>'

    def __mul__(self, other: int | float) -> Self:
        """:return Point with scaler x and y by other value"""
        if isinstance(other, (int, float)):
            return Point(int(self.x*other), int(self.y*other))
        else:
            ValueError(F"got unsupport type: {other}, expected int or float")
