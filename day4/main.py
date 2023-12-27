def read_input_file(path):
    """
    Reads the contents of a file and returns them as a list of strings.

    Args:
        path (str): The path to the file to be read.

    Returns:
        list: A list of strings, where each string represents a line from the file.
    """
    with open(path, "r") as file:
        data = [line.strip().strip("\n") for line in file.readlines()]
    return data


class Scratchcard:
    """
    Represents a Scratchcard object.

    The Scratchcard class provides methods to initialize a card object, calculate the common numbers
    between the winning numbers and the scratched numbers, calculate the number of common numbers,
    and calculate the points earned based on the number of common numbers.

    Attributes:
        card_id (str): The ID of the card.
        winning_numbers (set): A set of winning numbers.
        scratched_numbers (set): A set of scratched numbers.

    Methods:
        __init__(card): Initializes a Card object with the provided card string.
        __str__(): Returns a formatted string representation of the Card object.
        calculate_winnings(): Calculates the common numbers between the winning numbers and the scratched numbers.
        number_of_winnings(): Calculates the number of common numbers between the winning numbers and the scratched numbers.
        calculate_points(): Calculates the points earned based on the number of common numbers.
    """
    def __init__(self, card):
        """
        Initializes a Card object with the provided card string.

        Args:
            card (str): The string representation of the card, in the format "Card ID: Winning Numbers | Scratched Numbers".

        Returns:
            None
        """
        parts = card.split(":")
        self.card_id = parts[0].split()[1]
        self.winning_numbers = set(map(int, parts[1].split("|")[0].split()))
        self.scratched_numbers = set(map(int, parts[1].split("|")[1].split()))

    def __str__(self):
        """
        Returns a formatted string representation of the Card object.

        Returns:
            str: A string representation of the Card object, including the card ID, winning numbers, scratched numbers, common numbers, and score.
        """
        return (
            f"Card {self.card_id :>3}: Winning numbers: {', '.join(map(str, self.winning_numbers)):>40}"
            f" | Scratched numbers: {', '.join(map(str, self.scratched_numbers)):>100}"
            f" | Common numbers: {', '.join(map(str, self.calculate_winnings())):<45}"
            f" | Score: {self.calculate_points():<5}")

    def calculate_winnings(self):
        """
        Calculates the common numbers between the winning numbers and the scratched numbers.

        Returns:
            set: A set containing the common numbers between the winning numbers and the scratched numbers.
        """
        # return self.winning_numbers & self.scratched_numbers
        return self.winning_numbers.intersection(self.scratched_numbers)

    def number_of_winnings(self):
        """
        Calculates the number of common numbers between the winning numbers and the scratched numbers.

        Returns:
            int: The number of common numbers between the winning numbers and the scratched numbers.
        """
        return len(self.calculate_winnings())

    def calculate_points(self):
        """
        Calculates the points earned based on the number of common numbers between the winning numbers and the scratched numbers.

        Returns:
            int: The points earned based on the number of common numbers. The points are calculated
            using the formula 2^(number_of_common_numbers - 1), unless there are no common numbers, in which case 0 points are earned.
        """
        power = self.number_of_winnings()
        return 2 ** (power - 1) if power > 0 else 0


class Deck:
    """
    Represents a Deck object.

    The Deck class provides methods to initialize a deck with a list of Scratchcard objects, calculate
    the total score of the deck, update the quantities of cards based on winnings, calculate the total
    number of cards in the deck, and return a formatted string representation of the deck.

    Attributes:
        deck (dict): A dictionary mapping card IDs to Scratchcard objects.
        quantities (dict): A dictionary mapping card IDs to their quantities in the deck.
        total_score (int): The total score of the deck.

    Methods:
        __init__(cards): Initializes a Deck object with the provided list of Scratchcard objects.
        __str__(): Returns a formatted string representation of the Deck object.
        deck_score(): Calculates the total score of the deck based on the points earned from each card.
        gain_cards(): Updates the quantities of cards in the deck based on the number of winnings associated with each card.
        number_of_cards_in_total(): Calculates the total number of cards in the deck.
    """

    def __init__(self, cards: list[Scratchcard]):
        """
        Initializes a Deck object with the provided list of Scratchcard objects.

        Args:
            cards (list[Scratchcard]): A list of Scratchcard objects representing the cards in the deck.

        Returns:
            None
        """
        self.deck = {int(card.card_id): card for card in cards}
        self.quantities = {int(card.card_id): 1 for card in cards}
        self.total_score = self.deck_score()

    def __str__(self):
        """
        Returns a formatted string representation of the Deck object.

        Returns:
            str: A string representation of the Deck object, including the card details and their quantities.
        """
        return "\n".join(
            f"{card} | Quantity: {self.quantities[idx]:>3}" for idx, card in self.deck.items()
        )

    def deck_score(self):
        """
        Calculates the total score of the deck based on the points earned from each card.

        Returns:
            int: The total score of the deck.
        """
        scores = [card.calculate_points() for card in self.deck.values()]
        return sum(scores)

    def gain_cards(self):
        """
        Updates the quantities of cards in the deck based on the number of winnings associated with each card.

        Returns:
            None
        """
        for idx, card in self.deck.items():
            number_of_wins = card.number_of_winnings()

            for d_idx in range(1, number_of_wins + 1):
                self.quantities[idx + d_idx] += self.quantities[idx]

    def number_of_cards_in_total(self):
        """
        Calculates the total number of cards in the deck.

        Returns:
            int: The total number of cards in the deck.
        """
        return sum(self.quantities.values())


if __name__ == "__main__":
    # file_input_path = "test.txt"
    file_input_path = "input.txt"

    file_data = read_input_file(file_input_path)

    scratchcards = [Scratchcard(line) for line in file_data]
    packet = Deck(scratchcards)

    print("Part 1:"
          "\n\tTotal score:", packet.total_score)

    packet.gain_cards()
    # print(packet)

    print("Part 2:"
          "\n\tTotal number of cards:", packet.number_of_cards_in_total())
