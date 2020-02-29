from enum import Enum, IntEnum, auto

# Project: complete this implementation

class ScaleDegrees (Enum):
    # Degree enums, values are the semitonal content of the
    # major scale degrees
    SD1 = 0
    SD2 = 2
    SD3 = 4
    SD4 = 5
    SD5 = 7
    SD6 = 9
    SD7 = 11

    # Inflection enums, values -1 to 1
    LOWERED = -1
    DIATONIC = 0
    RAISED = 1

    # ScaleDegree enums, each is a tuple: (degree, inflection)
    TONIC = (SD1, DIATONIC)
    RAISED_TONIC = (SD1, RAISED)
    LOWERED_TONIC = (SD1, LOWERED)

    # ...define remaining scale degrees here...  
    SUPERTONIC = (SD2, DIATONIC)
    LOWERED_SUPERTONIC = (SD2, LOWERED)
    RAISED_SUPERTONIC = (SD2, RAISED)
    
    MEDIANT = (SD3, DIATONIC)
    LOWERED_MEDIANT = (SD3, LOWERED)
    RAISED_MEDIANT = (SD3, RAISED)
    
    SUBDOMINANT = (SD4, DIATONIC)
    LOWERED_SUBDOMINANT = (SD4, LOWERED)
    RAISED_SUBDOMINANT = (SD4, RAISED)
    
    DOMINANT = (SD5, DIATONIC)
    LOWERED_DOMINANT = (SD5, LOWERED)
    RAISED_DOMINANT = (SD5, RAISED)
    
    SUBMEDIANT = (SD6, DIATONIC)
    LOWERED_SUBMEDIANT = (SD6, LOWERED)
    RAISED_SUBMEDIANT = (SD6, RAISED)
    
    LEADINGTONE = (SD7, DIATONIC)
    LOWERED_LEADINGTONE = (SD7, LOWERED)
    RAISED_LEADINGTONE = (SD7, RAISED)
    
    def degree(self):
        """Returns the degree enum for this enum.
        Hint: the first tuple value of this enum
        will be the value of the degree enum."""
        
        return self.value[0]
    

    def inflection(self):
        """Returns the inflection enum for this enum.
        Hint: the second tuple value of this enum
        will be the value of the inflection enum."""
        
        return self.value[1]

    
    def semitones(self):
        """Returns the number of semitones in this
        scale degree.  Hint: Use the values of degrees
        and inflectons to determine the semitonal content"""

        return self.degree() + self.inflection()