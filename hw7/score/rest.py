###############################################################################

from .durational import Durational


## A class that inherits from Durational to represent musical silence for
# an exact beat duration.
class Rest (Durational):

    ## Initializes a Rest and its two attributes self.dur and self.voice.
    # @param dur The Ratio duration of the Rest. The initializer
    # should call the Durational superclass' __init__() function
    # to set the dur attribute.
    # The self.voice attribute should be initialized to None.
    # See also: Note, Chord, Durational.
    def __init__(self, dur):
        Durational.__init__(self, dur)
        self.voice = None

    ## Returns the print representation of the rest. Information includes
    #  the class name, the ratio duration and the hex id of the instance.
    #
    #  Example:
    #  <Rest: 1/4 0x10999e390>
    def __str__(self):
        return f'<Rest: {self.dur.string()} {id(self)}>'

    ## Define __repr__ to be the same as __str__ except there is
    # no hex id included.
    # Example: '<Rest: 1/4>'
    def __repr__(self):
        return f'<Rest: {self.dur.string()}>'

    ## Returns a string containing an R and the ratio duration.
    # Examples: 'R 1/4', 'R 3/8'
    def string(self):
        return f'R {self.dur.string()}'

    ## Creates a Rest with an added 'pad' attribute set to true. A Pad is
    # durational placeholder for an mxml voice whose first note starts
    # later than beat 0 in the measure. The pad attribute allows these
    # placeholders to be distinguished from explicitly notated rests.
    @classmethod
    def pad(cls, dur):
        rest = Rest(dur)
        rest.pad = True

        return rest

    ## Returns true if the Rest is marked as a pad. See: pad(), and Python's
    # builtin function getattr().
    def is_pad(self):
        return getattr(self, 'pad', False)



