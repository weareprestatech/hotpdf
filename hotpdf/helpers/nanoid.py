"""Implementation from: https://github.com/puyuan/py-nanoid."""

from math import ceil, log
from os import urandom
from typing import Callable


def algorithm_generate(random_bytes: int) -> bytearray:
    """Algorithm to generate random bytes.

    Args:
        random_bytes (int):

    Returns:
        bytearray:
    """
    return bytearray(urandom(random_bytes))


def method(algorithm: Callable[[int], bytearray], alphabet: str, size: int) -> str:
    alphabet_len = len(alphabet)

    mask = 1
    if alphabet_len > 1:
        mask = (2 << int(log(alphabet_len - 1) / log(2))) - 1
    step = ceil(1.6 * mask * size / alphabet_len)

    id = ""
    while True:
        random_bytes = algorithm(step)

        for i in range(step):
            random_byte = random_bytes[i] & mask
            if random_byte < alphabet_len and alphabet[random_byte]:
                id += alphabet[random_byte]

                if len(id) == size:
                    return id


def generate_nano_id(
    alphabet: str = "_-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    size: int = 21,
) -> str:
    return method(algorithm_generate, alphabet, size)
