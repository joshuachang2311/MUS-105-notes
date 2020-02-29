###############################################################################

from .pitch import Pitch

## A class that implements musical intervals.
#
#  An Interval measures the distance between two Pitches. Interval distance
#  can be measured in different ways, for example using lines-and-spaces,
#  semitones, ratios, or cents. In western music theory an interval distance is
#  measured using 'span' (number of lines and spaces) and 'quality' (a chromatic
#  adjustment to the size). The Interval class supports the standard interval
#  names and classification system, including the notion of descending or
#  ascending intervals and simple or compound intervals.
#  Intervals can be numerically compared for their size (span+quality) and
#  can be used to transpose Pitches.
#
#  An Interval contains four integer attributes:
#  * span  The number of lines and spaces the interval moves (0-7).
#  * qual  The quality of the interval (0-12).
#  * xoct  The 'extra octaves' spanned by compound intervals (0-10).
#  * sign  1 for ascending intervals, -1 for descending.
#
#  See also: https://en.wikipedia.org/wiki/Interval_(music)


class Interval:

    ## Creates an Interval from a string, list, or two Pitches.
    #  * Interval(string) - creates an Interval from a pitch string.
    #  * Interval([s, q, x, s]) - creates a Pitch from a list of four
    #  integers: a span, quality, extra octaves and sign. (see below).
    #  * Interval(pitch1, pitch2) - creates an Interval from two Pitches.
    #
    #  @param arg If only arg is specified it should be either an
    #  interval string or a list of four interval indexes.  If both
    #  arg and other are provided, both should be a Pitch.
    #  @param other A Pitch if arg is a Pitch, otherwise None.
    #
    # The format of a Interval string is:
    #  @code
    #  interval  = ["-"] , <quality> , <span>
    #  <quality> = <diminished> | <minor> | <perfect> | <major> | <augmented>
    #  <diminished> = <5d> , <4d> , <3d> , <2d> , <1d> ;
    #  <5d> = "ooooo" | "ddddd"
    #  <4d> = "oooo" | "dddd"
    #  <3d> = "ooo" | "ddd"
    #  <2d> = "oo" | "dd"
    #  <1d> = "o" | "d"
    #  <minor> = "m"
    #  <perfect> = "P"
    #  <major> = "M"
    #  <augmented> = <5a>, <4a>, <3a>, <2a>, <1a>
    #  <5d> = "+++++" | "aaaaa"
    #  <4d> = "++++" | "aaaa"
    #  <3d> = "+++" | "aaa"
    #  <2d> = "++" | "aa"
    #  <1d> = "+" | "a"
    #  <span> = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ...
    # @endcode
    #
    # The __init__function should check to make sure the arguments are either a string, a
    # list of four integers, or two pitches.  If the input is a string then __init__ should
    # pass the string to the the private _init_from_string() method (see below).  If the
    # input is a list of four ints, __init__ will pass them to the private _init_from_list()
    # method (see below). If the input is two pitches they will be passed to the private
    # _init_from_pitches() method (see below).  Otherwise (if the input is not
    # a string, list of four integers, or two pitches) the method will raise a TypeError
    # for the offending value.
    span_names = ['unison', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'octave']
    numerical_adverbs = ['', 'doubly-', 'triply-', 'quadruply-', 'quintuply-']
    
    diminishes = ['o' * i for i in range(5, 0, -1)]
    diminished_letters = ['d' * i for i in range(5, 0, -1)] + ['D' * i for i in range(5, 0, -1)]
    diminished_letter_to_symbol = {diminished_letter: diminish for diminished_letter, diminish in zip(diminished_letters, diminishes + diminishes)}
    
    augments = ['+' * i for i in range(1, 6)]
    augmented_letters = ['a' * i for i in range(1, 6)] + ['A' * i for i in range(1, 6)]
    augmented_letter_to_symbol = {augmented_letter: augment for augmented_letter, augment in zip(augmented_letters, augments + augments)}
    
    quality_letter_to_symbol = diminished_letter_to_symbol
    quality_letter_to_symbol.update(augmented_letter_to_symbol)
    qualities = diminishes + ['m', 'P', 'M'] + augments
    
    perfect_spans = [0, 3, 4, 7]
    imperfect_spans = [1, 2, 5, 6]
    
    perfect_qualities = diminishes + ['P'] + augments
    imperfect_qualities = diminishes + ['m', 'M'] + augments
    
    perfect_index = 5
    imperfect_index = 6
    
    span_to_keynum = [0, 2, 4, 5, 7, 9, 11, 12]
    
    def __init__(self, arg, other=None):
        if isinstance(arg, str):
            if other != None:
                raise TypeError("Expected 1 string argument")
            else:
                self._init_from_string(arg)
        elif isinstance(arg, list):
            if other != None:
                raise TypeError("Expected a 4-element list")
            elif (len(arg) != 4):
                raise TypeError("Expected a 4-element list")
            else:
                self._init_from_list(arg)
        elif isinstance(arg, Pitch):
            if not isinstance(other, Pitch):
                raise TypeError("Expected two Pitch instances")
            else:
                self._init_from_pitches(arg, other)

    ## A private method that checks four integer values (span, qual, xoct, sign) to make sure
    # they are valid index values for the span, qual, xoct and sign attributes. Legal values
    # are: span 0-7, qual 0-12, xoct 0-10, sign -1 or 1. If any value is out of range the
    # method will raise a ValueError for that value. If all values are legal the method will
    # make the following 'edge case' tests:
    # * span and quality values cannot produce negative semitones, i.e. an interval
    #   whose 'top' would be lower that its 'bottom'. Here are the smallest VALID 
    #   interval for each span that could cause this: perfect unison, diminished-second,
    #   triply-diminished third.
    # * Only the span of a fifth can be quintuply diminished.
    # * Only the span of a fourth can be quintuply augmented.
    # * No interval can surpass 127 semitones, LOL. The last legal intervals are: 'P75'
    #  (a 10 octave perfect 5th), and a 'o76' (a 10 octave diminished 6th) 
    # * If a user specifies an octave as a unison span with 1 extra octave, e.g. [0,*,1,*],
    # it should be converted to an octave span with 0 extra octaves, e.g. [7,*,0,*]
    #
    # Only if all the edge case checks pass then _init_from_list() should assign
    # the four values to the attributes, e.g. self.span=span, self.qual=qual, and
    # so on. Otherwise if any edge case fails the method should raise a ValueError.
    def _init_from_list(self, arg):
        span, qual, xoct, sign = tuple(arg)
    
        if not isinstance(span, int):
            raise TypeError("Expected span to be an int between 0-7")
        elif span < 0 or span > 7:
            raise ValueError("Expected span to be an int between 0-7")
        if not isinstance(qual, int):
            raise TypeError("Expected qual to be an int between 0-12")
        elif qual < 0 or qual > 12:
            raise ValueError("Expected qual to be an int between 0-12")
        if not isinstance(xoct, int):
            raise TypeError("Expected xoct to be an int between 0-10")
        elif xoct < 0 or xoct > 10:
            raise ValueError("Expected xoct to be an int between 0-10")
        if not isinstance(sign, int):
            raise TypeError("Expected sign to be either 1 or -1")
        elif sign != -1 and sign != 1:
            raise ValueError("Expected sign to be either 1 or -1")

        self.span = span
        self.qual = qual
        self.xoct = xoct
        self.sign = sign

        if self.sign * self.semitones() < 0:
            raise ValueError("Higher note has lower pitch")
        elif abs(self.semitones()) < 0 or abs(self.semitones()) > 127:
            raise ValueError("Semitones of Interval instance not in range 0-127")
        elif Interval.span_names[self.span] != 'fifth' and Interval.qualities[self.qual] == 'ooooo':
            raise ValueError("Only the span of a fifth can be quintuply diminished")
        elif Interval.span_names[self.span] != 'fourth' and Interval.qualities[self.qual] == '+++++':
            raise ValueError("Only the span of a fourth can be quintuply augmented")

        if self.span == 0 and self.xoct > 0:
            self.span = 7
            self.xoct -= 1

    ## A private method that accepts an interval string and parses it into four
    # integer values: span, qual, xoct, sign. If all four values can be parsed
    # from the string they should be passed to the _init_from_list() method to
    # check the values and assign them to the instance's attributes. A ValueError
    # should be raised for any value that cannot be parsed from the string. See:
    # _init_from_list().
    def _init_from_string(self, string):
        if not isinstance(string, str):
            raise TypeError("Expected string")

        index = 0
        length = len(string)
        span, qual, xoct, sign = (-1, -1, -1, 0)

        if string[0] == '-':
            sign = -1
            index += 1
        else:
            sign = 1

        for i in range(5, 0, -1):
            qual_string = string[index:min(index + i, length)]
            qual_string = Interval.quality_letter_to_symbol.get(qual_string, qual_string)

            if qual_string in Interval.qualities:
                qual = Interval.qualities.index(qual_string)
                index += i
                break
        if qual == -1:
            raise ValueError("Missing qual")

        span = int(string[index:]) - 1
        if span % 7 == 0:
            if span == 0:
                xoct = 0
            else:
                xoct = span // 7 - 1
                span = 7
        else:
            xoct = span // 7
            span = span % 7

        self._init_from_list([span, qual, xoct, sign])

    ## A private method that determines approprite span, qual, xoct, sign
    # from two pitches. If pitch2 is lower than pitch1 then a descending
    # interval should be formed. The values should be passed to the
    # _init_from_list() method to initalize the interval's attributes.
    # See: _init_from_list().
    #
    # Do NOT implement this method yet.
    def _init_from_pitches(self, pitch1, pitch2):
        if not isinstance(pitch1, Pitch) or not isinstance(pitch2, Pitch):
            raise TypeError("Expected two Pitch objects")

        span, qual, xoct, sign = (-1, -1, 0, 0)

        if pitch1 > pitch2:
            if pitch1.keynum() < pitch2.keynum():
                raise ValueError("High note has lower pitch")

            value2, value1 = pitch1.pos(), pitch2.pos()
            sign = -1
        else:
            if pitch1.keynum() > pitch2.keynum():
                raise ValueError("High note has lower pitch")

            value1, value2 = pitch1.pos(), pitch2.pos()
            sign = 1
        accidental1, accidental2 = value1 - (value1 >> 4 << 4), value2 - (value2 >> 4 << 4)
        value1, value2 = value1 >> 4, value2 >> 4
        letter1, letter2 = value1 - (value1 >> 4 << 4), value2 - (value2 >> 4 << 4)
        value1, value2 = value1 >> 4, value2 >> 4
        octave1, octave2 = value1, value2

        span = (octave2 - octave1) * 7 + (letter2 - letter1)

        if span % 7 == 0:
            if span <= 7:
                new_span = span
                xoct = 0
            else:
                new_span = 7
                xoct = span // 7 - 1
        else:
            xoct = span // 7
            new_span = span % 7

        perfect = span % 7 in Interval.perfect_spans
        if perfect:
            index = Interval.perfect_index
        else:
            index = Interval.imperfect_index

        qual = abs(pitch2.keynum() - pitch1.keynum()) - Interval.span_to_keynum[new_span] - xoct * 12 + index

        if perfect:
            qual = Interval.qualities.index(Interval.perfect_qualities[qual])
        else:
            qual = Interval.qualities.index(Interval.imperfect_qualities[qual])

        self.__init__([new_span, qual, xoct, sign])
        
    ## Returns a string displaying information about the
    #  Interval within angle brackets. Information includes the
    #  the class name, the interval text, the span, qual, xoct and sign
    #  values, and the id of the object. Example:
    #  <Interval: oooo8 [7, 1, 0, 1] 0x1075bf6d0>
    #  See also: string().
    def __str__(self):
        return f'<Interval: {self.string()} [{self.span}, {self.qual}, {self.xoct}, {self.sign}] {hex(id(self))}>'

    ## The string the console prints shows the external form.
    # Example: Interval("oooo8")
    def __repr__(self):
        return f'Interval("{self.string()}")'

    ## Implements Interval < Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is less than the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __lt__(self, other):
        if not isinstance(other, Interval):
            raise TypeError("Other is not an instance of Interval")

        return self.pos() < other.pos()

    ## Implements Interval <= Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is less than or equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __le__(self, other):
        if not isinstance(other, Interval):
            raise TypeError("Other is not an instance of Interval")

        return self.pos() <= other.pos()

    ## Implements Interval == Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __eq__(self, other):
        if not isinstance(other, Interval):
            raise TypeError("Other is not an instance of Interval")

        return self.pos() == other.pos()

    ## Implements Interval != Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is not equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ne__(self, other):
        if not isinstance(other, Interval):
            raise TypeError("Other is not an instance of Interval")

        return self.pos() != other.pos()

    ## Implements Interval >= Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is greater than or equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ge__(self, other):
        if not isinstance(other, Interval):
            raise TypeError("Other is not an instance of Interval")

        return self.pos() >= other.pos()

    ## Implements Interval > Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is greater than the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __gt__(self, other):
        if not isinstance(other, Interval):
            raise TypeError("Other is not an instance of Interval")

        return self.pos() > other.pos()

    ## Returns a numerical value for comparing the size of this interval to
    # another. The comparison depends on the span, extra octaves, and quality
    # of the intervals but not their signs. For two intervals, if the span of
    # the first (including extra octaves) is larger than the second then the
    # first interval is larger than the second regardless of the quality of
    # either interval. If the interval spans are the same then the first is
    # larger than the second if its quality is larger. This value can be
    # encoded as a 16 bit integer: (((span + (xoct * 7)) + 1) << 8) + qual  
    def pos(self):
        return (((self.span + (self.xoct * 7)) + 1) << 8) + self.qual

    ## Returns a string containing the interval name.
    #  For example, Interval('-P5').string() would return '-P5'.
    def string(self):
        if self.sign == -1:
            string = '-'
        else:
            string = ''

        string += f'{Interval.qualities[self.qual]}{self.span + self.xoct * 7 + 1}'

        return string

    ## Returns the full interval name, e.g. 'doubly-augmented third'
    #  or 'descending augmented sixth'
    # @param sign If true then "descending" will appear in the
    # name if it is a descending interval.
    def full_name(self, *, sign=True):
        string = ''
    
        if self.sign == -1:
            string += 'descending '
        string += f'{self.quality_name()} {self.span_name()}'

        return string

    ## Returns the full name of the interval's span, e.g. a
    # unison would return "unison" and so on.
    def span_name(self):
        return Interval.span_names[self.span]

    ## Returns the full name of the interval's quality, e.g. a
    # perfect unison would return "perfect" and so on.
    def quality_name(self):
        string = ''
        quality = Interval.qualities[self.qual]

        if quality in Interval.diminishes:
            string += Interval.numerical_adverbs[len(quality) - 1]
            string += 'diminished'
        elif quality in Interval.augments:
            string += Interval.numerical_adverbs[len(quality) - 1]
            string += 'augmented'
        elif quality == 'm':
            string += 'minor'
        elif quality == 'P':
            string += 'perfect'
        elif quality == 'M':
            string += 'major'
        else:
            raise ValueError("Undefined quality")
    
        return string

    ## Returns true if this interval and the other interval have the
    # same span, quality and sign. The extra octaves are ignored.
    def matches(self, other):
        if not isinstance(other, Interval):
            raise TypeError("Other is not an instance of Interval")

        return self.span == other.span and self.qual == other.qual and self.sign == other.sign

    ## Returns the interval's number of lines and spaces, e.g.
    # a unison will return 1.
    def lines_and_spaces(self):
        return self.span + 1

    ## Private method that returns a zero based interval quality from its 
    #  external name. Raises an assertion if the name is invalid. See:
    # is_unison() and similar.
    def _to_iq(self):
        if self.is_perfect_type():
            return Interval.perfect_qualities.index(Interval.qualities[self.qual]) - Interval.perfect_index
        else:
            return Interval.imperfect_qualities.index(Interval.qualities[self.qual]) - Interval.imperfect_index

    ## Returns the interval values as a list: [span, qual, xoct, sign]
    def to_list(self):
        return [self.span, self.qual, self.xoct, self.sign]

    ## Returns true if the interval is a unison otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of unison, which can be any valid quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_unison(self, qual=None):
        if qual == None:
            return self.span == 0
        else:
            return self.span == 0 and Interval.quality_letter_to_symbol.get(Interval.qualities[self.qual], Interval.qualities[self.qual]) == Interval.quality_letter_to_symbol.get(qual, qual)

    ## Returns true if the interval is a second otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of second, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_second(self, qual=None):
        if qual == None:
            return self.span == 1
        else:
            return self.span == 1 and Interval.quality_letter_to_symbol.get(Interval.qualities[self.qual], Interval.qualities[self.qual]) == Interval.quality_letter_to_symbol.get(qual, qual)

    ## Returns true if the interval is a third otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of third, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_third(self, qual=None):
        if qual == None:
            return self.span == 2
        else:
            return self.span == 2 and Interval.quality_letter_to_symbol.get(Interval.qualities[self.qual], Interval.qualities[self.qual]) == Interval.quality_letter_to_symbol.get(qual, qual)

    ## Returns true if the interval is a fourth otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of fourth, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_fourth(self, qual=None):
        if qual == None:
            return self.span == 3
        else:
            return self.span == 3 and Interval.quality_letter_to_symbol.get(Interval.qualities[self.qual], Interval.qualities[self.qual]) == Interval.quality_letter_to_symbol.get(qual, qual)

    ## Returns true if the interval is a fifth otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of fifth, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_fifth(self, qual=None):
        if qual == None:
            return self.span == 4
        else:
            return self.span == 4 and Interval.quality_letter_to_symbol.get(Interval.qualities[self.qual], Interval.qualities[self.qual]) == Interval.quality_letter_to_symbol.get(qual, qual)

    ## Returns true if the interval is a sixth otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of sixth, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_sixth(self, qual=None):
        if qual == None:
            return self.span == 5
        else:
            return self.span == 5 and Interval.quality_letter_to_symbol.get(Interval.qualities[self.qual], Interval.qualities[self.qual]) == Interval.quality_letter_to_symbol.get(qual, qual)

    ## Returns true if the interval is a seventh otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of seventh, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_seventh(self, qual=None):
        if qual == None:
            return self.span == 6
        else:
            return self.span == 6 and Interval.quality_letter_to_symbol.get(Interval.qualities[self.qual], Interval.qualities[self.qual]) == Interval.quality_letter_to_symbol.get(qual, qual)

    ## Returns true if the interval is an octave otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of octave, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_octave(self, qual=None):
        if qual == None:
            return self.span == 7
        else:
            return self.span == 7 and Interval.quality_letter_to_symbol.get(Interval.qualities[self.qual], Interval.qualities[self.qual]) == Interval.quality_letter_to_symbol.get(qual, qual)

    ## Returns a 'diminution count' 1-5 if the interval is diminished else False.
    # For example, if the interval is doubly-diminished then 2 is returned.
    # If the interval not diminished at all (e.g. is perfect, augmented, minor or
    # major) then False is returned.
    def is_diminished(self):
        quality = Interval.qualities[self.qual]
        if quality in Interval.diminishes:
            return len(quality)
        else:
            return False

    ## Returns true if the interval is minor, otherwise false.
    def is_minor(self):
        return Interval.qualities[self.qual] == 'm'

    ## Returns true if the interval is perfect, otherwise false.
    def is_perfect(self):
        return Interval.qualities[self.qual] == 'P'

    ## Returns true if the interval is major, otherwise false.
    def is_major(self):
        return Interval.qualities[self.qual] == 'M'

    ## Returns a 'augmentation count' 1-5 if the interval is augmented else False.
    # For example, if the interval is doubly-augmented then 2 is returned.
    # If the interval not augmented at all (e.g. is perfect, diminished, minor or
    # major) then False is returned.
    def is_augmented(self):
        quality = Interval.qualities[self.qual]
        if quality in Interval.augments:
            return len(quality)
        else:
            return False

    ## Returns true if the interval belongs to the 'perfect interval'
    #  family, i.e. it is a Unison, 4th, 5th, or Octave.
    def is_perfect_type(self):
        return self.span in Interval.perfect_spans

    ## Returns true if this interval belongs to the 'imperfect interval'
    #  family, i.e. it is a 2nd, 3rd, 6th, or 7th.
    def is_imperfect_type(self):
        return self.span in Interval.imperfect_spans

    ## Returns true if this is a simple interval, i.e. its span is
    #  less-than-or-equal to an octave.
    def is_simple(self):
        return self.xoct == 0

    ## Returns true if this is a compound interval, i.e. its span is
    #  more than an octave (an octave is a simple interval).
    def is_compound(self):
        return self.xoct > 0

    ## Returns true if this interval's sign is 1.
    def is_ascending(self):
        return self.sign == 1

    ## Returns true if this interval's sign is -1.
    def is_descending(self):
        return self.sign == -1

    ## Returns true if the interval is a consonant interval. In this
    # context the perfect fourth should be considered consonant.
    def is_consonant(self):
        if self.is_perfect_type():
            return self.is_perfect()
        else:
            return self.is_third('m') or self.is_third('M') or self.is_sixth('m') or self.is_sixth('M')

    ## Returns true if the interval is not a consonant interval.
    def is_dissonant(self):
        return not self.is_consonant()

    ##  Returns a complemented copy of the interval. To complement an interval
    # you invert its span and quality. To invert the span, subtract it from
    # the maximum span index (the octave index). To invert the  quality subtract
    # it from the maximum quality index (quintuply augmented).
    def complemented(self):
        return Interval([7 - self.span, 12 - self.qual, self.xoct, self.sign])

    ## Returns the number of semitones in the interval. It is possible
    # to determine the number of semitones by looking at the span and
    # quality indexes. For example, if the span is a perfect fifth
    # (span index 4) and the quality is perfect (quality index 6)
    # then the semitones will be 5 and augmented or diminished fifths
    # will add or subtract semitones accordingly.
    #
    # This value will be negative for descending intervals otherwise positive.
    def semitones(self):
        return (Interval.span_to_keynum[self.span] + self._to_iq() + self.xoct * 12) * self.sign

    ## Adds a specified interval to this interval.
    #  @return  a new interval expressing the total span of both intervals.
    #  @param other the interval to add to this one.
    #
    # A TypeError should be raised if other is not an interval. A
    # NotImplementedError if either intervals are descending.
    def add(self, other):
        # Do NOT implement this method yet.
        if not isinstance(other, Interval):
            raise TypeError("Other is not an instance of Interval")
        elif self.is_descending() or other.is_descending():
            raise NotImplementedError("Either intervals are descending")
        new_self = Interval([self.span, self.qual, self.xoct, self.sign])

        new_self.span += other.span
        if new_self.span > 7:
            new_self.span -= 7
            new_self.xoct += 1

        new_self.xoct += other.xoct

        new_self.sign = 1

        new_self.qual = 0
        new_self.qual = self.semitones() + other.semitones() - new_self.xoct * 12 - Interval.span_to_keynum[new_self.span]

        if new_self.span in Interval.perfect_spans:
            new_self.qual = Interval.qualities.index(Interval.perfect_qualities[new_self.qual + Interval.perfect_index])
        else:
            new_self.qual = Interval.qualities.index(Interval.imperfect_qualities[new_self.qual + Interval.imperfect_index])

        return new_self

    # Transposes a Pitch or Pnum by the interval. Pnum transposition
    #  has no direction so if the interval is negative its complement
    #  should be used.
    #  @param pref  The Pitch or Pnum to transpose.
    #  @return The transposed Pitch or Pnum.
    def transpose(self, pref):
        # Do NOT implement this method yet.
        if isinstance(pref, Pitch):
            new_pitch = pref
            value = pref.pos()
            accidental = value - (value >> 4 << 4)
            value = value >> 4
            letter = value - (value >> 4 << 4)
            value = value >> 4
            octave = value

            letter += self.span * self.sign
            if letter >= 7 or letter < 0:
                letter = (letter + 7) % 7
                octave += self.sign

            octave += self.xoct * self.sign

            accidental += pref.keynum() + self.semitones() - Pitch([letter, accidental, octave]).keynum()

            return Pitch([letter, accidental, octave])
        elif isinstance(pref, Pitch.pnums):
            if self.is_descending():
                self = self.complemented()
            value = pref.value
            accidental = value - (value >> 4 << 4)
            value = value >> 4
            letter = value

            new_letter = letter + self.span
            if new_letter >= 7:
                new_letter = letter % 7

            accidental += Pitch([letter, accidental, 0]).keynum() + self.semitones() - Pitch([new_letter, accidental, 0]).keynum()

            return Pitch.pnums((new_letter << 4) + accidental)
        else:
            raise TypeError("Pref is not an instance of Pitch or Pnum")
