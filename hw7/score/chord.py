###############################################################################

from .durational import Durational
from .note import Note


## A class that represents a simultaneous set of notes with the same
# duration.
class Chord(Durational):
    ## Initializes a Chord and its two attributes self.notes, and self.voice.
    # @param notes A list of notes for the chord's notes attribute.
    #
    # The initializer should call the Durational superclass' __init__() function
    # and pass it the first note's duration.  The attribute self.voice should
    # be initialized to an empty list.
    #
    # The method should raise a TypeError if all notes do not contain the same
    # duration.
    #
    # See also: Rest, Note, https://en.wikipedia.org/wiki/Chord_(music)

    def __init__(self, notes):
        dur = notes[0].dur
        for note in notes:
            if note.dur != dur:
                raise TypeError("all notes do not contain the same duration")

        Durational.__init__(self, dur)
        self.notes = notes
        self.voice = []

    ## Returns a string showing the chords's pitches, duration,
    # and the hex id of the instance. See: string()
    # Example: '<Chord: (Eb3, Ab3, C4, Eb4) 1/4 0x10e2d5950>'
    def __str__(self):
        return f'<Chord: {self.string()} {id(self)}>'

    ## Define __repr__ to be the same as __str__ except there is
    # no hex id included.
    # Example: '<Chord: (Eb3, Ab3, C4, Eb4) 1/4>'
    def __repr__(self):
        return f'<Chord: {self.string()}>'

    # Returns a string displaying the chords's pitches and duration.
    # The pitches are parenthesized and separated by commas.
    # Example: '(Eb3, Ab3, C4, Eb4) 1/2'
    def string(self):
        to_return = '('
        for note in self.notes:
            to_return += note.pitch.string() + ', '
        if len(self.notes) > 0:
            to_return = to_return[0 : len(to_return) - 2]
        to_return += f') {self.dur.string()}'

        return to_return