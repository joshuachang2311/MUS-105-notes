###############################################################################

from .bar import Bar


## A class representing a musical staff in a Part.
class Staff:
    ## Initializes a Staff and its three attributes self.id,
    # self.bars, and self.part.
    # @param staffid A unique identifier for the staff's id attribute.
    #
    # The attribute self.bars should be initialized to an empty list
    # and self.part to None.  See also: Bar, Part
    def __init__(self, staffid):
        self.id = staffid
        self.bars = []
        self.part = None

    ## Returns a string showing the staff's unique id and the
    # hex id of the instance.
    # Example: '<Staff: 1 0x109e69990>'
    def __str__(self):
        return f'<Staff: {self.id} {id(self)}>'

    ## Define __repr__ to be the same as __str__ except there is
    # no hex id included.
    # Example: '<Staff: 1>'
    def __repr__(self):
        return f'<Staff: {self.id}>'

    ## Implements Staff iteration by returning an iterator for the staff's
    # bars. See: Python's iter() function.
    def __iter__(self):
        return iter(self.bars)

    ## Appends a Bar to the staff's bar list and assigns
    # itself to the bar's staff attribute.
    # @param bar The Bar to append to the staff's bar list.
    # The method should raise a TypeError if bar is not a Bar instance.
    def add_bar(self, bar):
        if isinstance(bar, Bar):
            self.bars.append(bar)
        else:
            raise TypeError("bar is not a Bar instance")

    ## Returns a list of the staffs's bar identifiers in the same order
    # that they occur in the bars list.
    def bar_ids(self):
        return [bar.id for bar in self.bars]

    ## Returns the number of bars in the staff.
    def num_bars(self):
        return len(self.bars)