# Liar's Dice in Python

> *"All dice on the table. Nobody knows the truth. Everyone's bluffing."*

A fully-featured Python implementation of the classic **Liar's Dice** (Pirate Dice) game — playable by a human against one or more AI bots, complete with optional Wild Ones mode.

Built as a submission for a programming challenge. The goal: not just to implement the rules, but to make it genuinely fun to play.

---

## What Is Liar's Dice?

Liar's Dice is a hidden-information bluffing game. Every player secretly rolls five dice, then players take turns making bold claims about the total dice on the table — knowing full well they might be lying. When someone calls "Liar!", the dice are revealed. Whoever was wrong loses a die. Last one standing wins.

---

## ✨ Features

- 🧑‍💻 **Human vs. Bot(s)** — play against 1 to 4 AI opponents
- 🃏 **Wild Ones mode** — toggle the advanced rule where 1s count as any face
- 🤖 **Smart bot AI** — bots use probability-aware logic to bid and bluff
- 📜 **Full rule implementation** — bidding, challenging, elimination, round rotation

---

### Installation

```bash
# Clone the repository and navigate to the project directory:
git clone https://github.com/ITsvqt/liars-dice.git
cd liars-dice

# (Recommended) Create and activate a virtual environment:

# Windows (Command Prompt):
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

```

---

## 🎮 How to Play


In `root/source/main.py`, toggle the `IS_WEB_UI` flag to choose between the terminal and web UIs.

When enabled, the web UI starts a local server at http://127.0.0.1:8000


```bash
# Run the game
python main.py
```

On startup you will be asked:
1. Whats your battle tag 
2. How many bot opponents you want (1–4)
3. Whether to enable **Wild Ones** mode

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
