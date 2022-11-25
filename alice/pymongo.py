from pymongo import MongoClient


class MongoDB:
    def __init__(self, bd, path='mongodb://localhost:27017/'):
        self._bd = bd
        self._path = path

    def get_database(self):
        cliente = MongoClient(self._path)
        return cliente[self._bd]

    def __call__(self):
        return self.get_dataBase()
