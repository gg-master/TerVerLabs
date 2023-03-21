from math import factorial
from functools import reduce


def permutation_with_rep(*k) -> int:
    kp = reduce(lambda x, y: x * y, map(factorial, k))
    return factorial(sum(k)) // kp


def permutation_without_rep(n: int) -> int:
    return factorial(n)


def placement_with_rep(k: int, n: int) -> int:
    return int(n ** k)


def placement_without_rep(k: int, n: int) -> int:
    assert k <= n, "Number n must be greater than k"
    return factorial(n) // factorial(n - k)


def combinations_without_rep(k: int, n: int) -> int:
    assert k <= n, "Number n must be greater than k"
    return factorial(n) // (factorial(n - k) * factorial(k))


def combinations_with_rep(k: int, n: int) -> int:
    return combinations_without_rep(k, n + k - 1)
