# 🎲 Liar's Dice in Python

> *"All dice on the table. Nobody knows the truth. Everyone's bluffing."*

A fully-featured Python implementation of the classic **Liar's Dice** (Pirate Dice) game — playable by a human against one or more AI bots, complete with optional Wild Ones mode.

Built as a submission for a programming challenge. The goal: not just to implement the rules, but to make it genuinely fun to play.

---

## 🏴‍☠️ What Is Liar's Dice?

Liar's Dice is a hidden-information bluffing game. Every player secretly rolls five dice, then players take turns making bold claims about the total dice on the table — knowing full well they might be lying. When someone calls "Liar!", the dice are revealed. Whoever was wrong loses a die. Last one standing wins.

---

## ✨ Features

- 🧑‍💻 **Human vs. Bot(s)** — play against 1 to 5 AI opponents
- 🎯 **Configurable player count** — choose how many bots join the table
- 🃏 **Wild Ones mode** — toggle the advanced rule where 1s count as any face
- 🤖 **Smart bot AI** — bots use probability-aware logic to bid and bluff
- 📜 **Full rule implementation** — bidding, challenging, elimination, round rotation

---

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/pirate-dice.git
cd pirate-dice

# (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

---

## 🎮 How to Play

```bash
# Clone the repo
git clone https://github.com/your-username/liars-dice.git
cd source

# Run the game
python main.py
```

On startup you will be asked:
1. How many bot opponents you want (1–5)
2. Whether to enable **Wild Ones** mode

Then the game begins. On your turn, you can:
- **Bid** — announce a quantity and face value higher than the current bid
- **Challenge** — call the last bidder a liar and reveal all dice

---

## 📐 Rules Summary

| Situation | Result |
|---|---|
| Bid holds up (count ≥ bid) | Challenger loses 1 die |
| Bid was a bluff (count < bid) | Bidder loses 1 die |
| Player loses all dice | Eliminated |
| Last player with dice | Winner 🏆 |

**Wild Ones (optional):** When counting dice for any bid on face *X*, all 1s on the table also count toward face *X*.

**Round start:** The loser of the previous round opens the bidding. If they were eliminated, the next player clockwise goes first.



## 🙌 Acknowledgements

Built as part of a programming challenge to reimagine a classic game with clean code, solid rules, and a bot that actually puts up a fight.
