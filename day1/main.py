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


def extract_numbers(lines):
    """
    Extracts numbers from each line in the given list of lines.

    Args:
        lines (list[str]): The list of lines containing numbers.

    Returns:
        list[list[str]]: A list of lists, where each inner list contains the extracted numbers from a line.
    """
    return [re.findall(r"\d", line) for line in lines]


def calibration_sum(numbers):
    """
    Calculates the sum of the first and last digits of each number in the given list of numbers.

    Args:
        numbers (list[list[str]]): The list of numbers.

    Returns:
        int: The sum of the first and last digits of each number.
    """
    return sum(int(n[0] + n[-1]) for n in numbers)


def perform_calibration(data):
    """
    Performs calibration on the given data by extracting numbers from each line,
    and calculating the sum of the first and last digits of each number.

    Args:
        data (str): The input data containing lines of numbers.

    Returns:
        int: The sum of the first and last digits of each number.
    """
    numbers = extract_numbers(data.split("\n"))
    return calibration_sum(numbers)


if __name__ == "__main__":
    # input_file_path = "test.txt"
    input_file_path = "input.txt"

    input_data = read_input_file(input_file_path)

    result = perform_calibration(input_data)
    print("Result part 1:", result)

    replacement_dict = {"one": "one1one", "two": "two2two", "three": "three3three",
                        "four": "four4four", "five": "five5five", "six": "six6six",
                        "seven": "seven7seven", "eight": "eight8eight", "nine": "nine9nine"}

    for old_str, new_str in replacement_dict.items():
        input_data = input_data.replace(old_str, new_str)

    result_part = perform_calibration(input_data)
    print("Result part 2:", result_part)
