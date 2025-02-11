# utils/error_dictionary.py
class ErrorDictionary:
    def __init__(self):
        self.errors = []

    def add_error(self, error):
        print(f"🛑 {error}")
        self.errors.append(error)

    def has_errors(self):
        return len(self.errors) > 0

    def get_all_errors(self):
        return self.errors

    def clear_errors(self):
        self.errors.clear()
