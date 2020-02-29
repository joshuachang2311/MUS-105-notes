###############################################################################

from .pitch import Pitch
from .mode import Mode
from .interval import Interval

## A class that implements musical keys.
#
# The Key class represents the complete chromatic set of keys in western music.
# A key consists of an integer 'signum' representing the number of sharps or
# flats in the key's signature, and a mode (Enum). Keys can return Pnums
# representing their tonic note and diatonic scale degrees.
# See: https://en.wikipedia.org/wiki/Key_(music)
class Key:
    ## Creates a Key from an integer key signature identifier and mode.
    #  @param signum  A value -7 to 7 representing the number of flats
    #  (negative) or sharps (positive).
    #  @param mode  A Mode enum, or its case-insensitive string name.
    #
    #  The constructor should raise a TypeError if signum is not an integer
    #  or if mode is not a Mode or string. The constructor should raise a
    #  ValueError if the signum integer or the mode string is invalid.
    def __init__(self, signum, mode):
        if not isinstance(signum, int):
            raise TypeError("signum is not an integer")
        elif abs(signum) > 7:
            raise ValueError("signum integer is invalid")
        else:
            self.signum = signum

        if isinstance(mode, Mode):
            self.mode = mode
        elif isinstance(mode, str):
            try:
                self.mode = Mode[mode.upper()]
            except:
                raise ValueError("mode string is invalid")
        else:
            raise TypeError("mode is not a Mode or string")

    ## Returns the print representation of the key. The string should
    # include the class name, tonic, mode, number of sharps or flats,
    # and the instance id.
    #
    # Examples:
    # <Key: C-Major (0 sharps or flats) 0x10c03c050>
    # <Key: G-Major (1 sharp) 0x10eec5250>
    # <Key: A-Mixolydian (2 sharps) 0x10c03c490>
    # <Key: Af-Minor (7 flats) 0x10c03c390>
    def __str__(self):
        string = '<Key: '
        string += self.string()
        string += ' (' + str(abs(self.signum))

        if self.signum > 0:
            string += 'sharp'
        elif self.signum < 0:
            string += 'flat'
        else:
            string += 'sharps or flats'

        if abs(self.signum) > 1:
            string += 's'

        string += f' {hex(id(self))}>'

        return string

    ## Returns the external representation of the Key including the
    # constructor name, signum, and the capitalized version of the
    # mode's name.
    #
    # Examples:
    # 'Key(4, "Dorian")'
    # 'Key(-1, "Major")'
    def __repr__(self):
        return f'Key({self.signum}, "{self.mode.name.capitalize()}")'

    ## Returns a string containing the name of the tonic Pnum, a
    # hyphen, and the capitalized version of the mode's name.
    #
    # Examples: Fs-Dorian, Bf-Phrygian, B-Major
    def string(self):
        return f'{self.tonic()}-{self.mode.name.capitalize()}'

    ## Returns a Pnum representing the key's tonic. The tonic can
    # be calculated by transposing the Major tonic (Pnum) by the
    # interval distance of the mode above the major. The
    # transposition can be performed using that interval's transpose()
    # method. The interval distances of Major up to Locrian are:
    # P1, M2, M3, P4, P5, M6, M7.
    #
    # Examples:
    # Key(0, "lydian").tonic() is Pnum F.
    # Key(2, "dorian").tonic() is Pnum E.
    # Key(-6, "phrygian").tonic() is Pnum Bf.
    def tonic(self):
        return self.scale()[0]

    ## Returns a list of Pnums representing the unique pitches of the key's
    # diatonic scale. The octave completion should NOT be included in the list.
    def scale(self):
        pnum_names = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

        for i in range(0, self.signum):
            pnum_names[(i * 4 + 3) % 7] += 's'
        for i in range(0, self.signum, -1):
            pnum_names[(i * 4 - 1) % 7] += 'f'

        scale = [Pitch.pnums[pnum_name] for pnum_name in pnum_names]
        rotate = (self.signum * 4 + self.mode.value) % 7
        if rotate < 0:
            rotate += 7

        if rotate == 0:
            return scale
        else:
            return scale[rotate:] + scale[:rotate]