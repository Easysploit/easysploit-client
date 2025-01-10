import pickle

class Data:
    TYPE_LIST = ["Screen", "Command", "Exit", "EXPLOIT", "Port", "Response", "Info"]
    def __init__(self, type: str, content: str):
        if type not in self.TYPE_LIST:
            raise ValueError(f"Invalid data found")
        self.type = type
        self.content = content
    def __repr__(self):
        return f"{self.type}: {self.content}"
    def __str__(self):
        return f"{self.type}: {self.content}"
    def __bytes__(self):
        return pickle.dumps(self)
    def __len__(self):
        return len(pickle.dumps(self))