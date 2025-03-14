from pathlib import Path

class Properties:

    def get_file_path_pathlib(self, relative_path):
        """
        Constructs an absolute file path using pathlib.
        """
        current_dir = Path(__file__).parent.absolute()
        absolute_path = current_dir/relative_path
        return str(absolute_path)

    def __init__(self):
        file_path = self.get_file_path_pathlib("config.properties")
        print("****** ", file_path)
        self.properties = self._read_properties(file_path)

    def get_properties(self):
        return self.properties

    @staticmethod
    def _read_properties(file_path):
        properties = {}
        with open(file_path, "r") as f:
            for line in f:
                # Skip empty lines or comments
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    properties[key.strip()] = value.strip()
        return properties
