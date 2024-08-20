import random


def check_event_probability(p1, p2=None) -> bool:
    """
    function takes random probability from [p1, p2] and uses it to check event probability
    *p2>p1
    :param p1: first probability
    :param p2: second probability
    :return:
    """
    if p2 is None:
        p2 = p1
    event_probability = random.randint(p1, p2)
    if random.randint(1, 100) <= event_probability:
        return 1
    return 0
