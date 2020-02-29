##############################################################################
from enum import IntEnum
from math import pow


## A class that implements musical pitches.
#
# The Pitch class represent equal tempered pitches and returns information
# in hertz, keynum, pitch class, Pnum  and pitch name formats.  Pitches
# can be compared using standard math relations and maintain proper spelling
# when complemented or transposed by an Interval.


class Pitch:
    letters = [chr(ord('C') + i) for i in range(5)] + ['A', 'B']
    accidentals = ['bb', 'b', '', '#', '##']
    octaves = ['00'] + [str(i) for i in range(10)]
    letters_accidentals = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    letter_to_pc = {
        'C': 0,
        'D': 2,
        'E': 4,
        'F': 5,
        'G': 7,
        'A': 9,
        'B': 11
    }
    pc_to_letter = {
        0: 'C',
        2: 'D',
        4: 'E',
        5: 'F',
        7: 'G',
        9: 'A',
        11: 'B'
    }
    accidental_to_pc = {accidental: i - 2 for i, accidental in enumerate(accidentals)}
    default_to_safe_accidental = {
        'bb': 'ff',
        'b': 'f',
        '': '',
        '#': 's',
        '##': 'ss'
    }

    ## A class variable that holds an IntEnum of all possible letter-and-accidental
    #  combinations Cff up to Bss. Each pnum encodes its letter and accidental index
    #  as a one byte value 'llllaaaa', where 'llll' is its letter index 0-6, and
    #  'aaaa' is its accidental index 0-4.  You should set the pnums variable like this:
    #  pnum = IntEnum('Pnum', [tuple...]) where Pnum is the name of the enum class,
    #  [tuple...'] is a list of tuples, and each tuple is (enum_name, enum_val).
    #  The enum names are all possible combinations of pitch letters and accidentals
    #  e.g. 'Cff' upto  'Bss'.  Since the accidental character # is illegal as a
    #  python enum name be sure to use only the 'safe versions' of the accidental
    #  names: 'ff' upto 'ss'. The enum values are the one byte integers containing
    #  the letter and accidental indexes: (letter << 4) + accidental.
    pnums = IntEnum('Pnum', [((letter + accidental), (i << 4) + j) for (i, letter) in enumerate(letters) for (j, accidental) in enumerate(['ff', 'f', '', 's', 'ss'])])

    ## Creates a Pitch from a string or list, if neither is provided
    #  an empty Pitch is returned.
    #  * Pitch(string) - creates a Pitch from a pitch name string.
    #  * Pitch([l, a, o]) - creates a Pitch from a three element
    #  pitch list containing a letter, accidental and octave index
    #  (see below).
    #  * Pitch() - creates an empty Pitch.
    #
    #  @param ref A pitch name string, a list of three pitch indexes, or None.
    #
    # The format of a Pitch name string is:
    # @code
    #  <pitch> :=  <letter>, [<accidental>], <octave>
    #  <letter> := 'C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B'
    #  <accidental> := <2flat> | <flat> | <natural> | <sharp> | <2sharp>
    #  <2flat> := 'bb' | 'ff'
    #  <flat> := 'b' | 'f'
    #  <natural> := ''
    #  <sharp> := '#' | 's'
    #  <2sharp> := '##' | 'ss'
    #  <octave> := '00' | '0' | '1'  | '2'  | '3'  | '4'  | '5'  | '6'  | '7'  | '8'  | '9'
    # @endcode
    #
    # The format of a three-element pitch list is:
    # * A letter index 0-6 corresponding to the pitch letter names ['C', 'D', 'E', 'F', 'G', 'A', 'B'].
    # * An accidental index 0-4 corresponding to symbolic accidental names ['bb', 'b', '', '#', '##']
    #   or 'safe' accidental names ['ff', 'f', '', 's', 'ss'].
    # * An octave index 0-10 corresponding to the pitch octave names ['00', '0', '1', '2', '3',
    #   '4', '5', '6', '7', '8', '9'].
    #
    # If the argument is not a pitch string, a pitch list, or None the method
    # should raise a TypeError.  If the string or list contains invalid information the
    # method should raise a ValueError.
    #
    # Examples: Pitch('C4'), Pitch('F##2'), Pitch('Gs8'), Pitch('Bb3'), Pitch("Df00"),
    # Pitch([0,3,6]), Pitch()

    def __init__(self, ref=None):
        if isinstance(ref, str):
            i = 0
            
            try:
                if ref[i].capitalize() in Pitch.letters:
                    self.letter = ref[i].capitalize()
                    i += 1
                else:
                    raise ValueError("Invalid letter")
            except:
                raise ValueError("String cannot be empty")
            
            try:
                if ref[i : i + 2] == 'bb' or ref[i : i + 2] == 'ff':
                    self.accidental = 'bb'
                    i += 2
                elif ref[i] == 'b' or ref[i] == 'f':
                    self.accidental = 'b'
                    i += 1
                elif ref[i : i + 2] == '##' or ref[i : i + 2] == 'ss':
                    self.accidental = '##'
                    i += 2
                elif ref[i] == '#' or ref[i] == 's':
                    self.accidental = '#'
                    i += 1
                elif ref[i] == 'n':
                    self.accidental = ''
                    i += 1
                else:
                    self.accidental = ''
            except:
                raise ValueError("Invalid accidental")
            
            try:
                if ref[i] >= '0' and ref[i] <= '9':
                    self.octave = ref[i]
                    i += 1
                else:
                    raise ValueError("Invalid octave")
            except:
                raise ValueError("Octave cannot be empty")
            
            if self.octave == '0':
                try:
                    if ref[i] == '0':
                        self.octave += '0'
                        i += 1
                except:
                    pass
            
            if i != len(ref):
                raise ValueError("Octave should be the end of input")
        elif isinstance(ref, list):
            if len(ref) != 3:
                raise ValueError("Invalid ref length")
            
            if isinstance(ref[0], int):
                if ref[0] >= 0 and ref[0] < len(Pitch.letters):
                    self.letter = Pitch.letters[ref[0]]
                else:
                    raise ValueError("Invalid letter index")
            else:
                raise TypeError("Letter index is not int")
            
            if isinstance(ref[1], int):
                if ref[1] >= 0 and ref[1] < len(Pitch.accidentals):
                    self.accidental = Pitch.accidentals[ref[1]]
                else:
                    raise ValueError("Invalid accidental index")
            else:
                raise TypeError("Accidental index is not int")
               
            if isinstance(ref[2], int):
                if ref[2] >= 0 and ref[2] < len(Pitch.octaves):
                    self.octave = Pitch.octaves[ref[2]]
                else:
                    raise ValueError("Invalid octave index")
            else:
                raise TypeError("Octave index is not int")
        elif ref == None:
            self.letter = None
            self.accidental = None
            self.octave = None
        else:
            raise TypeError("Argument is not string, list, or None")
        
        if not self.is_empty():
            if self.keynum() < 0 or self.keynum() > 127:
                raise ValueError("Pitch does not have valid keynum")

        ## A letter index 0-6.
        # self.letter = None
        ## An accidental index 0-4.
        # self.accidental = None
        ## An octave index 0-10.
        # self.octave = None

    ## Returns a string displaying information about the
    #  pitch within angle brackets. Information includes the
    #  the class name, the pitch text, and the id of the object,
    #  for example '<Pitch: C#7 0x10f263e10>'. If the pitch is
    #  empty the string will show '<Pitch: empty 0x10f263b50>'.
    #  See also: string().
    def __str__(self):
        return ''

    ## Prints the external form of the Pitch that, if evaluated
    #  would create a Pitch with the same content as this pitch.
    #  Examples: 'Pitch("C#7")' and Pitch().  See also string().
    def __repr__(self):
        if not self.is_empty():
            return f'Pitch("{self.string()}")'
        else:
            return f'Pitch()'

    ## Implements Pitch < Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is less than the other.
    #
    # This method should call self.pos() and other.pos() to get the
    # two values to compare. See: pos().
    def __lt__(self, other):
        if isinstance(other, Pitch):
            try:
                return self.pos() < other.pos()
            except:
                raise ValueError("Pitch cannot be empty")
        else:
            raise TypeError("Other is not pitch")

    ## Implements Pitch <= Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is less than or equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __le__(self, other):
        if isinstance(other, Pitch):
            try:
                return self.pos() <= other.pos()
            except:
                raise ValueError("Pitch cannot be empty")
        else:
            raise TypeError("Other is not pitch")

    ## Implements Pitch == Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __eq__(self, other):
        if isinstance(other, Pitch):
            try:
                return self.pos() == other.pos()
            except:
                return False
        else:
            raise TypeError("Other is not pitch")

    ## Implements Pitch != Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is not equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ne__(self, other):
        if isinstance(other, Pitch):
            try:
                return self.pos() != other.pos()
            except:
                return True
        else:
            raise TypeError("Other is not pitch")

    ## Implements Pitch >= Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is greater or equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ge__(self, other):
        if isinstance(other, Pitch):
            try:
                return self.pos() >= other.pos()
            except:
                raise ValueError("Pitch cannot be empty")
        else:
            raise TypeError("Other is not pitch")

    ## Implements Pitch > Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is greater than the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __gt__(self, other):
        if isinstance(other, Pitch):
            try:
                return self.pos() > other.pos()
            except:
                raise ValueError("Pitch cannot be empty")
        else:
            raise TypeError("Other is not pitch")

    ## Returns a unique integer representing this pitch's position in
    #  the octave-letter-accidental space. The expression to calculate
    #  this value is (octave<<8) + (letter<<4) + accidental.
    def pos(self):
        if not self.is_empty():
            octave = int(self.octave)
            
            if self.octave != '00':
                octave += 1
            
            return (octave << 8) + (Pitch.letter_to_pc[self.letter] << 4) + Pitch.accidental_to_pc[self.accidental] + 2
        else:
            raise ValueError("Pitch cannot be empty")

    ## Returns true if the Pitch is empty. A pitch is empty if its
    # letter, accidental and octave attributes are None. Only one of
    # these attributes needs to be checked because __init__ will only
    # create a Pitch if all three are legal values or all three are None.
    def is_empty(self):
        return self.letter == None or self.accidental == None or self.octave == None

    ## Returns a string containing the pitch name including the
    #  letter, accidental, and octave.  For example,
    #  Pitch("C#7").string() would return 'C#7'.
    def string(self):
        if not self.is_empty():
            return self.letter + self.accidental + self.octave
        else:
            return 'empty'

    ## Returns the midi key number of the Pitch.
    def keynum(self):
        if not self.is_empty():
            midi = int(self.octave) * 12 + Pitch.letter_to_pc[self.letter] + Pitch.accidental_to_pc[self.accidental]
            
            if self.octave != '00':
                midi += 12
            
            if midi < 0 or midi > 127:
                raise ValueError("Keynum is out of range")
            
            return midi
        else:
            raise ValueError("Pitch cannot be empty")

    ## Returns the pnum (pitch class enum) of the Pitch. Pnums enumerate
    #  and order the letter and accidental of a Pitch so they can be compared,
    #  e.g.: C < C# < Dbb. See also: pnums.
    def pnum(self):
        if not self.is_empty():
            return Pitch.pnums[self.letter + Pitch.default_to_safe_accidental[self.accidental]]
        else:
            raise ValueError("Pitch cannot be empty")

    ## Returns the pitch class (0-11) of the Pitch.
    def pc(self):
        if not self.is_empty():
            pc = Pitch.letter_to_pc[self.letter] + Pitch.accidental_to_pc[self.accidental]
            pc = (pc + 12) % 12
            
            return pc
        else:
            raise ValueError("Pitch cannot be empty")

    ## Returns the hertz value of the Pitch.
    def hertz(self):
        if not self.is_empty():
            try:
                return 440.0 * 2 ** ((self.keynum() - 69) / 12)
            except:
                raise ValueError("Invalid keynum")
        else:
            raise ValueError("Pitch cannot be empty")

    ## A @classmethod that creates a Pitch for the specified
    #  midi key number.
    #  @param keynum A valid keynum 0-127.
    #  @param acci  The accidental to use. If no accidental is provided
    #  a default is chosen from C C# D Eb F F# G Ab A Bb B
    #  @returns a new Pitch with an appropriate spelling.
    #
    #  The function should raise a ValueError if the midi key number
    #  is invalid or if the pitch requested does not support the specified
    #  accidental.
    @classmethod
    def from_keynum(cls, keynum, accidental=None):
        if not isinstance(keynum, int):
            raise TypeError("Keynum is not int")
        elif keynum < 0 or keynum > 127:
            raise ValueError("Keynum is out of range")
        
        if accidental == None:
            octave = str(keynum // 12)
            
            if octave == '0':
                octave = '00'
            else:
                octave = str(int(octave) - 1)
                
            return Pitch(Pitch.letters_accidentals[keynum % 12] + octave)
        elif isinstance(accidental, str):
            if accidental == 'bb':
                keynum += 2
            elif accidental == 'b':
                keynum += 1
            elif accidental == '#':
                keynum -= 1
            elif accidental == '##':
                keynum -= 2
            else:
                raise ValueError("Invalid accidental")
            
            octave = str(keynum // 12)
            
            if octave == '0':
                octave = '00'
            else:
                octave = str(int(octave) - 1)
                
            try:
                return Pitch(Pitch.pc_to_letter[keynum % 12] + accidental + octave)
            except:
                raise ValueError("Pitch requested does not support the specified accidental")
        else:
            raise TypeError("Accidental is not string")