import json
import os


class JsonFile:
    """A class that represents the content of a JSON file with locale translations.
    The JSON file can have up to 3 nested structures."""

    def __init__(self, path: str):
        self._path = os.path.abspath(path)
        self.translation_keys = set()

    def get_path(self) -> str:
        """Return the path to the JSON file."""
        return self._path

    def _read_json_file(self):
        """Read the content of a JSON file located in _path and deserializes its content."""
        with open(self._path) as file:
            file_content = file.read()
            return json.loads(file_content)

    def scan_translation_keys(self):
        """Scan the content of the JSON file up to the third nested structure and
        combines translation keys in a 'general.section.parameter' format.
        Adds all keys in translation_keys set."""
        content = self._read_json_file()
        for k1, v1 in content.items():
            if isinstance(v1, dict):
                for k2, v2 in v1.items():
                    if isinstance(v2, dict):
                        for k3, v3 in v2.items():
                            if isinstance(v3, dict):
                                pass
                                # for k4, v4 in v3.items():
                                #     translation_key = ".".join([k1, k2, k3, k4])
                                #     self.translation_keys.add(translation_key)
                            else:
                                translation_key = ".".join([k1, k2, k3])
                                self.translation_keys.add(translation_key)
                    else:
                        translation_key = ".".join([k1, k2])
                        self.translation_keys.add(translation_key)
            else:
                self.translation_keys.add(k1)


if __name__ == "__main__":
    pass
