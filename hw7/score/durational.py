###############################################################################

from .ratio import Ratio


## A base class whose instances have a metric duration. This implementation is
# complete -- you just need to implement the subclasses Rest, Note, and Chord.


class Durational:
    ## Constructor.
    #  @param dur A Ratio beat duration. See also: Ratio.
    def __init__(self, dur):
        if not isinstance(dur, Ratio):
            raise TypeError(f"Invalid duration: {dur}.")
        ## Holds a Ratio representing a beat duration.
        self.dur = dur

    ## Returns the durational's Ratio string.
    def string(self):
        return self.dur.string()

    ## Returns the 'part and voice' identifier for this object.
    # Should only by called on subclass instances that already 
    # have their 'voice' attribute already set.
    def get_pvid(self):
        return self.voice.bar.staff.part.id + "." + str(self.voice.id)

