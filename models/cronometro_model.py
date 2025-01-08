from datetime import datetime

class Cronometro:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed_time = 0

    def start(self):
        self.start_time = datetime.now()

    def stop(self):
        if self.start_time:
            self.end_time = datetime.now()
            self.elapsed_time = (self.end_time - self.start_time).total_seconds()

    def reset(self):
        self.start_time = None
        self.end_time = None
        self.elapsed_time = 0

    def get_elapsed_time(self):
        return self.elapsed_time
