import json
import random
from pathlib import Path

from card import Card


class Deck:
    def __init__(self, cards_file=None):
        if cards_file is None:
            cards_file = Path(__file__).parent / "data" / "cards.json"

        self.cards_file = Path(cards_file)
        self.cards = []
        self.rebuild()

    def _load_cards(self):
        with self.cards_file.open("r", encoding="utf-8") as file:
            definitions = json.load(file)

        return [
            Card(
                name=item["name"],
                seme=item["seme"],
                base_value=item["base_value"],
                arcana=item["arcana"],
            )
            for item in definitions
        ]

    def shuffle(self):
        # Orientation is assigned here, not when drawing/revealing.
        for card in self.cards:
            card.is_upside_down = random.choice([False, True])
        random.shuffle(self.cards)

    def draw(self, n):
        n = max(0, int(n))
        amount = min(n, len(self.cards))
        drawn = self.cards[:amount]
        self.cards = self.cards[amount:]
        return drawn

    def return_to_middle(self, cards):
        if not cards:
            return

        middle = len(self.cards) // 2
        self.cards[middle:middle] = cards

    def discard(self, cards):
        # Cards are already removed by draw(); no discard pile is tracked.
        # This method exists to make the game action explicit.
        for card in cards:
            if card in self.cards:
                self.cards.remove(card)

    def is_empty(self):
        return len(self.cards) == 0

    def rebuild(self):
        self.cards = self._load_cards()
        self.shuffle()

    def __len__(self):
        return len(self.cards)
