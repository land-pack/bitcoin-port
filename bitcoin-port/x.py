import math

(
def add(x, y):
    return(x + y)

def sub(x, y):
    return(x - y)


def multiply(x, y):
    return(x * y)

def divide(x, y):
    return(x / y)

def sqaure(x):
    return math.sqrt(x)


if __name__ == '__main__':
	print(add(12, 34))
	print(sub(12, 34))
	print(multiply(12, 34))
	print(divide(12, 34))
	print(sqaure(16))
