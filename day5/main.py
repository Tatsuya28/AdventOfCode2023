def read_input_file(path):
    """
    Reads the contents of a file and returns the data as a string.

    Args:
        path (str): The path to the file to be read.

    Returns:
        str: The contents of the file as a string.
    """
    with open(path, "r") as file:
        data = file.read().strip()
    return data


class Category:
    """
    Represents a category with its ID and map.

    Args:
        block (str): The block of data containing the title and maps.

    Attributes:
        category_id (str): The ID of the category.
        category_map (list): The map of the category.

    Methods:
        __init__(block): Initializes a Category object with the given block of data.
        __str__(): Returns a string representation of the Category object.
        convert_initial_seed(source_number): Converts the given source number based on the category map.
        convert_seed_range(seed_ranges_pair): Converts the given seed ranges based on the category map.
    """
    def __init__(self, block):
        """
        Initializes a Category object with the given block of data.

        Args:
            block (str): The block of data containing the title and maps.

        Returns:
            None
        """
        title, *maps = block.split("\n")
        self.category_id = title.strip(":").lower().replace("-", "_")
        self.category_map = [tuple(map(int, line.split())) for line in maps]

    def __str__(self):
        """
        Returns a string representation of the Category object.

        Returns:
            str: The string representation of the Category object.
        """
        map_str = "\n".join([f"{dest_start} {source_start} {length}"
                             for dest_start, source_start, length in self.category_map])

        return (f"{self.category_id}:"
                f"\n{map_str}"
                f"\n----------------------------")

    def convert_initial_seed(self, source_number):
        """
        Converts the given source number based on the category map.

        Args:
            source_number (int): The source number to be converted.

        Returns:
            int: The converted number based on the category map, or the original source number if no conversion is applicable.
        """
        # for destination_start, source_start, length in self.category_map:
        #         if source_start <= source_number < source_start + length:
        #             return destination_start + (source_number - source_start)
        #     return source_number
        return next((destination_start + (source_number - source_start)
                     for destination_start, source_start, length in self.category_map
                     if source_start <= source_number < source_start + length),
                    source_number)

    def convert_seed_range(self, seed_ranges_pair):
        """
        Converts the given seed ranges based on the category map.

        Args:
            seed_ranges_pair (list): A list of seed ranges to be converted.

        Returns:
            list: The converted seed ranges.

        """
        converted_ranges = []
        while len(seed_ranges_pair) > 0:
            start, end = seed_ranges_pair.pop()
            for destination_start, source_start, length in self.category_map:
                overlap_start = max(start, source_start)
                overlap_end = min(end, source_start + length)
                if overlap_start < overlap_end:
                    converted_start = overlap_start - source_start + destination_start
                    converted_end = overlap_end - source_start + destination_start
                    converted_ranges.append((converted_start, converted_end))
                    if overlap_start > start:
                        seed_ranges_pair.append((start, overlap_start))
                    if end > overlap_end:
                        seed_ranges_pair.append((overlap_end, end))
                    break
            else:
                converted_ranges.append((start, end))
        return converted_ranges


class Gardener:
    """
    Represents a gardener with the ability to parse an almanac and perform conversions on seed ranges.

    Attributes:
        initial_seeds (list): The initial seeds.
        seed_ranges (list): The seed ranges.
        categories (dict): The categories parsed from the almanac.

    Methods:
        __init__(data): Initializes the Gardener object with the given data by parsing the almanac.
        __str__(): Returns a string representation of the Gardener object.
        parse_almanac(data): Parses the almanac data and initializes the gardener's attributes.
        convert_to_location_initial_seeds(seed_number): Converts the given seed number to a location based on the category map.
        find_lowest_location_from_initial_seeds(): Finds the lowest location number from the initial seeds.
        convert_to_location_seed_ranges(seed_ranges_pair): Converts the given seed ranges to locations based on the category map.
        find_lowest_location_from_seed_ranges(): Finds the lowest location number from the seed ranges.
    """
    def __init__(self, data):
        """
        Initializes the object with the given data by parsing the almanac.

        Args:
            data (str): The data to be parsed.

        Returns:
            None
        """
        self.initial_seeds = []
        self.seed_ranges = []
        self.categories = {}

        self.parse_almanac(data)

    def __str__(self):
        """
        Returns a string representation of the Gardener object.

        Returns:
            str: The string representation of the Gardener object.
        """
        initial_seeds = f"Initial Seeds: {' '.join(map(str, self.initial_seeds))}"
        seed_range = f"Seeds Range: {' '.join(map(str, self.seed_ranges))}"
        categories = "\n".join([f"{key}:\n{value}" for key, value in self.categories.items()])
        return (f"{initial_seeds}"
                f"\n{seed_range}"
                f"\n{categories}")

    def parse_almanac(self, data: str):
        """
        Parses the almanac data and initializes the gardener's attributes.

        Args:
            data (str): The data to be parsed.

        Returns:
            None
        """
        seeds, *blocks = data.split("\n\n")
        self.initial_seeds = list(map(int, seeds.split(":")[1].split()))

        self.seed_ranges = [(int(self.initial_seeds[i]), int(self.initial_seeds[i]) + int(self.initial_seeds[i + 1]))
                            for i in range(0, len(self.initial_seeds), 2)]

        for idx, block in enumerate(blocks):
            category = Category(block)
            self.categories[idx] = category

    def convert_to_location_initial_seeds(self, seed_number):
        """
        Converts the given seed number to a location based on the category map.

        Args:
            seed_number (int): The seed number to be converted.

        Returns:
            int: The converted seed number based on the category map.
        """
        current_number = seed_number

        for category in self.categories.values():
            current_number = category.convert_initial_seed(current_number)
        return current_number

    def find_lowest_location_from_initial_seeds(self):
        """
        Finds the lowest location number from the initial seeds.

        Returns:
            int: The lowest location number from the initial seeds.
        """
        converted_locations = [self.convert_to_location_initial_seeds(seed) for seed in self.initial_seeds]
        return min(converted_locations)

    def convert_to_location_seed_ranges(self, seed_ranges_pair):
        """
        Converts the given seed ranges to locations based on the category map.

        Args:
            seed_ranges_pair (list): A list of seed ranges to be converted.

        Returns:
            list: The converted seed ranges.
        """
        seed_pair = seed_ranges_pair
        for category in self.categories.values():
            seed_pair = category.convert_seed_range(seed_pair)
        return seed_pair

    def find_lowest_location_from_seed_ranges(self):
        """
        Finds the lowest location number from the seed ranges.

        Returns:
            int: The lowest location number from the seed ranges.
        """
        seed_ranges_pair = self.seed_ranges
        seed_ranges_pair = self.convert_to_location_seed_ranges(seed_ranges_pair)

        return min(seed_ranges_pair)[0]


if __name__ == "__main__":
    # input_file_path = "test.txt"
    input_file_path = "input.txt"

    almanac_data = read_input_file(input_file_path)
    gardener = Gardener(almanac_data)
    print(gardener)

    print("Part 1:"
          f"\tThe lowest location number for the initial seeds is: {gardener.find_lowest_location_from_initial_seeds()}")

    # Optimization part 2: https://youtu.be/NmxHw_bHhGM, THANKS !
    print("Part 2:"
          f"\tThe lowest location number for the seed ranges is: {gardener.find_lowest_location_from_seed_ranges()}")
