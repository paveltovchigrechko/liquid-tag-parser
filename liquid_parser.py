from pathlib import Path
import re

TRANSLATION_TAG_PATTERN = re.compile(r"{{ '.+' \| t.*?}}")
TRANSLATION_KEY_PATTERN = re.compile(r"'.+'")


class TranslationTag:
    def __init__(self, line, tag):
        self._line = line
        self._text = tag

    def get_text(self):
        return self._text

    def get_line(self):
        return self._line

    def print_tag(self):
        print(f"Line {self._line}: {self._text}")


class LiquidFile:
    def __init__(self, path):
        self._path = path
        self.found_translation_tags = []

    def get_path(self):
        return self._path

    def get_translation_tags(self):
        return self.found_translation_tags

    def parse_translation_keys(self):
        with open(self._path) as file:
            for (line_num, line) in enumerate(file, start=1):
                t_tag = re.search(TRANSLATION_TAG_PATTERN, line)
                if t_tag:
                    translation_key = re.search(TRANSLATION_KEY_PATTERN, t_tag.group(0))
                    tag = TranslationTag(line_num, translation_key.group(0).strip("'"))
                    self.found_translation_tags.append(tag)

    def print_translation_tags(self):
        if not self.found_translation_tags:
            return

        print(f"File: {self._path}")
        for tag in self.found_translation_tags:
            tag.print_tag()


class Dir:
    def __init__(self, path):
        self.path = path
        self.filenames = []
        self.parsed_liquid_files = []

    def scan_filenames(self, extension=".liquid"):
        path = Path(self.path).absolute()
        self.filenames = list(path.glob(f'**/*{extension}'))

    def parse_files(self):
        if not self.filenames:
            return

        for filename in self.filenames:
            file = LiquidFile(filename)
            file.parse_translation_keys()
            self.parsed_liquid_files.append(file)

    # TODO: delete. For debugging purposes
    def print_tags(self):
        if not self.parsed_liquid_files:
            return

        for file in self.parsed_liquid_files:
            if file.found_translation_tags:
                file.print_translation_tags()
                print("="*60)

    def process(self):
        self.scan_filenames()
        self.parse_files()
        # self.print_tags()


if __name__ == "__main__":
    pass
