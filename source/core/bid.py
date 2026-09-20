
from dataclasses import dataclass

@dataclass
class Bid:
    
    # default values represent the state of the initial bid in the game
    face_value: int = 1
    quantity:   int = 0


    def __gt__(self, other: Bid) -> bool:
        """A bid is higher if quantity is greater for same face, or face is higher."""
        if not isinstance(other, Bid):
            raise ValueError(f"[Bid{self.__gt__.__name__}] Cannot compare Bid to {type(other)}")
        if self.face_value == other.face_value:
            return self.quantity > other.quantity
        return self.face_value > other.face_value