import json
import threading
from json import JSONDecodeError


class Data:
    lock = threading.Lock()

    def __init__(self, file_name: str):
        self.file_name = file_name
        try:
            self.data = json.load(open(file_name, 'r', encoding='utf-8'))
        except (FileNotFoundError, JSONDecodeError):
            self.data = {}
        self._privte = 15

    def __call__(self, key, from_list: list = None, loop: bool = False):
        return self.get(key, from_list, loop)

    def get(self, key, from_list: list = None, loop: bool = False):
        if key not in self.data.keys():
            self.data[key] = 0
        if isinstance(self.data[key], int):
            Data.lock.acquire()
            self.data[key] += 1
            json.dump(self.data, open(self.file_name, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
            Data.lock.release()
            try:
                return self.data[key] - 1 if from_list is None else from_list[self.data[key] - 1]
            except IndexError as IE:
                if loop:
                    self.reset(key)
                    if len(from_list) > 0:
                        return self.get(key, from_list, loop)
                    else:
                        raise IndexError("The list is empty")
                else:
                    raise IE
        else:
            return self.data[key]

    def reset(self, key):
        self.data[key] = 0
        Data.lock.acquire()
        json.dump(self.data, open(self.file_name, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
        Data.lock.release()
