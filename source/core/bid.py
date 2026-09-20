

class Bid:
    
    def __init__(self, face: int, quantity: int):
        self._ensure_valid_bid(face, quantity)
    
        self.face_value: int = face
        self.quantity:   int = quantity


    def __gt__(self, other: Bid) -> bool:
        """A bid is higher if quantity is greater for same face, or face is higher."""
        if not isinstance(other, Bid):
            raise ValueError(f"[Bid{self.__gt__.__name__}] Cannot compare Bid to {type(other)}")
        if self.face_value == other.face_value:
            return self.quantity > other.quantity
        return self.face_value > other.face_value
    
    @staticmethod
    def _ensure_valid_bid(face: int, quantity: int):
        if not (1 <= face <= 6) or quantity < 1:
            raise ValueError(f"Illegal bid values. Face 1-6, quantity >= 1, ")
        
        