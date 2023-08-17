"""
Custom Exceptions classes made for the poker module.
"""


class InvalidSuitException(Exception):
    def __init__(self):
        super().__init__("<suit> must be 's', 'h', 'd', or 'c'.")


class InvalidRankException(Exception):
    def __init__(self):
        super().__init__("<rank> must be an integer member of [1, 13].")


class JokerCountException(Exception):
    def __init__(self):
        super().__init__("The maximum number of Joker cards is two.")


if __name__ == '__main__':
    import doctest
    doctest.testmod()
