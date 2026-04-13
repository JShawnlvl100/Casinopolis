class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.calculate_value()

    def calculate_value(self):
        self.value = 0
        self.aces = 0
        
        # Define values for ranks
        values = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "10": 10, "j": 10, "q": 10, "k": 10, "a": 11
        }

        # Initial calculation
        for card in self.cards:
            self.value += values[card.rank]
            if card.rank == "a":
                self.aces += 1

        # Adjust for Aces if we are busting
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        # Useful for debugging in the console!
        return f"Hand Value: {self.value}"