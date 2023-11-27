import json_parser
import liquid_parser


class Checker:
    """An abstract class that combines the JSON with source translation keys (JsonFile class)
    and directory with Liquid files (Dir class)."""

    def __init__(self, json_file_path, directories_list):
        self.json_file = json_parser.JsonFile(json_file_path)
        self.directories = []
        self.unknown_tags = []
        self.liquid_translation_keys = set()
        self.unused_keys = set()
        self.has_unused_keys = False

        # Set paths for all directories
        self.set_directories(directories_list)

    def set_directories(self, directory_paths):
        """Sets the directories with Liquid files."""
        for dir_path in directory_paths:
            directory = liquid_parser.Dir(dir_path)
            self.directories.append(directory)

    def parse_files(self):
        """Run the process method for each directory (Dir class) ."""
        for directory in self.directories:
            directory.process()

    def check_translation_tags(self):
        for directory in self.directories:
            for file in directory.parsed_liquid_files:
                for tag in file.found_translation_keys:
                    self.liquid_translation_keys.add(tag.get_text())

        self.unused_keys = self.json_file.translation_keys.difference(self.liquid_translation_keys)
        if self.unused_keys:
            self.has_unused_keys = True

    def print_unused_translation_keys(self):
        print(f"Locale JSON file: {self.json_file.get_path()}")

        if not self.liquid_translation_keys:
            print("No translation keys found")
            return

        if self.has_unused_keys:
            count = 1
            for unused_key in self.unused_keys:
                print(f"{count} Unused key: {unused_key}")
                count += 1
        else:
            print("Everything is OK, all keys are used.")

    # For debugging purposes
    def print_unknown_tags(self):
        for file, unknown_tag in self.unknown_tags:
            print(f"File: {file}, line {unknown_tag.get_line()}: unknown tag '{unknown_tag.get_text()}'")

    def run(self):
        """General method that does all in one.
        Scan JSON keys, directory files, check the key usage, and print unused keys.
        """
        self.json_file.scan_translation_keys(max_level=3)
        self.parse_files()
        self.check_translation_tags()
        self.print_unused_translation_keys()


if __name__ == "__main__":
    pass
