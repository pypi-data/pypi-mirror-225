from pathlib import Path


class LogObject:
    def __init__(self):
        self.log = []

    def add(self, path, msg, level="error"):
        self.log.append({"path": path, "msg": msg, "level": level})

    def get_logs(self, level=None):
        if level is None:
            return self.log
        assert level in ["error", "warning"], "Invalid level, must be 'error' or 'warning'"
        return [i for i in self.log if i["level"] == level]

    def print_logs(self, level=None):
        for i in self.get_logs(level=level):
            print("=" * 50)
            print(f"Path: {i['path']}")
            print(f"Message: {i['msg']}")
            print(f"Level: {i['level']}")

    def write_logs(self, path, level=None):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            for i in self.get_logs(level=level):
                f.write("=" * 50 + "\n")
                f.write(f"Path: {i['path']}\n")
                f.write(f"Message: {i['msg']}\n")
                f.write(f"Level: {i['level']}\n")


class LogHelper:
    def __init__(self, log: LogObject, prepend_path: list):
        self.log = log
        self.prepend_path = prepend_path

    def add(self, path, msg, level="error"):
        self.log.add(path=self.prepend_path + path, msg=msg, level=level)
