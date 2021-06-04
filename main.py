from pipeline import Pipeline
from math import pow

DEBUG = True

class TestPipe(Pipeline):
    def __init__(self, source):
        super().__init__(source)

    def map(self, data):
        if DEBUG:
            print("Source: " + str(self.source) + " | Data: " + str(data))

        return (data + self.source) ** self.source


if __name__ == '__main__':
    p1 = TestPipe(1)
    p2 = TestPipe(2)
    p3 = TestPipe(3)
    pl1 = p1 >> p2 >> p3

    p1 = TestPipe(1)
    p2 = TestPipe(2)
    p3 = TestPipe(3)
    pl2 = p1 >> p3 >> p2

    print('--')
    test_val = 2

    res1 = pl1.map(test_val)
    res2 = pl2.map(test_val)

    print("To show that commutativity is not preserved:")
    print(f"pl1 = p1 >> p2 >> p3; pl1({test_val}) = {res1}")
    print(f"pl2 = p1 >> p3 >> p2; pl2({test_val}) = {res2}")
