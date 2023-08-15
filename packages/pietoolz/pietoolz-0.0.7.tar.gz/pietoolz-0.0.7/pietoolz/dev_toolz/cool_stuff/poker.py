from __future__ import annotations
from typing import Any, Optional, Union
import random as r

from poker_exceptions import JokerCountException
from poker_exceptions import InvalidSuitException
from poker_exceptions import InvalidRankException

class Card:
    """
    Card class.

    Dev Representation Invariants
    -----------------------------
    - Once instantiated, a Card object CANNOT change the instance attributes
    <_suit> or <_rank>.
    - If a joker Card is instantiated, it will be randomly assigned either a
    black or a colored variant. This CANNOT be changed.
    """
    # Private Attributes
    _suit: str
    _rank: str
    _is_joker_blk: bool
    _is_joker_clr: bool
    _is_face_up: bool
    _feltpen_msg: Optional[str]

    # Class Attribute
    _id: int = 0


    # Class Constants
    RANK_STRS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                 'J', 'Q', 'K'
                ]
    SUIT_STRS = ['spade', 'spades', 's',
                'heart', 'hearts', 'h',
                'diamond', 'diamonds', 'd',
                'club', 'clubs', 'c'
                ]
    SUIT_EMOJIS = {'s': '♠',
                   'h': '♥',
                   'd': '♦',
                   'c': '♣'
                  }


    def __init__(self,
                 suit: str,
                 rank: int,
                 is_face_up=True,
                 ) -> None:
        """
        Pass in <suit='joker'> and <rank=0> to instantiate a joker Card.

        >>> c1 = Card('h', 13)
        >>> c1._suit
        '♥'
        >>> c1._rank
        'K'
        >>> c2 = Card('joker', 0)
        >>> c2.get_suit()
        'j0ker'
        >>> c2.get_rank()
        'j0ker'
        """
        if suit == 'joker' or rank == 0:
            # Init
            self._suit = self._rank = 'j0ker'
            if r.choice(['clr', 'blk']) == 'clr':
                self._is_joker_clr = True
                self._is_joker_blk = False
            else:
                self._is_joker_clr = False
                self._is_joker_blk = True

        else:
            # Error checks
            if suit.lower() not in self.SUIT_STRS:
                raise InvalidSuitException
            if rank not in range(1, 14):
                raise InvalidRankException
            # init
            self._suit = self.SUIT_EMOJIS[suit.lower()[0]]
            self._rank = self.RANK_STRS[rank-1]
            self._is_face_up = is_face_up

        self._id += 1


    def __str__(self) -> str:
        """
        Return a str representation of this Card.

        >>> c1 = Card('joker', 0)
        >>> c1.get_id()
        1
        >>> str(c1)
        'j0ker: clr'
        """
        if self._is_joker_blk:
            return 'j0ker: blk'
        elif self._is_joker_clr:
            return 'j0ker: clr'
        return f'{self._suit}{self._rank}'
    
    
    def flip(self) -> None:
        """
        Flip the card, changing its face-up status.

        Returns
        -------
            str: The new status of this Card.
        """
        self._is_face_up = not self._is_face_up
        if self._is_face_up:
            if self.is_joker_blk():
                return f'j0ker (blk)'
            if self.is_joker_clr():
                return f'j0ker (clr)'
            return f'{self._suit}{self._rank}'


    def is_face_up(self) -> bool:
        """
        Check if the card is face up.

        Returns
        -------
            bool: True if the card is face up, False otherwise.
        """
        return self._is_face_up
        

    def is_face_down(self) -> bool:
        """
        Check if the card is face down.

        Returns
        -------
            bool: True if the card is face down, False otherwise.
        """
        return not self._is_face_up


    def is_joker(self) -> bool:
        """
        Check if the card is a joker.

        Returns
        -------
            bool: True if the card is a joker, False otherwise.
        """
        return self._suit == 'j0ker'


    def is_joker_blk(self) -> bool:
        """
        Check if the card is a black joker.

        Returns
        -------
            bool: True if the card is a black joker, False otherwise.
        """
        return self._is_joker_blk


    def is_joker_clr(self) -> bool:
        """
        Check if the card is a colored joker.

        Returns
        -------
            bool: True if the card is a colored joker, False otherwise.
        """
        return self._is_joker_clr
    

    def write_feltpen_msg(self, msg: str) -> str:
        """
        Write a message on the card with a felt pen.

        Args
        ----
            msg (str): The message to write.

        Returns
        -------
            str: The written message.
        """
        self._feltpen_msg = msg
        return msg


    def get_suit(self):
        """
        Get the suit of the card.

        Returns
        -------
            str: The suit of the card.
        """
        return self._suit


    def get_rank(self):
        """
        Get the rank of the card.

        Returns
        -------
            str: The rank of the card.
        """
        return self._rank


    def get_id(self):
        """
        Get the ID of the card.

        Returns
        -------
            int: The ID of the card.
        """
        return self._id
    
    
    def get_feltpen_msg(self) -> Optional[None]:
        """
        Get the felt pen message written on the card.

Returns:
    Optional[str]: The message, if present; None otherwise.
        """
        return self._feltpen_msg
    

