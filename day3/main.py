import math
import re


def read_input_file(path):
    """
    Reads the contents of a file and returns the stripped data.

    Args:
        path (str): The path to the file.

    Returns:
        list[str]: The list of stripped lines read from the file.
    """
    with open(path, "r") as file:
        data = [line.strip() for line in file]
    return data


def create_dict_coords_symbols(board):
    """
    Creates a dictionary with coordinates as keys and empty lists as values.

    Args:
        board (list[str]): The board representing the game.

    Returns:
        dict[tuple[int, int], list]: A dictionary with coordinates as keys and empty lists as values.
    """
    return {(_r, _c): []
            for _r in range(len(board))
            for _c in range(len(board[0]))
            if board[_r][_c] not in "0123456789."}


def find_adjacent_coords(r_idx, n_start, n_end):
    """
    Finds the adjacent coordinates based on the given row index and start and end positions.

    Args:
        r_idx (int): The row index.
        n_start (int): The start position.
        n_end (int): The end position.

    Returns:
        set: A set of adjacent coordinates as tuples.
    """
    return {(_r, _c)
            for _r in (r_idx - 1, r_idx, r_idx + 1)
            for _c in range(n_start - 1, n_end + 1)}


def update_symbol_coords(adj_chars, coords_edge_number, number):
    """
    Updates the symbol coordinates based on the given edge coordinates and number.

    Args:
        adj_chars (dict): The dictionary of symbol coordinates.
        coords_edge_number (set): The set of edge coordinates.
        number (int): The number to append to the symbol coordinates.

    Returns:
        None
    """
    for o in coords_edge_number & adj_chars.keys():
        adj_chars[o].append(number)


def process_schematic(schematic):
    """
    Processes the given schematic to find symbol coordinates.

    Args:
        schematic (list[str]): The schematic representing the game.

    Returns:
        dict[tuple[int, int], list]: A dictionary with symbol coordinates as keys and empty lists as values.
    """
    symbol_coords = create_dict_coords_symbols(schematic)

    for cur_r, row_data in enumerate(schematic):
        for number_match in re.finditer("\d+", row_data):
            edge = find_adjacent_coords(cur_r, number_match.start(), number_match.end())
            update_symbol_coords(symbol_coords, edge, int(number_match.group()))

    return symbol_coords


def sum_adjacent_values(symbol_coords):
    """
    Sums the adjacent values in the given symbol coordinates.

    Args:
        symbol_coords (dict[tuple[int, int], list]): A dictionary with symbol coordinates as keys and lists of values.

    Returns:
        int: The sum of the adjacent values in the symbol coordinates.
    """
    return sum(sum(p) for p in symbol_coords.values())


def sum_with_gear_ratios(symbol_coords):
    """
    Sums the products of gear ratios in the given symbol coordinates.

    Args:
        symbol_coords (dict[tuple[int, int], list]): A dictionary with symbol coordinates as keys and lists of values.

    Returns:
        int: The sum of the products of gear ratios in the symbol coordinates.
    """
    return sum(math.prod(p) for p in symbol_coords.values() if len(p) == 2)


if __name__ == "__main__":
    file_input_path = "input.txt"
    # file_input_path = "test.txt"
    schematic_data = read_input_file(file_input_path)

    symbol_coordinates = process_schematic(schematic_data)

    print("Part 1:"
          "\n\tThe sum of all part numbers in the engine schematic is:",
          sum_adjacent_values(symbol_coordinates))

    print("Part 2:"
          "\n\tThe sum of all gear ratios in the engine schematic is:",
          sum_with_gear_ratios(symbol_coordinates))
