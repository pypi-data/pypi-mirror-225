"""
    1. Loguru
        install: pip install loguru
    2. Snoop
        install: pip install snoop
"""

"""
    Loguru
"""

from loguru import logger
from itertools import combinations

def division(num1: int, num2: int):
    return num1/num2

# usage
@logger.catch
def divide_numbers(num_list:list):
    for comb in combinations(num_list, 2):
        num1, num2 = comb
        res = division(num1, num2)
        print(f"{num1} / {num2} is equal to {res}")

# if __name__ == '__main__':
#     num_list = [2,1,0]
#     divide_numbers(num_list)


"""
    Snoop
"""
import snoop

@snoop
def divide_numbers(num_list:list):
    for comb in combinations(num_list, 2):
        num1, num2 = comb
        res = division(num1, num2)
        print(f"{num1} / {num2} is equal to {res}")

if __name__ == '__main__':
    num_list = [2,1,0]
    divide_numbers(num_list)