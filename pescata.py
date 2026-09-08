class Pescata:
    def __init__(self, deck, number_of_cards, chosen_seme):
        self.deck = deck
        self.number_of_cards = number_of_cards
        self.chosen_seme = chosen_seme

        self.drawn_cards = []
        self.upright_total = 0
        self.upside_down_total = 0

        self.deck_finished = False
        self.deck_rebuilt = False
        self.resolved = False
            
    def draw(self):
        # If the requested draw exceeds the remaining deck, use what remains.
        self.drawn_cards = self.deck.draw(self.number_of_cards)

        # Remember that this draw exhausted the deck.
        # The deck will be rebuilt after the Pescata is resolved.
        self.deck_finished = self.deck.is_empty()

        return self.drawn_cards

    def reveal(self):
        # Orientation was already assigned by Deck.shuffle().
        # Revealing only exposes the existing orientation.
        return self.drawn_cards

    def calculate_totals(self):
        self.upright_total = 0
        self.upside_down_total = 0

        for card in self.drawn_cards:
            value = card.calculate_value(self.chosen_seme)

            if card.is_upside_down:
                self.upside_down_total += value
            else:
                self.upright_total += value

        return self.upright_total, self.upside_down_total

    def cheat(self, cards_to_flip):
        for card in cards_to_flip:
            if card in self.drawn_cards:
                card.flip()

        return self.calculate_totals()

    def resolve(self):
        self.calculate_totals()

        if self.upright_total > self.upside_down_total:
            self.winner = "Dritta"
        elif self.upside_down_total > self.upright_total:
            self.winner = "Rovesciata"
        else:
            self.winner = "Pareggio"

        if self.winner == "Dritta":
            winning = [c for c in self.drawn_cards if not c.is_upside_down]
            losing = [c for c in self.drawn_cards if c.is_upside_down]
        elif self.winner == "Rovesciata":
            winning = [c for c in self.drawn_cards if c.is_upside_down]
            losing = [c for c in self.drawn_cards if not c.is_upside_down]
        else:
            # The spec defines higher-total winner only; on a tie, no side wins.
            # Return all cards to the middle rather than discarding either side.
            winning = []
            losing = list(self.drawn_cards)

        self.deck.return_to_middle(losing)
        self.deck.discard(winning)
        self.resolved = True

        return {
            "winner": self.winner,
            "winning_cards": winning,
            "losing_cards": losing,
            "upright_total": self.upright_total,
            "upside_down_total": self.upside_down_total,
        }
