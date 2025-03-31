
class Result:
    index: int
    expected: int
    predicted: int

    def __init__(self, index: int, expected: int, predicted: int):
        self.index = index
        self.expected = expected
        self.predicted = predicted