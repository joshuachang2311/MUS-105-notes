###############################################################################

from .durational import Durational
from .pitch import Pitch


## A class that inherits from Durational to represent a musical pitch with an
# exact beat duration.
class Note (Durational):
    ## Initializes a Note and its three attributes self.pitch, self.marks,
    # and self.voice.
    # @param pitch A Pitch for the note's pitch attribute.
    # @param dur The Ratio duration of the Note. The initializer
    # should call the Durational superclass' __init__() function
    # to set the dur attribute.
    # @param marks A list Marks for the note's marks attribute.
    # Defaults to an empty list.
    #
    # The attribute self.voice should be initialized to None.
    # See also: Rest, Chord, Durational, https://en.wikipedia.org/wiki/Musical_note
    def __init__(self, pitch, dur, marks=[]):
        Durational.__init__(self, dur)
        self.pitch = pitch
        self.marks = marks
        self.voice = None

    ## Returns a string showing the note's pitch, duration
    # and the hex id of the instance.
    # Example: '<Note: F#4 1/8 0x10e242d10>'
    def __str__(self):
        return f'<Note: {self.string()} {id(self)}>'

    ## Define __repr__ to be the same as __str__ except there is
    # no hex id included.
    # Example: '<Note: F#4 1/8>'
    def __repr__(self):
        return f'<Note: {self.string()}>'

    ## Implements Note < Note.
    # @param other The note to compare with this note.
    # @returns True if this note's pitch is less than the other.
    #
    # A TypeError should be raised if other is not a Note.
    # This method can call self.pitch.__lt__() to compare.
    def __lt__(self, other):
        if isinstance(other, Note):
            return self.pitch < other.pitch
        else:
            raise TypeError("other is not an instance of Note")

    ## Implements Note <= Note.
    # @param other The note to compare with this note.
    # @returns True if this note's pitch is less than or
    # equal to the other.
    #
    # A TypeError should be raised if other is not a Note.
    # This method can call self.pitch.__le__() to compare.
    def __le__(self, other):
        if isinstance(other, Note):
            return self.pitch <= other.pitch
        else:
            raise TypeError("other is not an instance of Note")

    ## Implements Note == Note.
    # @param other The note to compare with this note.
    # @returns True if this note's pitch is equal to the other.
    #
    # A TypeError should be raised if other is not a Note.
    # This method can call self.pitch.__eq__() to compare.
    def __eq__(self, other):
        if isinstance(other, Note):
            return self.pitch == other.pitch
        else:
            raise TypeError("other is not an instance of Note")

    ## Implements Note != Note.
    # @param other The note to compare with this note.
    # @returns True if this note's pitch is not equal to the other.
    #
    # A TypeError should be raised if other is not a Note.
    # This method can call self.pitch.__ne__() to compare.
    def __ne__(self, other):
        if isinstance(other, Note):
            return self.pitch != other.pitch
        else:
            raise TypeError("other is not an instance of Note")

    ## Implements Note >= Note.
    # @param other The note to compare with this note.
    # @returns True if this note's pitch is not greater
    # than or equal to the other.
    #
    # A TypeError should be raised if other is not a Note.
    # This method can call self.pitch.__ge__() to compare.
    def __ge__(self, other):
        if isinstance(other, Note):
            return self.pitch >= other.pitch
        else:
            raise TypeError("other is not an instance of Note")

    ## Implements Note > Note.
    # @param other The note to compare with this note.
    # @returns True if this note's pitch is greater than the other.
    #
    # A TypeError should be raised if other is not a Note.
    # This method can call self.pitch.__gt__() to compare.
    def __gt__(self, other):
        if isinstance(other, Note):
            return self.pitch > other.pitch
        else:
            raise TypeError("other is not an instance of Note")

    ## Returns a string that contains the note's pitch and duration.
    # Example: 'G#4 1/4'
    def string(self):
       return f'{self.pitch.string()} {self.dur.string()}'