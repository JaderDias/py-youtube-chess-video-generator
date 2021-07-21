class MockScript:
    def __init__(self, shots):
        self.shots = shots
        self.index = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.index >= len(self.shots):
            raise StopIteration
        shot = self.shots[self.index]
        self.index += 1
        return shot
    
