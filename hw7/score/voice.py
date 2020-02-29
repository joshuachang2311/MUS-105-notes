###############################################################################

from .ratio import Ratio
from .durational import Durational


## A class that represents a musical Voice in a Bar. One voice holds a
# single timeline of notes; multiple voices represent parallel
# streams of notes.
class Voice:
    ## Initializes a Voice and its attributes self.id, self.notes,
    # and self.bar.
    # @param voiceid  The unique integer id for the voice's id attribute.
    #
    # The attribute self.notes should be initialized to an empty list and
    # self.bar to None.  See also: Note, Rest, Chord, Bar.
    def __init__(self, voiceid):
        self.id = voiceid
        self.notes = []
        self.bar = None

    ## Returns a string showing the voices's unique id and the
    # hex id of the instance.
    # Example: '<Voice: 2 0x109877c50>'
    def __str__(self):
        return f'<Voice: {self.id} {id(self)}>'

    ## Define __repr__ to be the same as __str__ except there is
    # no hex id included.
    # Example: '<Voice: 2>'
    def __repr__(self):
        return f'<Voice: {self.id}>'

    ## Implements Voice iteration by returning an iterator for the voices's
    # notes. See: Python's iter() function.
    def __iter__(self):
        return iter(self.notes)

    ## Appends a Note, Chord or Rest to the voice's note list and assigns
    # itself to that object's voice attribute.
    # @param note The note, chord, or rest to append to the note list.
    #
    # The method should raise a TypeError if object supplied is not a Durational.
    def add_note(self, note):
        if isinstance(note, Durational):
            self.notes.append(note)
        else:
            raise TypeError("object supplied is not an instance of Durational")

    ## Returns a beat Ratio representing the total duration of the notes
    # in the voice.
    def dur(self):
        return sum([note.dur for note in self.notes])

    ## Returns the 'part and voice' identifier of the voice, a string
    # concatenation of the part's id with the voice's id: PARTID.VOICEID
    # Example: 'P1.1'
    def get_pvid(self):
        return f'P1.{self.id}'
