###############################################################################
## @file
#  A class that implements fractional numbers.
#  The Ratio class provides exact arithmetic for representing exact musical
#  quantities such as proportional (metric) time, duration, and 'just' tuning
#  intervals. Ratios can be created from two integers or from a string.
#  Ratios are compared and combined using the standard math operators.

import math
from decimal import Decimal
from collections import namedtuple

RatioBase = namedtuple('RatioBase', 'num den')

class Ratio(RatioBase):

    ## Creates a Ratio from integers, a floating point number, or a string name.
    #  * Ratio(int, int) - creates a ratio from an integer numerator and denominator.
    #  * Ratio(int) - creates a ratio from an integer numerator with the denominator
    #  set to 1.
    #  * Ratio(float) - creates a ratio from a floating point number
    #  (see: as_integer_ratio())
    #  * Ratio(string) -  creates a ratio from a string 'num/den'. Both num and
    #  den must produce valid integers.
    #
    #  @param num If only num is specified it must be either an integer, float,
    #  or a string containing a valid ratio expression 'a/b'. If both num and
    #  den are provided they must both be integer value.
    #  @param den If specified den must be a non-zero integer denominator
    #
    #  Upon construction the new ratio will always be expressed in its most simple
    #  form, for example Ratio(6,12) will become Ratio(1/2), See: gcd().
    #  If both the numerator and denominator are negative the ratio should be
    #  converted to positive by the constructor.
    #
    #  The constructor should raise a TypeError if the num or den is not a integer,
    #  string or float and a DivisionByZero error if the denominator is 0.
    def __new__(cls, n, d=None):
        if isinstance(n, int):
            num = n

            if isinstance(d, int):
                den = d
            elif den == None:
                den = 1
            else:
                raise TypeError("Denominator is not an integer")

            if num * den > 0:
                num = num
                den = den
            else:
                num = -abs(num)
                den = abs(den)
        elif isinstance(n, float):
            if d != None:
                raise TypeError("Denominator should be None when numerator is float")
            num, den = Decimal(str(n)).as_integer_ratio()
        elif isinstance(n, str):
            length = len(n)
            num = ''
            den = ''
            i = 0
            has_slash = False

            if length > 0 and n[i] == '-':
                num += '-'
                i += 1

            while i < length:
                if n[i] >= '0' and n[i] <= '9':
                    num += n[i]
                    i += 1
                elif n[i] == '/':
                    has_slash = True
                    i += 1
                    break
                else:
                    raise TypeError("Numerator is not an integer")

            if has_slash:
                if length > 0 and n[i] == '-':
                    num += '-'
                    i += 1

                while i < length:
                    if n[i] >= '0' and n[i] <= '9':
                        den += n[i]
                        i += 1
                    else:
                        raise TypeError("Denominator is not an integer")

                try:
                    num = int(num)
                    den = int(den)
                except:
                    raise ValueError("Denominator cannot be empty")
            else:
                raise ValueError("Denominator cannot be empty")

        if den == 0:
            raise ZeroDivisionError("Denominator is 0")

        if num * den > 0:
            num = abs(num)
            den = abs(den)
        else:
            num = -abs(num)
            den = abs(den)
        gcd = math.gcd(num, den)
        num, den = num // gcd, den // gcd

        self = super(Ratio, cls).__new__(cls, num, den)

        return self

    ## Returns a string showing the ratio's fraction and the hex
    #  hex value of the ratio's memory address.
    #  Example: <Ratio: 1/4 0x10610d2b0>
    def __str__(self):
        return f'<Ratio: {self.num}/{self.den} {hex(id(self))}>'

    ## Returns a string expression that will evaluate to this ratio.
    def __repr__(self):
        return f'Ratio("{self.num}/{self.den}")'

    ## Implements Ratio*Ratio, Ratio*int and Ratio*float.
    # @param other An Ratio, int or float.
    # @returns A Ratio if other is a Ratio or an int, otherwise a float.
    #
    # A TypeError should be raised if other is not a Ratio, int or float.
    def __mul__(self, other):
        if isinstance(other, float):
            return self.num / self.den * other
        elif isinstance(other, Ratio):
            num, den = self.num * other.num, self.den * other.den
        elif isinstance(other, int):
            num, den = self.num * other, self.den
        else:
            raise TypeError("Other is not a Ratio, int or float")

        gcd = math.gcd(num, den)    
        return Ratio(num // gcd, den // gcd)

    ## Implements right side multiplication by calling __mul__
    #__rmul__ = __mul__
    def __rmul__(self, other):
        return self.__mul__(other)
    
    ## Implements 1 / ratio (reciprocal).
    #  @returns A new Ratio.
    def __invert__(self):
        if self.num == 0:
            raise ZeroDivisionError("Numerator is 0")
        elif self.num > 0:
            return Ratio(self.den, self.num)
        else:
            return Ratio(-self.den, -self.num)
    
    ## Implements Ratio/Ratio, Ratio/int and Ratio/float.
    # @param other A Ratio, int or float.
    # @returns A Ratio if other is a Ratio or an int, otherwise a float.
    #
    # A TypeError should be raised if other is not a Ratio, int or float.
    def __truediv__(self, other):
        if isinstance(other, Ratio):
            return self * other.__invert__()
        elif isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError("Other is 0")
            else:
                num, den = self.num, self.den * other

            gcd = math.gcd(num, den)
            return Ratio(num // gcd, den // gcd)
        elif isinstance(other, float):
            if other == 0:
                raise ZeroDivisionError("Other is 0")
            else:
                return self.num / self.den / other
        else:
            raise TypeError("Other is not a Ratio, int or float")

    ## Implements int / Ratio or float / Ratio (right side division).
    #  @returns A new Ratio.
    def __rtruediv__(self, other):
        if isinstance(other, (Ratio, int, float)):
            return self.__invert__() * other
        else:
            raise TypeError("Other is not a Ratio, int or float")

    ## A static method that returns the lowest common multiple of two integers
    # a and b. lcm be calculated using gcd(): (a*b) // gcd(a,b)
    @staticmethod
    def lcm(a, b):
        if isinstance(a, int) and isinstance(b, int):
            return (a * b) // math.gcd(a, b)
        else:
            raise TypeError("Input numbers are not int")
    
    ## Implements Ratio + Ratio, Ratio + int and Ratio + float. In order to
    #  add two ratios their denominators must be converted to the
    #  least common multiple of the current denominator. See: lcm().
    #  @returns A new Ratio.
    def __add__(self, other):
        if isinstance(other, Ratio):
            lcm = Ratio.lcm(self.den, other.den)
            return Ratio(self.num * lcm // self.den + other.num * lcm // other.den, lcm)
        elif isinstance(other, int):
            return Ratio(self.num + other * self.den, self.den)
        elif isinstance(other, float):
            return self.num / self.den + other
        else:
            raise TypeError("Other is not a Ratio, int or float")

    ## Implements right side addition by calling __add__.
    #  @returns A new Ratio.
    #__radd__ = __add__
    def __radd__(self, other):
        return self + other
    
    ## Implements -ratio (negation).
    #  @returns A new Ratio.
    def __neg__(self):
        return Ratio(self.num * -1, self.den)

    ## Implements ratio - ratio, ratio - int and ratio - float.
    #  @returns A new Ratio.
    def __sub__(self, other):
        return self + -other

    ## Implements int - ratio and float-ratio (right side subtraction).
    #  @returns A new Ratio.
    def __rsub__(self, other):
        # other is the LEFT side non-ratio operand.
        return -self + other

    ## Implements ratio % ratio.
    #  @returns A new Ratio.
    def __mod__(self, other):
        if not isinstance(other, (Ratio, int)):
            raise TypeError("Other is not a Ratio or int")
        elif isinstance(other, int):
            other = Ratio(other)

        q = int(self / other * 1.0)
        d = self - other * q

        if d.num < 0:
            if other.num < 0:
                d -= other
            else:
                d += other

        return d


    ## Implements Ratio**int, Ratio**float, and Ratio**Ratio.
    #  @returns If the exponent is a positive or negative int
    #  a Ratio should be returned. Otherwise for Ratio or float
    #  exponents a float should be returned. See: math.pow().
    def __pow__(self, other):
        if isinstance(other, int):
            to_return = self

            if other < 0:
                to_return = to_return.__invert__()
                other = -other

            to_return.num = to_return.num ** other
            to_return.den = to_return.den ** other

            return to_return
        elif isinstance(other, (Ratio, float)):
            return (1.0 * self) ** (1.0 * other)
        else:
            raise TypeError("Other is not a Ratio, int or float")

    ## Implements an int**ratio or float**ratio
    #  @param other  The base integer or float.
    #  @returns A floating point number.
    #
    #  The function can be implemented using math.pow().
    def __rpow__(self, other):
        if isinstance(other, (int, float)):
            return (1.0 * other) ** (1.0 * self)
        else:
            raise TypeError("Other is not a int or float")

    ## Implements Ratio < Ratio, Ratio < int, Ratio < float. See: compare().
    def __lt__(self, other):
        if isinstance(other, (Ratio, int)):
            return (self - other).num < 0
        elif isinstance(other, float):
            return self - other < 0
        else:
            raise TypeError("Other is not a Ratio, int or float")

    ## Implements Ratio <= Ratio, Ratio <= int, Ratio <= float. See: compare().
    def __le__(self, other):
        if isinstance(other, (Ratio, int)):
            return (self - other).num <= 0
        elif isinstance(other, float):
            return self - other <= 0
        else:
            raise TypeError("Other is not a Ratio, int or float")

    ## Implements Ratio <= Ratio, Ratio <= int, Ratio <= float. See: compare().
    def __eq__(self, other):
        if isinstance(other, (Ratio, int)):
            return (self - other).num == 0
        elif isinstance(other, float):
            return self - other == 0
        else:
            return False

    ## Implements Ratio != Ratio, Ratio != int, Ratio != float. See: compare().
    def __ne__(self, other):
        return not self == other

    ## Implements Ratio >= Ratio, Ratio >= int, Ratio >= float. See: compare().
    def __ge__(self, other):
        if isinstance(other, (Ratio, int)):
            return (self - other).num >= 0
        elif isinstance(other, float):
            return self - other >= 0
        else:
            raise TypeError("Other is not a Ratio, int or float")

    ## Implements Ratio>Ratio, Ratio > int, Ratio > float. See: compare().
    def __gt__(self, other):
        if isinstance(other, (Ratio, int)):
            return (self - other).num > 0
        elif isinstance(other, float):
            return self - other > 0
        else:
            raise TypeError("Other is not a Ratio, int or float")

    ## Returns a single integer hash value for the ratio: (num<<16 + den)
    def __hash__(self):
        return self.num << 16 + self.den

    ## Helper method implements ratio comparison. Returns 0 if the ratios are equal,
    # a negative value if self is less than other and a positive value if self is
    # GEQ other. Given two ratios the comparison is (num1*den2) - (num2/den1)
    def compare(self, other):
        if isinstance(other, (int, float)):
            other = Ratio(other)

        if not isinstance(other, Ratio):
            raise TypeError("Other is not a Ratio, int or float")
        
        return (self.num * other.den) - (other.num * self.den)

    ## Returns the string name of the ratio 'num/den'.
    def string(self):
        return f'{self.num}/{self.den}'

    ## Returns 1/ratio.
    def reciprocal(self):
        return self.__invert__()

    ## Returns the musical 'dotted' value of the ratio, e.g. 1/4 with
    #  one dot is 1/4 + 1/8 = 3/8.
    #  @param dots  The number of dots to apply, each dot adds half the
    #  previous value of the ratio.
    #  @return A new ratio representing the dotted value.

    # The method should raise a ValueError if dots is not a positive integer.
    def dotted(self, dots=1):
        if not isinstance(dots, int):
            raise ValueError("Dots is not a positive integer")
        elif dots <= 0:
            raise ValueError("Dots is not a positive integer")

        return self * (2 - Ratio(1, 2) ** dots)

    ## Returns a list of num sub-divisions (metric 'tuples') that sum to
    #  value of ratio*num.
    #  @param num  The number of tuples to return.
    #  @param intimeof  A number that, when multiplied by the fraction
    #  itself, represents the sum of all the tuplets returned.
    #  @returns A list of num ratios that sum to the value of the Ratio.
    #
    #  Examples: Ratio(1,4).tuplets(3) returns three tuplets [1/12, 1/12, 1/12]
    #  which sum to Ratio(1,4).  Ratio(1,4).tuplets(3,2) returns three
    #  tuplets [1/6, 1/6, 1/6] which sum to ratio*2, or 1/2.
    def tuplets(self, num, intimeof=1):
        if not isinstance(num, int):
            raise ValueError("Num is not a positive integer")
        elif num <= 0:
            raise ValueError("Num is not a positive integer")

        if not isinstance(intimeof, (Ratio, int)):
            raise TypeError("Intimeof is not a positive Ratio or int")
        elif intimeof <= 0:
            raise TypeError("Intimeof is not a positive Ratio or int")

        if isinstance(intimeof, int):
            intimeof = Ratio(intimeof)

        return [(self * intimeof / num) for i in range(0, num)]

    ## Returns the ratio representing num divisions of this ratio.
    #  @param num  The number to divide this ratio by.
    #  @return The new tuple value ratio.
    #
    #  Example:  Ratio(1,4).tup(5) is 1/20
    def tup(self, num):
        if not isinstance(num, (Ratio, int)):
            raise TypeError("Num is not a positive Ratio or int")
        elif num <= 0:
            raise TypeError("Num is not a positive Ratio or int")

        if isinstance(num, int):
            num = Ratio(num)

        return self / num

    ## Returns the ratio as a floating point number.
    def float(self):
        return 1.0 * self

    ## Converts the ratio to floating point seconds according to a
    #  given tempo and beat:
    #  @param tempo  The tempo in beats per minute. Defaults to 60.
    #  @param beat  A ratio representing the beat. Defaults to 1/4 (quarter note).
    def seconds(self, tempo=60, beat=None):
        if beat == None:
            beat = Ratio(1, 4)
        
        if not isinstance(tempo, (Ratio, int)):
            raise TypeError("Tempo is not a positive Ratio or int")
        elif tempo <= 0:
            raise TypeError("Tempo is not a positive Ratio or int")

        if isinstance(tempo, int):
            tempo = Ratio(tempo)

        if not isinstance(beat, (Ratio, int)):
            raise TypeError("Beat is not a positive Ratio or int")
        elif beat <= 0:
            raise TypeError("Beat is not a positive Ratio or int")

        if isinstance(beat, int):
            beat = Ratio(beat)

        return (self / beat / tempo * 60) * 1.0



if __name__ == '__main__':
    pass