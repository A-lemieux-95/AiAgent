import sys
from calculator import Calculator

if __name__ == "__main__":
    expression = sys.argv[1]
    calculator = Calculator()
    result = calculator.evaluate(expression)
    print(result)
