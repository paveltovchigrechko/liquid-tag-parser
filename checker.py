from sys import exit

import json_parser
import liquid_parser

class Checker:
    def __init__(self, json_file_path, directories_list):
        self.json_file = json_parser.JsonFile(json_file_path)
        self.directories = []
        self.unknown_tags = []
        self.translation_keys_freq = {}
        self.has_unused_keys = False

        # Scan JSON and extract keys
        self.json_file.get_translation_keys()
        self.set_translation_keys_freq()

        # Set paths for all directories
        self.set_directories(directories_list)

    def set_translation_keys_freq(self):
        self.translation_keys_freq = dict.fromkeys(self.json_file.translation_keys, 0)

    def set_directories(self, directory_paths):
        for dir_path in directory_paths:
            directory = liquid_parser.Dir(dir_path)
            self.directories.append(directory)

    def parse_files(self):
        for directory in self.directories:
            directory.process()

    def check_translation_tags(self):
        for directory in self.directories:
            for file in directory.parsed_liquid_files:
                for translation_tag in file.found_translation_tags:
                    if translation_tag.get_text() in self.json_file.translation_keys:
                        self.translation_keys_freq[translation_tag.get_text()] += 1
                    else:
                        self.unknown_tags.append((file.get_path(), translation_tag))

    def print_unused_translation_keys(self):
        if not self.translation_keys_freq:
            print("No translation keys found")
            return

        print(f"Locale JSON file: {self.json_file.get_path()}")
        for tag, freq in self.translation_keys_freq.items():
            if freq == 0:
                self.has_unused_keys = True
                print(f"Not used tag: {tag}")

        # exit("Found unused translation keys!")

    # For debugging purposes
    def print_unknown_tags(self):
        for file, unknown_tag in self.unknown_tags:
            print(f"File: {file}, line {unknown_tag.get_line()}: unknown tag '{unknown_tag.get_text()}'")


    def run(self):
        self.parse_files()
        self.check_translation_tags()
        self.print_unused_translation_keys()
        # self.print_unknown_tags()


if __name__ == "__main__":
    pass
