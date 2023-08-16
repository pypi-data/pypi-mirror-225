import json

class pydbjson:
    def __init__(self, filename):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return {}

    def _save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    def insert_one(self, document):
        if document in self.data.values():
            print("Document already exists in the database.")
            return None
        key = str(len(self.data) + 1)
        self.data[key] = document
        self._save_data()
        return key

    def retrieve(self, key):
        return self.data.get(key)

    def delete_one(self, key):
        if key in self.data:
            del self.data[key]
            self._save_data()
        else:
            print(f"Key '{key}' not found.")

    def find_one(self, condition):
        for key, value in self.data.items():
            if all(value.get(field) == val for field, val in condition.items()):
                return key, value
        return None

    def find(self, condition):
        results = [(key, value) for key, value in self.data.items()
                   if all(value.get(field) == val for field, val in condition.items())]
        return results
    
    def update_one(self, key, update_fields):
        if key in self.data:
            document = self.data[key]
            document.update(update_fields)
            self._save_data()
        else:
            print(f"Key '{key}' not found.")