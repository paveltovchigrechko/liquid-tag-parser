from pathlib import Path
import re

# Represents a Liquid translation tag pattern: {{ 'any_text' | t 'optional_text' }}
TRANSLATION_TAG_PATTERN = re.compile(r"{{ '.+' \| t.*?}}")
# Represents a translation key passed into a Liquid translation tag: 'any_text'
TRANSLATION_KEY_PATTERN = re.compile(r"'.+'")


class TranslationTag:
    """A class that represents a single Liquid translation key found in a Liquid file.
    Liquid translation tag has format {{ 'translation_key' | t }}."""
    def __init__(self, line, tag):
        self._line = line
        self._text = tag

    def get_text(self) -> str:
        """Return the text (aka translation key) passed into the tag."""
        return self._text

    def get_line(self) -> int:
        """Return the line in a file where the tag is located."""
        return self._line

    def __repr__(self):
        print(f"Line: {self._line}: {self._text}")


class LiquidFile:
    """A class that represents a Liquid file."""
    def __init__(self, path):
        self._path = path
        self.found_translation_keys = set()

    def get_path(self) -> str:
        """Return the path to a Liquid file."""
        return self._path

    def get_translation_keys(self) -> set:
        """Return the list of translation keys found in the Liquid file."""
        return self.found_translation_keys

    def parse_translation_keys(self):
        """Open a Liquid file by indicated path, search for translation tags in
        the file content, extract translation keys passed in tags, and add them in
        found_translation_keys list with their lines in file."""
        try:
            with open(self._path) as file:
                for (line_num, line) in enumerate(file, start=1):
                    t_tag = re.search(TRANSLATION_TAG_PATTERN, line)
                    if t_tag:
                        translation_key = re.search(TRANSLATION_KEY_PATTERN, t_tag.group(0))
                        tag = TranslationTag(line_num, translation_key.group(0).strip("'"))
                        self.found_translation_keys.add(tag)
        except FileNotFoundError:
            print(f"File {self._path} was not found.")

    def print_translation_keys(self):
        """Print all translation keys found in Liquid file.
        Does nothing if the found_translation_keys list is empty."""
        if not self.found_translation_keys:
            return

        print(f"File: {self._path}")
        for tag in self.found_translation_keys:
            print(tag)


class Dir:
    """A class that represents a directory with Liquid files."""
    def __init__(self, path):
        self.path = path
        self.filenames = []
        self.parsed_liquid_files = []

    def scan_filenames(self, extension=".liquid"):
        """Scan all files recursively in directory path that have .liquid extension
        and adds them into filenames list."""
        path = Path(self.path).absolute()
        self.filenames = list(path.glob(f'**/*{extension}'))

    def parse_files(self):
        """For each file in filenames list create a new LiquidFile object, parse its
        translation keys, and add the object into parsed_liquid_files list.
        Do nothing if filenames list is empty."""
        if not self.filenames:
            return

        for filename in self.filenames:
            file = LiquidFile(filename.resolve())
            file.parse_translation_keys()
            self.parsed_liquid_files.append(file)

    def process(self):
        """General method that consequently scans all Liquid files in the directory and
        parses their translation keys."""
        self.scan_filenames()
        self.parse_files()


if __name__ == "__main__":
    pass
