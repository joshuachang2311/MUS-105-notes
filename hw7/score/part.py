###############################################################################

from .staff import Staff


## A class representing a musical part in a Score.
class Part:
    ## Initializes a Part and its five attributes self.id, self.name,
    # self.shortname, self.staffs, and self.score.
    # @param partid A unique identifier for the parts's id attribute.
    # @param name A string name for the part's name attribute. Defaults
    # to None.
    # @param shortname A short name for the part's shortname attribute.
    # Defaults to None.
    #
    # The attribute self.staffs should be initialized to an empty list
    # and self.score to None. See also: Staff, Score.
    def __init__(self, partid, name=None, shortname=None):
        self.id = partid
        self.name = name
        self.shortname = shortname
        self.staffs = []
        self.score = None

    ## Returns a string showing the parts's unique id and the
    # hex id of the instance.
    # Example: '<Part: P1 0x10963ff90>'
    def __str__(self):
        return f'<Part: {self.id} {id(self)}>'

    ## Define __repr__ to be the same as __str__ except there is
    # no hex id included.
    # Example: '<Part: P1>'
    def __repr__(self):
        return f'<Part: {self.id}>'


    ## Implements Part iteration by returning an iterator for the parts's
    # staffs. See: Python's iter() function.
    def __iter__(self):
        return iter(self.staffs)

    ## Appends a Staff to the part's staff list and assigns
    # itself to the staff's part attribute.
    # @param staff The staff to append to the parts's staff list.
    # The method should raise a TypeError if part is not a Part instance.
    def add_staff(self, staff):
        if isinstance(staff, Staff):
            self.staffs.append(staff)
        else:
            raise TypeError("part is not a Part instance")

    ## Returns the part's staff identifiers.
    def staff_ids(self):
        return [staff.id for staff in self.staffs]

    ## Returns the number of staffs in the part.
    def num_staffs(self):
        return len(self.staffs)