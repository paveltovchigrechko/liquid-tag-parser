import json_parser
import liquid_parser

class Checker:
    """An abstract class that combines the JSON with source translation keys (JsonFile class)
    and directory with Liquid files (Dir class)."""
    def __init__(self, json_file_path, directories_list):
        self.json_file = json_parser.JsonFile(json_file_path)
        self.directories = []
        self.unknown_tags = []
        self.translation_keys_freq = {}
        self.has_unused_keys = False

        # Set paths for all directories
        self.set_directories(directories_list)

    def set_translation_keys_freq(self):
        """Sets a dictionary with keys as string from JSON translation keys and values as 0.
        Represents how often is a key is encountered across the directory Liquid files."""
        self.translation_keys_freq = dict.fromkeys(self.json_file.translation_keys, 0)

    def set_directories(self, directory_paths):
        """Sets the directories with Liquid files."""
        for dir_path in directory_paths:
            directory = liquid_parser.Dir(dir_path)
            self.directories.append(directory)

    def parse_files(self):
        """Runs the process method for each directory (Dir class) ."""
        for directory in self.directories:
            directory.process()

    def check_translation_tags(self):
        """Populates the translation_keys_freq dictionary.
        For each directory checks each found translation key for each file and either
        increases its counter in translation_keys_freq (if the key is found) or
        add it to unknown_tags list."""
        for directory in self.directories:
            for file in directory.parsed_liquid_files:
                for translation_tag in file.found_translation_keys:
                    if translation_tag.get_text() in self.json_file.translation_keys:
                        self.translation_keys_freq[translation_tag.get_text()] += 1
                    else:
                        self.unknown_tags.append((file.get_path(), translation_tag))

    def print_unused_translation_keys(self):
        """Prints unused translation keys found in directories files."""
        if not self.translation_keys_freq:
            print("No translation keys found")
            return

        print(f"Locale JSON file: {self.json_file.get_path()}")
        count = 1
        for tag, freq in self.translation_keys_freq.items():
            if freq == 0:
                self.has_unused_keys = True
                print(f"{count} Unused key: {tag}")
                count += 1
        if count == 1:
            print("Everything is OK, all keys are used.")

    # For debugging purposes
    def print_unknown_tags(self):
        for file, unknown_tag in self.unknown_tags:
            print(f"File: {file}, line {unknown_tag.get_line()}: unknown tag '{unknown_tag.get_text()}'")

    def run(self):
        """General method that does all in one.
        Scans JSON keys, directory files, checks the key usage, and prints unused keys.
        """
        # Scan JSON and extract keys
        self.json_file.scan_translation_keys()
        self.set_translation_keys_freq()

        self.parse_files()
        self.check_translation_tags()
        self.print_unused_translation_keys()
        # self.print_unknown_tags()


if __name__ == "__main__":
    pass
