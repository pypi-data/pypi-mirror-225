from abc import ABC, abstractmethod
from dataclasses import dataclass
from ._k_number import KNumber


@dataclass
class KInt(KNumber):
    _data: int

    def __repr__(self) -> str:
#       return f"KInt(value={self._data})"
        return str(self._data)
