

class Bid:
    
    def __init__(self, face: int, quantity: int):
        self._ensure_valid_bid(face, quantity)
    
        self.face_value: int = face
        self.quantity:   int = quantity


    def __gt__(self, other: Bid) -> bool:
    #- tested raiseError on invalid data
        """A bid is higher if quantity is greater for same face, or face is higher."""
        
        if not isinstance(other, Bid):
            raise ValueError(
                f"[{type(self).__name__}."
                f"{self.__gt__.__name__}]"
                f"Cannot compare Bid to {type(other).__name__}"
                )
            
        if self.face_value == other.face_value:
            return self.quantity > other.quantity
        return self.face_value > other.face_value
    
    @staticmethod
    def _ensure_valid_bid(face: int, quantity: int):
    #- tested raiseError on invalid data
        if not (1 <= face <= 6) or quantity < 1:
            raise ValueError(f"Illegal bid values. Face 1-6, quantity >= 1, ")
        
    def __str__(self):
        face_names = {1: "Ones", 2: "Twos", 3: "Threes", 4: "Fours", 5: "Fives", 6: "Sixes"}
        return f"{self.quantity}x{face_names[self.face_value]}"
        
        