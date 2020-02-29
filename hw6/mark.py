###############################################################################

from enum import IntEnum

# Mark group constants 0-3 left-shifted 8 bits.
DYNAMIC = 0 << 8
ARTICULATION = 1 << 8
ORNAMENT = 2 << 8
TEMPORAL = 3 << 8


## The Mark class inherits from IntEnum to enumerate various types
# of notation marks that appear in musical scores. Each Mark enum is
# a 16 bit value with the format 'ggggggggrrrrrrrr', where:
# @code
# 7654321076543210
# gggggggg--------   the 'group' of the mark (dynamic, articulation, etc.)
# --------rrrrrrrr   the 'rank' of the identifier within its group.
# @endcode
#
# The mark module defines four top-level 'group' constants: DYNAMIC,
# ARTICULATION, ORNAMENT, and TEMPORAL. These constants are assigned
# the values 0 to 3 and left-shifted 8 bits.

# The DYNAMIC group enums are: NIENTE, PPPP, PPP, PP, P, MP, MF, F, FF, FFF,
# FFFF, SFZ, CRESCENDO, CRESCENDO_END, DECRESCENDO, DECRESCENDO_END.
# These enums all have DYNAMIC as their upper byte and their lower byte
# holds their rank value 0-15.

# The ARTICULATION group enums are: TENUTO, DETATCHED, STACCATO, STACCATISSIMO,
# ACCENT, MARCATO. These enums all have ARTICULATION as their upper byte and
# their lower byte holds their rank value 0-5.

# The ORNAMENT group enums are: TRILL, MORDENT, TURN. These enums all have
# ORNAMENT as their upper byte and their lower byte holds their rank value 0-2.

# The TEMPORAL group enums are: FERMATA, ACCEL, DEACCEL. These enums all have
# TEMPORAL as their upper byte and their lower byte holds their rank value 0-2.

#  See: https://en.wikipedia.org/wiki/Dynamics_(music)
#  https://en.wikipedia.org/wiki/Articulation_(music)
#  https://en.wikipedia.org/wiki/Ornament_(music)
class Mark (IntEnum):
    # Create enums here...
    NIENTE = DYNAMIC + 0
    PPPP = DYNAMIC + 1
    PPP = DYNAMIC + 2
    PP = DYNAMIC + 3
    P = DYNAMIC + 4
    MP = DYNAMIC + 5
    MF = DYNAMIC + 6
    F = DYNAMIC + 7
    FF = DYNAMIC + 8
    FFF = DYNAMIC + 9
    FFFF = DYNAMIC + 10
    SFZ = DYNAMIC + 11
    CRESCENDO = DYNAMIC + 12
    CRESCENDO_END = DYNAMIC + 13
    DECRESCENDO = DYNAMIC + 14
    DECRESCENDO_END = DYNAMIC + 15
    TENUTO = ARTICULATION + 0
    DETATCHED = ARTICULATION + 1
    STACCATO = ARTICULATION + 2
    STACCATISSIMO = ARTICULATION + 3
    ACCENT = ARTICULATION + 4
    MARCATO = ARTICULATION + 5
    TRILL = ORNAMENT + 0
    MORDENT = ORNAMENT + 1
    TURN = ORNAMENT + 2
    FERMATA = TEMPORAL + 0
    ACCEL = TEMPORAL + 1
    DEACCEL = TEMPORAL + 2

    ## Returns the mark's rank number from the lower eight
    # bits of the enum.
    def rank(self):
        return self.value - (self.value >> 8 << 8)

    ## Returns the mark's group number from the upper eight
    # bits of the enum.
    def group(self):
        return self.value >> 8 << 8
