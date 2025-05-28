from dataclasses import dataclass


@dataclass
class Speed:
    _value: float

    def __init__(self, value: float):
        if not 0.5 <= value <= 2.0:
            raise ValueError("速度は0.5から2.0の間で指定してください")
        self._value = value

    def __str__(self) -> str:
        return f"atempo={self._value}"
