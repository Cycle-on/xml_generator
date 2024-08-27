import random


def get_random_name(gender: str) -> str:
    if gender == 'F':
        with open('female.txt') as f:
            return random.choice(f.readlines())[:-1].split()

    with open("male.txt") as f:
        return random.choice(f.readlines())[:-1].split()
