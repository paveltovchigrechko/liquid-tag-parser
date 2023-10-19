import json

class JsonFile:
    def __init__(self, path):
        self._path = path
        self.translation_keys = set()

    def get_path(self):
        return self._path

    def _read_json_file(self):
        with open(self._path) as file:
            file_content = file.read()
            return json.loads(file_content)

    def get_translation_keys(self):
        content = self._read_json_file()
        for k1, v1 in content.items():
            if type(v1) is dict:
                for k2, v2 in v1.items():
                    if type(v2) is dict:
                        for k3, v3 in v2.items():
                            translation_key = ".".join([k1, k2, k3])
                            self.translation_keys.add(translation_key)
                    else:
                        translation_key = ".".join([k1, k2])
                        self.translation_keys.add(translation_key)
            else:
                self.translation_keys.add(k1)


if __name__ == "__main__":
    pass
