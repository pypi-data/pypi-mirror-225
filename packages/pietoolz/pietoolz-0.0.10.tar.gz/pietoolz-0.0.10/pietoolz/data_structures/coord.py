from __future__ import annotations
from typing import Any, Optional, Union


class Coord:
    """
    A coordinate class to represent a point in 2D space.

    Attributes
    ----------
    x : int, float
        The x-coordinate of the point.
    y : int, float
        The y-coordinate of the point.
    
    """
    _name: Optional[str]
    x: Union[int, float]
    y: Union[int, float]


    def __init__(self,
                 x: Union[int, float],
                 y: Union[int, float],
                 name: Optional[str]=None
                 ) -> None:
        """
        Initialize the coordinate object.
        
        Parameters
        ----------
        x : int, float
            The x-coordinate of the point.
        y : int, 
            The y-coordinate of the point.
        """
        self.x = x
        self.y = y
        self._name = name


    def __repr__(self) -> str:
        """
        Return a string representation of the coordinate object.
        
        Returns
        -------
        str
            The string representation of the coordinate object.

        Examples
        --------
        >>> p1 = str(Coord(1, 2))
        >>> p1
        'Coord: (1, 2)'
        >>> p2 = str(Coord(75, 300, 'test'))
        >>> p2
        'Coord: (75, 300)  <--  test'
        >>> print(p2)
        Coord: (75, 300)  <--  test
        """
        if self._name is None:
            return f'Coord: ({self.x}, {self.y})'
        return f'Coord: ({self.x}, {self.y})  <--  {self._name}'
    

    def __len__(self) -> int:
        """
        Return the number of coordinates.
        
        Returns
        -------
        int
            The number of coordinates.

        Examples
        --------
        >>> p1 = Coord(1, 2)
        >>> len(p1)
        2
        """
        return 2


    def __eq__(self, other: Coord) -> bool:
        """
        Return True if the coordinates are equal, False otherwise.
        
        Parameters
        ----------
        other : object
            The object to compare to.

        Returns
        -------
        bool
            True if the coordinates are equal, False otherwise.

        Examples
        --------
        >>> p1 = Coord(1, 2)
        >>> p2 = Coord(1, 2)
        >>> p3 = Coord(1, 3)
        >>> p1 == p2
        True
        >>> p1 == p3
        False
        """
        return (self.x == other.x) and (self.y == other.y)


    def __ne__(self, other: Coord) -> bool:
        """
        Return True if the coordinates are not equal, False otherwise.
        
        Parameters
        ----------
        other : object
            The object to compare to.

        Returns
        -------
        bool
            True if the coordinates are not equal, False otherwise.

        Examples
        --------
        >>> p1 = Coord(1, 2)
        >>> p2 = Coord(1, 2)
        >>> p3 = Coord(1, 3)
        >>> p1 != p2
        False
        >>> p1 != p3
        True
        """
        return (self.x != other.x) or (self.y != other.y)


    def __add__(self, other: Coord, name: Optional[str]=None) -> 'Coord':
        """
        Return a new Coord object with the coordinates sum.

        Parameters
        ----------
        other : Coord

        Returns
        -------
        Coord
            A new Coord object.

        Representation Invariants
        -------------------------
        - This method does NOT change <self>.

        Examples
        --------
        >>> p1 = Coord(1, 2)
        >>> p2 = Coord(3, 4)
        >>> p3 = p1 + p2
        >>> str(p3)
        'Coord: (4, 6)  <--  [None+None]'
        >>> p3
        Coord: (4, 6)  <--  [None+None]
        
        # TODO: FINISH WRITING DOCTESTS

        """
        sum_x, sum_y = self.x + other.x, self.y + other.y
        new = f'[{self._name}+{other._name}]' if name is None else name
        return Coord(sum_x, sum_y, new)
        # sum_x = self.x + other.x
        # sum_y = self.y + other.y
        # if name is None:
        #     new_name = f'[{self._name}+{other._name}]'
        #     return Coord(sum_x, sum_y, new_name)
        # return Coord(sum_x, sum_y, name)


    def __sub__(self, other: Coord, name: Optional[str]=None) -> 'Coord':
        """
        Return a new coordinate object with the coordinates subtracted.
        
        Parameters
        ----------
        other : object
            The object to subtract from.

        Returns
        -------
        Coord
            The new coordinate object.

        Examples
        --------
        >>> p1 = Coord(1, 2)
        >>> p2 = Coord(3, 4)
        >>> p3 = p2 - p1
        >>> p3
        Coord: (2, 2)  <--  [None-None]

        # TODO: FINISH WRITING DOCTESTS
        """
        new_x, new_y = self.x - other.x, self.y - other.y
        new = f'[{self._name}-{other._name}]' if name is None else name
        return Coord(new_x, new_y, new)


    def __getitem__(self, key: int) -> Union[int, float]:
        """
        Return the coordinate at the specified index.
        
        Parameters
        ----------
        key : int
            The index of the coordinate to return.

        Returns
        -------
        int, float
            The coordinate at the specified index.

        Examples
        --------
        >>> p1 = Coord(1, 2)
        >>> p1[0]
        1
        >>> p1[1]
        2
        """
        if key not in [0, 1]:
            raise IndexError('You must index 0 or 1, for x and y, respectively.')
        return self.y if key else self.x


    def __setitem__(self, key: int, value: Union[int, float]) -> None:
        """
        Set the coordinate at the specified index to the specified value.
        
        Parameters
        ----------
        key : int
            The index of the coordinate to set.
        value : int, float
            The value to set the coordinate to.

        Examples
        --------
        >>> p1 = Coord(1, 2)
        >>> p1[0] = 3
        >>> p1
        Coord: (3, 2)
        >>> p1[1] = 4
        >>> p1
        Coord: (3, 4)
        """
        if key not in [0, 1]:
            raise IndexError('You must index 0 or 1, for x and y, respectively.')
        if key:
            self.y = value
        else:
            self.x = value
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
