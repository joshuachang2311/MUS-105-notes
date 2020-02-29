###############################################################################

from .ratio import Ratio


## A class representing the standard musical meters.
# See: https://en.wikipedia.org/wiki/Metre_(music)
class Meter:
    ## Constructor.
    # @param num  The numerator, an integer between 1 and 16 inclusive.
    # @param den  The denominator, a power of 2 between 1 and 32 inclusive.
    # @returns A meter instance with attributes num and den.
    #
    # The constructor should raise a TypeError if num or den are not
    # integers and a ValueError if their values are invalid.
    def __init__(self, num, den):
        if not isinstance(num, int):
            raise TypeError("num is not integer")
        elif num < 1 or num > 16:
            raise ValueError("num's value is invalid")
        else:
            self.num = num

        legal_dens = [2 ** i for i in range(6)]
        if not isinstance(den, int):
            raise TypeError("den is not integer")
        elif den not in legal_dens:
            raise ValueError("den's value is invalid")
        else:
            self.den = den

    ## Returns the print representation of the meter. The string should
    # include the class name, the num and den, and instance id.
    #
    # Examples:
    # <Meter: 2/4 0x1051a1690>
    # <Meter: 7/16 0x1051a1bd0>
    # <Meter: 3/1 0x1053ee910>
    def __str__(self):
        return f'<Meter: {self.string()} {hex(id(self))}>'

    ## Returns the external representation of the meter. The string
    # should include the class name, num and den.
    #
    # Examples:
    # Meter(2, 4)
    # Meter(7, 16)
    # Meter(3, 1)
    def __repr__(self):
        return f'Meter({self.num}, {self.den})'

    ## Returns the string name of the meter, e.g. '6/8'
    def string(self):
        return f'{self.num}/{self.den}'

    ## Returns true if the meter is compound (numerator 6, 9, 12, or 15).
    def is_compound(self):
        return self.num in [i * 3 for i in range(2, 6)]

    ## Returns true if the meter is simple (numerator 1, 2, 3, or 4).
    def is_simple(self):
        return self.num in [i for i in range(1, 5)]

    ## Returns true if the meter is complex (numerator 5, 7, 8, 10, 13, or 14).
    def is_complex(self):
        return self.num in [5, 7, 8, 10, 11, 13, 14]

    ## Returns true if the meter is duple (numerator 2 or 6).
    def is_duple(self):
        return self.num in [2, 6]

    ## Returns true if the meter is triple (numerator 3 or 9).
    def is_triple(self):
        return self.num in [3, 9]

    ## Returns true if the meter is quadruple (numerator 4 or 12).
    def is_quadruple(self):
        return self.num in [4, 12]

    ## Returns true if the meter is quintuple (numerator 5 or 15).
    def is_quintuple(self):
        return self.num in [5, 15]

    ## Returns true if the meter is a septuple (numerator 7).
    def is_septuple(self):
        return self.num == 7

    ## Returns a Ratio representing the meter's beat. For example,
    # 4/4 returns a beat of 1/4, 6/8 meter returns the beat 3/8,
    # and 3/2 returns a beat of 1/2. The method should raise
    # a NotImplementedError If the meter is not simple or compound.
    # See: Ratio.
    def beat(self):
        if self.is_simple():
            return Ratio(1, self.den)
        elif self.is_compound():
            return Ratio(3, self.den)
        else:
            raise NotImplementedError("meter is not simple or compound")

    ## Returns a Ratio representing the meter's total measure duration, in beats.
    # For example, 4/4 returns a duration ratio of 1/1, 6/8 meter returns 3/4,
    # and 3/2 returns a duration of 3/2. See: Ratio.
    def measure_dur(self):
        return Ratio(self.num, self.den)
