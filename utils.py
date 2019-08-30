from datetime import datetime


class Timed:
    def __init__(self, label=''):
        self.label = label
        self.start = None
        self.end = None

    def __enter__(self):
        print(f'[Timing{" " + self.label if self.label else ""}]')
        self.start = datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = datetime.now()
        print(f'[Done timing{" " + self.label if self.label else ""}: {self.end - self.start}]')