class Deck:
    """
    Standard 52-card deck.
    
    Optional Parameter
    ------------------
    jokers=0
        Enter integers 1 or 2, for the number of joker cards to add
        to the 52-card deck.

    Pre-Condition
    -------------
    - <jokers> must be either 0, 1, or 2. Otherwise, an exception will
      be raised.
    
    Client Code
    -----------
    >>> my_deck = Deck()
    >>> my_deck.get_joker_count()
    0
    >>> another_deck = Deck(jokers=1)
    >>> another_deck.get_joker_count()
    1
    >>> another_deck = Deck(jokers=2)
    >>> another_deck.get_joker_count()
    2
    >>> 

    Dev Representation Invariants
    -----------------------------
    - Inbetween method calls, the instance fields <_ordered_deck> and
      <_unordered_deck> must share the same number of cards remaining in the
      Deck. I.e., the two instance fields are two different representations
      of the current status of the Deck.
    """
    _joker_count: int
    _ordered_deck: list[Card]
    _unordered_deck: dict[str, list[str]]
    

    def __init__(self, jokers=0) -> None:
        """
        Create a Deck of Cards.
        """
        self._joker_count = jokers
        self._generate_decks()


    def _generate_decks(self):
        """
        Generate both the ordered AND the unordered deck representations.
        """
        pass


    def _update_decks(self):
        """
        Update both the ordered AND the unordered deck representations.
        """
        pass


    def get_joker_count(self) -> int:
        """
        Get the count of joker cards in the deck.

        Returns
        -------
            int: The number of joker cards.
        """
        return self._joker_count


class Poker():
    """
    Parent class for different variations of the poker game.
        First Betting Round: Players fold, call, or raise in turn.

    Betting Rounds:
        Pre-flop: Initial round described in "Starting."
        Flop: After three community cards are revealed.
        Turn: After fourth community card is revealed.
        River: After fifth community card is revealed.

    Community Cards:
        Flop: First three cards, face up.
        Turn: Fourth card, face up.
        River: Fifth card, face up.

    Combination:
        Use five of seven cards (two private, five community).
        Form best hand: High Card, Pair, Two Pair, etc.

    Winning:
        Best Hand: Highest-ranking hand wins pot.
        Last Player: Remaining player if others fold.
        Tie: Split pot if hands are equal.

    Hand Rankings (Highest to Lowest):
        Royal Flush
        Straight Flush
        Four of a Kind
        Full House
        Flush
        Straight
        Three of a Kind
        Two Pair
        One Pair
        High Card

    This hierarchy covers the essential rules and structure of Texas Hold'em.

    Happy Playing!
    """
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
