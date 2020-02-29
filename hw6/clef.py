###############################################################################

from enum import Enum

## Line-Space unit constants.
TOP_LINE = 8
SPACE_BELOW_TOP_LINE = 7
LINE_ABOVE_MIDDLE_LINE = 6
SPACE_ABOVE_MIDDLE_LINE = 5
MIDDLE_LINE = 4
SPACE_BELOW_MIDDLE_LINE = 3
LINE_BELOW_MIDDLE_LINE = 2
SPACE_ABOVE_BOTTOM_LINE = 1
BOTTOM_LINE = 0


## An enumeration of music clefs using 3-tuples. The first value in the enum's
# tuple is a unique number of the clef 0-15. The second value is the
# attachment position of the clef in 'line-space' units (see above), where 0
# is bottom line, 1 is the space above , 3 is space below middle line,
# and so on. The third value is a clef transposition value. This is usually 0,
# but for a transposing clef it will be either 8, -8, 15, or -15 depending on
# the clef. The clefs to enumerate are: TREBLE, SOPRANO, MEZZO_SOPRANO, ALTO,
# TENOR, BARITONE, BASS, TREBLE_8VA, BASS_8VA, TREBLE_15MA, BASS_15MA,
# TENOR_TREBLE, BARITONE_F, SUB_BASS, FRENCH_VIOLIN, PERCUSSION
#
# For information about clefs see: https://en.wikipedia.org/wiki/Clef
class Clef (Enum):
    # Create enums here...
    TREBLE = (0, 2, 0)
    SOPRANO = (1, 0, 0)
    MEZZO_SOPRANO = (2, 2, 0)
    ALTO = (3, 4, 0)
    TENOR = (4, 6, 0)
    BARITONE = (5, 8, 0)
    BASS = (6, 6, 0)
    TREBLE_8VA = (7, 2, 8)
    BASS_8VA = (8, 6, -8)
    TREBLE_15MA = (9, 2, 15)
    BASS_15MA = (10, 6, -15)
    TENOR_TREBLE = (11, 2, -8)
    BARITONE_F = (12, 4, 0)
    SUB_BASS = (13, 8, 0)
    FRENCH_VIOLIN = (14, 0, 0)
    PERCUSSION = (15, 4, 0)

    ## Returns the linespace attachment value of the clef.
    def linespace(self):
        return self.value[1]

    ## Returns the transposition level of the clef.
    def transposition(self):
        return self.value[2]


