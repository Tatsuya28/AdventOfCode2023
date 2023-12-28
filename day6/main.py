import math


def read_file_input(path):
    """
    Reads the contents of a file and returns the data as a string.

    Args:
        path (str): The path to the file.

    Returns:
        str: The contents of the file as a string.
    """
    with open(path, "r") as file:
        data = file.read().strip()
    return data


class Boat:
    """
    Boat class.

    Summary:
        Represents a boat.

    Explanation:
        This class provides functionality to control the speed of a boat. It allows setting the speed by holding a button and retrieving the speed when the button is released.

    Attributes:
        speed (int): The current speed of the boat.

    Methods:
        __init__(): Initializes a new instance of the class.
        hold_button(time): Sets the speed of the button hold.
        release_button(): Returns the speed of the button release.
    """

    def __init__(self):
        """
        Initializes a new instance of the class.

        Returns:
            None
        """
        self.speed = 0

    def hold_button(self, time):
        """
        Sets the speed of the button hold.

        Args:
            time (int): The time in milliseconds for which the button should be held.

        Returns:
            None
        """
        self.speed = time

    def release_button(self):
        """
        Returns the speed of the button release.

        Returns:
            int: The speed of the button release.
        """
        return self.speed


class BoatRace:
    """
    Represents a boat race.

    Attributes:
        times (list): A list of race times for each race.
        records (list): A list of distance records to beat for each race.
        race_data (dict): A dictionary mapping race keys to race times and records.
        unique_time (int): The unique time value.
        unique_record (int): The unique record value.

    Methods:
        __init__(data): Initializes a new instance of the class.
        __str__(): Returns a string representation of the object.
        calculate_ways_to_win_for_all_races(): Calculates the ways to win for all races.
        calculate_ways_to_win_for_one_race(duration, distance_record): Calculates the number of ways to win for one race.
        multiply_ways_to_win(): Multiplies the ways to win for all races.
    """

    def __init__(self, data):
        """
        Initializes a new instance of the class.

        Args:
            data (str): The input data used to initialize the class.

        Returns:
            None
        """
        keys = [line.split(":")[0].lower() for line in data.split("\n")]
        self.times, self.records = [list(map(int, line.split(":")[1].split()))
                                    for line in data.split("\n")]
        self.race_data = dict(zip(keys, [self.times, self.records]))
        self.unique_time, self.unique_record = [int(line.replace(" ", "").split(":")[1])
                                                for line in data.split("\n")]

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: A string representation of the object.
        """
        return (f"race_data: {self.race_data}\n"
                f"times: {self.times}\n"
                f"records: {self.records}\n"
                f"unique time: {self.unique_time}\n"
                f"unique record: {self.unique_record}")

    def calculate_ways_to_win_for_all_races(self):
        """
        Calculates the ways to win for all races.

        Returns:
            list: A list of ways to win for each race.
        """
        return [self.calculate_ways_to_win_for_one_race(duration, record)
                for duration, record in zip(self.times, self.records)]

    def calculate_ways_to_win_for_one_race(self, duration, distance_record):
        """
        Calculates the number of ways to win for one race.

        Args:
            duration (int): The total duration of the race.
            distance_record (int): The distance record to beat.

        Returns:
            int: The number of ways to win for the race.
        """
        boat = Boat()
        first_time = 0

        for hold_time in range(duration + 1):
            boat.hold_button(hold_time)
            speed = boat.release_button()
            remaining_time = duration - hold_time
            distance = speed * remaining_time

            if distance > distance_record:
                first_time = hold_time
                break
        last_time = duration - first_time
        return last_time - first_time + 1

    def multiply_ways_to_win(self):
        """
        Multiplies the ways to win for all races.

        Returns:
            int: The product of the ways to win for each race.
        """
        ways = self.calculate_ways_to_win_for_all_races()
        return math.prod(ways)


if __name__ == "__main__":
    # input_file_path = "test.txt"
    input_file_path = "input.txt"

    races_data = read_file_input(input_file_path)

    races = BoatRace(races_data)
    print(races)

    print("Part 1:\n"
          "\tThe result of the multiplication of the number of ways to win is:",
          races.multiply_ways_to_win())

    print("Part 2:\n"
          "\tThe number of ways you can beat the much longer race is:",
          races.calculate_ways_to_win_for_one_race(races.unique_time, races.unique_record))
