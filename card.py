class Card:
    def __init__(self, name, seme, base_value, arcana="minor"):
        self.name = name
        self.seme = seme
        self.base_value = base_value
        self.arcana = arcana
        self.is_upside_down = False

    @property
    def orientation(self):
        return "Dritta" if not self.is_upside_down else "Rovesciata"

    def calculate_value(self, chosen_seme):
        value = self.base_value

        # Major Arcana: values 11+ use digit sum.
        if self.arcana == "major" and value >= 11:
            value = sum(int(digit) for digit in str(value))

        # Only matching Minor Arcana cards are doubled.
        if self.arcana == "minor" and self.seme == chosen_seme:
            value *= 2

        return value

    def flip(self):
        self.is_upside_down = not self.is_upside_down

    def __repr__(self):
        return f"Card({self.name!r}, {self.orientation}, {self.base_value})"
