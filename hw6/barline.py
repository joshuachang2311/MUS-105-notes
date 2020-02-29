###############################################################################

from enum import Enum, auto

## A barline represents the right or left side delimiter of a bar.  The set
# of bar lines are: STANDARD, DOTTED, DASHED, TICKED, SHORT, HEAVY,
# INTERIOR_DOUBLE, FINAL_DOUBLE, LEFT_REPEAT, RIGHT_REPEAT, MIDDLE_REPEAT.
# The enum values do not matter, you can use enum.auto() to assign them.
# See: https://en.wikipedia.org/wiki/Bar_(music)

class Barline (Enum):
    # Create enums here...
    STANDARD = auto()
    DOTTED = auto()
    DASHED = auto()
    TICKED = auto()
    SHORT = auto()
    HEAVY = auto()
    INTERIOR_DOUBLE = auto()
    FINAL_DOUBLE = auto()
    LEFT_REPEAT = auto()
    RIGHT_REPEAT = auto()
    MIDDLE_REPEAT = auto()