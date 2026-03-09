from collections import Counter
from typing import Any



def counter_data(data: int | float | Any | None):
    counter = Counter(data)
    return counter