from CheeseType import NonNegativeFloat, PositiveInt

class ProgressBar:
    def __init__(self, length: PositiveInt, template: str = '%b%l%r%b %p', *, boundaryStr: str = '|', leftStr: str = '█', rightStr: str = '-'):
        self.length: PositiveInt = PositiveInt(length)
        self.template: str = template
        self.boundaryStr: str = boundaryStr
        self.leftStr: str = leftStr
        self.rightStr: str = rightStr

    def __call__(self, value: NonNegativeFloat):
        left = round(value * self.length)
        right = self.length - left
        s = self.template.replace('%b', self.boundaryStr).replace('%l', self.leftStr * left).replace('%r', self.rightStr * right).replace('%p', '{:.2f}%'.format(value * 100))

        return s
