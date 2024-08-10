import random


def check_event_probability(p1, p2) -> bool:
    event_probability = random.randint(p1, p2)
    if random.randint(0, 100) < event_probability:
        return 1
    return 0
