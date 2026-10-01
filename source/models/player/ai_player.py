import random
import time

from models.player.base.player import Player
from models.bid import Bid

class AIPlayer(Player):
    
    
    def __init__(self, name: str, aggression: float):
        super().__init__(name)
        # aggression: 0.0 = cautious, 1.0 = reckless bluffer
        self.is_bot = True
        self.aggression = aggression
        

            
    def calc_turn(self, current_bid: Bid | None, total_dice: int, wild_ones: bool) -> tuple[str, Bid | None]:
        """Returns ('bid', Bid) or ('challenge', None)."""
        time.sleep(random.uniform(0.6, 1.4))  # Simulate thinking

        unknown_dice = total_dice - self.cnt_dice

        # --- Decide whether to challenge ---
        if current_bid is not None:
            prob = self._probability_of_bid(current_bid, unknown_dice, wild_ones)
            # Challenge threshold: lower aggression = more likely to challenge
            challenge_threshold = 0.35 - (self.aggression * 0.15)
            if prob < challenge_threshold:
                return ("Challenge", None)

        # --- Place a bid ---
        new_bid = self._choose_bid(current_bid, total_dice, wild_ones)
        return ("Bid", (new_bid.face_value, new_bid.quantity))

    def _choose_bid(self, current_bid: Bid | None, total_dice: int, wild_ones: bool) -> Bid:
        """Choose a smart bid that is higher than current_bid."""
        # Count what the bot can see
        best_face = max(range(1, 7), key=lambda f: self._count_face(f, wild_ones))
        known_qty = self._count_face(best_face, wild_ones)

        # Conservative estimate of how many exist on the table
        p = 1 / 6 if not wild_ones or best_face == 1 else 2 / 6
        expected_total = known_qty + int((total_dice - self.cnt_dice) * p)

        # Sometimes bluff above what we expect
        bluff_boost = 1 if random.random() < self.aggression * 0.4 else 0
        target_qty = max(1, expected_total + bluff_boost)

        candidate = Bid(target_qty, best_face)

        # If candidate isn't higher, increment quantity or face
        if not candidate > current_bid and current_bid is not None:
            # Try bumping quantity on the same face
            candidate = Bid(current_bid.quantity + 1, current_bid.face_value)
            # If that's not plausible, move to a higher face
            if current_bid.face_value < 6 and random.random() < 0.4:
                new_face = current_bid.face_value + 1
                candidate = Bid(max(1, current_bid.quantity - 1), new_face)
                if not candidate > current_bid:
                    candidate = Bid(current_bid.quantity, new_face)

        # Final safety: just bump quantity
        if not candidate > current_bid and current_bid is not None:
            candidate = Bid(current_bid.quantity + 1, current_bid.face_value)


        print(
            f"{self.name}: current={current_bid}, "
            f"candidate={candidate}, "
            f"valid={current_bid is None or candidate > current_bid}"
        )
        return candidate

    def _probability_of_bid(self, bid: Bid, unknown_dice: int, wild_ones: bool) -> float:
        """
        Estimate probability that bid holds, given how many dice the bot can see.
        Uses binomial distribution approximation.
        """
        known_count = self._count_face(bid.face_value, wild_ones)
        needed = max(0, bid.quantity - known_count)

        if needed == 0:
            return 1.0
        if needed > unknown_dice:
            return 0.0

        # Probability each unknown die matches face
        p = 1 / 6 if not wild_ones or bid.face_value == 1 else 2 / 6

        # Binomial CDF approximation: P(X >= needed) where X ~ Binomial(unknown_dice, p)
        from math import comb
        prob = 0.0
        for k in range(needed, unknown_dice + 1):
            prob += comb(unknown_dice, k) * (p ** k) * ((1 - p) ** (unknown_dice - k))
        return prob
            
            
    def _count_face(self, face: int, wild_ones: bool = False) -> int:
        """Count how many dice show a given face, optionally counting 1s as wild."""
        total = self.values.count(face)
        if wild_ones and face != 1:
            total += self.values.count(1)
        return total
    
    def __str__(self):
        return super().__str__() + f" aggresion: {self.aggression}"