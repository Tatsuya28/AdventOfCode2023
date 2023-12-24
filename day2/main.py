import re


def read_input_file(path):
    """
    Reads the contents of a file and returns the stripped data.

    Args:
        path (str): The path to the file.

    Returns:
        str: The stripped data read from the file.
    """

    with open(path, "r") as file:
        data = file.read().strip()
    return data


def parse_data(data):
    """
    Parses the given data to extract game information.

    Args:
        data (str): The input data to be parsed.

    Returns:
        list[tuple[int, list[str]]]: A list of tuples, where each tuple represents a game with its ID and subsets.
    """
    regex = r"Game (\d+): (.+?)$"
    matches = re.findall(regex, data, re.MULTILINE)
    games = []
    for match in matches:
        id_game, subsets_str = match
        subsets_list = [subset.strip() for subset in subsets_str.split(";")]
        games.append((int(id_game), subsets_list))

    return games


def parse_subset(subset):
    """
    Parses the given subset to extract color and count information.

    Args:
        subset (str): The subset string to be parsed.

    Returns:
        dict: A dictionary mapping colors to their corresponding counts.
    """
    matches = re.findall(r"(\d+) (\w+)", subset)
    return {color: int(count) for count, color in matches}


def is_possible(subsets_list: list[str], cube_counts_ref):
    """
    Checks if it is possible to create the given subsets using the available cube counts.

    Args:
        subsets_list (list[str]): The list of subsets to check.
        cube_counts_ref (dict[str, int]): The available cube counts for each color.

    Returns:
        bool: True if it is possible to create the subsets using the available cube counts, False otherwise.
    """
    for subset in subsets_list:
        game_counts = parse_subset(subset)
        for color in cube_counts_ref:
            if game_counts.get(color, 0) > cube_counts_ref[color]:
                return False
    return True


def find_minimum_set(subsets_list):
    """
    Finds the minimum set of cube counts required to create the given subsets.

    Args:
        subsets_list (list[str]): The list of subsets.

    Returns:
        dict[str, int]: A dictionary representing the minimum set of cube counts required, with keys as colors and values as counts.
    """
    minimum_set = {color: 0 for color in ["red", "green", "blue"]}
    for subset in subsets_list:
        game_counts = parse_subset(subset)
        for color in minimum_set:
            minimum_set[color] = max(minimum_set[color], game_counts.get(color, 0))
    return minimum_set


def calculate_power(game_counts):
    """
    Calculates the power based on the given game counts.

    Args:
        game_counts (dict[str, int]): A dictionary representing the game counts, with keys as colors and values as counts.

    Returns:
        int: The calculated power based on the game counts.
    """
    return game_counts["red"] * game_counts["green"] * game_counts["blue"]


if __name__ == "__main__":
    cube_counts = {"red": 12, "green": 13, "blue": 14}

    input_file_path = "input.txt"
    # input_file_path = "test.txt"

    input_data = read_input_file(input_file_path)
    games_data = parse_data(input_data)

    possible_games = []
    sum_of_powers = 0

    for game_id, subsets in games_data:
        if is_possible(subsets, cube_counts):
            possible_games.append(game_id)

        min_set = find_minimum_set(subsets)
        power = calculate_power(min_set)
        sum_of_powers += power

    print("Part 1:\n"
          "\tGames that would have been possible:", possible_games,
          "\n\tSum of the IDs of those games:", sum(possible_games))

    print("Part 2:\n"
          "\tSum of the powers of minimum sets:", sum_of_powers)
