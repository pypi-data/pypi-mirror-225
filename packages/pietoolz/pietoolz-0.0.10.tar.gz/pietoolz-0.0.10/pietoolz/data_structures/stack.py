"""
How to Implement Code:
----------------------
1. Program a working logic. This makes the code shippable immediately after.
2. Refactor/optimize if necessary.
"""
from __future__ import annotations
from typing import Any, Optional, Union
import secrets


class Stack:
    """
    The classic Stack object experience, equipped w/ the usual stack type
    methods. You can store any combination of data types within the same
    instance of Stack.

    How to Initialize in 3 Different Ways
    =====================================

    Create an empty Stack:
    ----------------------
    >>> s1 = Stack()
    >>> s1
    []
    >>> s1.push(7)
    >>> s1.push('nine')
    >>> s1
    [7, 'nine']
    >>> s1.pop()
    'nine'

    Create a Pre-made Stack (Multiple Items):
    -----------------------------------------
    >>> temp_list = [2, 3, 4, 9]
    >>> s2 = Stack(temp_list)
    >>> s2
    [2, 3, 4, 9]

    Create a Stack w/ a bottom item:
    --------------------------------
    >>> s3 = Stack('a str item')
    >>> s3
    ['a str item']

    Extra Features
    --------------
    1. Shuffle Stack
        >>> stk = Stack([1, 2, 3])
        >>> stk
        [1, 2, 3]
        >>> # The line of code below randomly shuffles the stacking order.
        >>> stk.shuffle()
        >>> # Now, there's only a "33.3% possibility" that s1.pop() will return 3.
    
    Representation Invariants
    -------------------------
    - The number of elements in the Stack cannot be a negative integer.
    I.e., Stack(arg_list).size() will never return a negative integer.

    """
    # Dev. Representation Invariants
    # ------------------------------
    # - Between calls to all public instance methods,
    #   self._size and len(self._stack) must be the SAME.
    #
    _stack: list[Any]
    _size: int


    def __init__(self, item: Any=None) -> None:
        """
        Initialize Stack. Refer to class docstring for details.
        """
        # Initialize an empty Stack
        self._stack = []
        self._size = 0
        # If an <item> is passed
        if item is not None:
            # <item>: list
            if isinstance(item, list):
                self._stack += item
                self._size += len(item)
            # <item>: tuple
            elif isinstance(item, tuple):
                for i in item:
                    self._stack.append(i)
                self._size += len(item)
            # <item>: anything other than Python list or tuple
            else:
                self._stack.append(item)
                self._size += 1

    
    def __str__(self) -> str:
        """
        Client Code:
        ------------
        >>> s1 = Stack([1, 2, 'three', 4.0, 5, 6, 7])
        >>> print(s1)
        [1, 2, 'three', 4.0, 5, 6, 7]
        >>> str(s1)
        "[1, 2, 'three', 4.0, 5, 6, 7]"
        """
        return str(self._stack)


    def __repr__(self) -> str:
        """
        Client Code:
        ------------
        >>> s1 = Stack([1, 2, 'three', 4.0, 5, 6, 7])
        >>> s1
        [1, 2, 'three', 4.0, 5, 6, 7]
        """
        return self.__str__()


    def push(self, item: Any) -> None:
        """
        Push <item> to the top of the Stack.

        Client Code:
        ------------
        >>> stk = Stack()
        >>> stk.push(1)
        >>> stk.push(2)
        >>> stk.push(3)
        >>> stk.push('four')
        >>> stk
        [1, 2, 3, 'four']
        >>> stk.size()
        4
        >>> stk.is_empty()
        False
        """
        self._stack.append(item)
        self._size += 1
    

    def pop(self) -> Optional[None]:
        """
        Info.
        -----
        Remove an item from the top of this Stack.

        Return
        ------
        None, if this Stack is already empty. Otherwise, return the
        popped item.

        Client Code:
        ------------
        >>> stk = Stack([1, 2, 3, 'four'])
        >>> stk
        [1, 2, 3, 'four']
        >>> stk.pop()
        'four'
        >>> stk
        [1, 2, 3]
        >>> stk.pop()
        3
        >>> stk.pop()
        2
        >>> stk
        [1]
        >>> stk.pop()
        1
        >>> stk
        []
        >>> stk.pop()
        >>> stk
        []
        >>> stk.is_empty()
        True
        """
        if len(self._stack) == 0:
            return None
        else:
            self._size -= 1
            return self._stack.pop()


    def is_empty(self) -> bool:
        """
        Return True if Stack is empty. Else, return False.
        """
        return len(self._stack) == 0
    

    def size(self) -> int:
        """
        Return how many items are in this Stack.

        Client Code
        -----------
        >>> s1 = Stack()
        >>> s1.is_empty()
        True
        >>> s1.size()
        0
        >>> s1.push(10)
        >>> s1.size()
        1
        >>> s1.push(20)
        >>> s1.push(30)
        >>> s1.size()
        3
        >>> _= s1.pop()
        >>> s1.size()
        2
        >>> _= s1.pop()
        >>> _= s1.pop()
        >>> s1.size()
        0
        >>> s1.is_empty()
        True
        """
        return self._size
    

    def dump_into(self, other: Stack) -> None:
        """
        Starting from the top of this Stack, transfer all current items into
        the <other> Stack, one-by-one, until this Stack is empty.

        I.e., the previously-top item of this Stack is now the currently-bottom
        item of the new <other> Stack that this method returns. This means that
        you will NOT lose the aliases, outside of the scope of this method, 
        that point to the Stack that you have passed.

        This method only mutates the argument Stack, and does NOT generate any
        new Stack instances.

        Note
        ----
        After exiting method, this Stack instance is NOT destroyed, but rather
        left as an empty Stack, ready to be re-used.

        It is up to you to decide whether or not you'd like to keep this
        now-empty Stack instance around for further use in your program, or
        abandon it for the garbage collector.

        Client Code
        -----------
        >>> s1 = Stack()
        >>> s1.push(1)
        >>> s1.push(2)
        >>> s1.push(3)
        >>> print(s1)
        [1, 2, 3]
        >>> s1.size()
        3
        >>> s2 = Stack()
        >>> s1.dump_into(s2)
        >>> print(s2)
        [3, 2, 1]
        >>> print(s1)
        []
        >>> s1.is_empty()
        True
        """
        for _ in range(len(self._stack)):
            other.push(self.pop())


    def shuffle(self) -> None:
        """
        Randomly shuffle the order of this Stack.

        >>> s = Stack([1, 2, 3, 4, 5])
        >>> s.shuffle()
        >>> # Now, s is shuffled (i.e., items are re-ordered)
        """
        secrets.SystemRandom().shuffle(self._stack)

    
    def __size_is_len_stack(self) -> bool:
        """
        DEBUG tool
        ----------
        Does this Stack have matching len(self._stack) and self._size?

        Return
        ------
        If so, return True. Otherwise, return False.
        """
        if len(self._stack) == self._size:
            return True
        else:
            print("that boi ain't right")
            return False


if __name__ == "__main__":
    import doctest
    doctest.testmod()
