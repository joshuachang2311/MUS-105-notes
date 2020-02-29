def power(base, exp):
    """
    Implement the math.pow function for integer powers. Note: exp can still be negative. This should be
    handled properly. What other edge cases should we be careful of? Return base^exp as a float.

    THIS IMPLEMENTATION SHOULD NOT USE: math.pow(base, exp) or base ** exp

    :param base: number to raise to a given power
    :type base: int
    :param exp: power to raise the base to. NOTE: this number can be negative!
    :type exp: int
    :return: base to the exp power
    :rtype: float
    """
    # replace the line below with your code

    if base == 0:
        if exp == 0:
            return 1.0
        else:
            return 0.0

    to_return = 1.0

    if exp >= 0:
        for i in range(0, exp):
            to_return *= base
    else:
        for i in range(0, -1 * exp):
            to_return /= base

    return to_return

def list_sum(l):
    """
    given a list l, return the sum of all the elements of l. You can assume that l only contains ints & floats.

    :param l: list of floats/ints
    :type l: list
    :return: the sum of all the elements in l, AS A FLOAT
    :rtype: float
    """
    # replace the line below with your code
    
    to_return = 0.0
    
    for i in l:
        to_return += i
        
    return to_return

def str_to_int(num_string):
    """
    Turn a string into an integer. For this function, num_string can be a string representation of a number in either
    binary, octal, decimal, or hexadecimal. Depending on the base, the string will start differently:
        binary:      "0b100" = 4 "0b" is first 2 characters
        octal:       "0o11"  = 9 "0o" is first 2 characters
        decimal:     "10"    = 10 no extra characters
        hexadecimal: "0xa"   = 10
     For binary, octal, and hexadecimal, the string will always be longer than 2 (i.e. the base prefix, and then the
     number. No matter the base, you are to correctly convert the string to an int and return it.

     If the base is unrecognized (the first two are not numbers, and also are not '0b', '0o', or '0x', the function
     should return -1.

    Don't worry about negative numbers!

    **hint** remember that the int() function can take multiple parameters. What was that second parameter?

    :param num_string: string representation of the integer
    :type num_string: str
    :return: integer with the value represented in the string, or negative one if the base is unrecognized
    :rtype: int
    """
    # replace the line below with your code
    
    length = len(num_string)
    
    if length == 0:
        return -1
    elif length == 1:
        return int(num_string)
    else:
        to_return = 0
        base = num_string[0:2]
        
        if(base == '0b'):
            for i in range(2, length):
                c = num_string[i]
                if(c < '0' or c > '1'):
                    return -1
                else:
                    to_return += int(c) * (2 ** (length - i - 1))
        elif(base == '0o'):
            for i in range(2, length):
                c = num_string[i]
                
                if(c < '0' or c > '7'):
                    return -1
                else:
                    to_return += int(c) * (8 ** (length - i - 1))
        elif(base == '0x'):
            for i in range(2, length):
                c = num_string[i]
                exp = 16 ** (length - i - 1)
                
                if(c >= '0' and c <= '9'):
                    to_return += int(c) * exp
                elif(c == 'a'):
                    to_return += 10 * exp
                elif(c == 'b'):
                    to_return += 11 * exp
                elif(c == 'c'):
                    to_return += 12 * exp
                elif(c == 'd'):
                    to_return += 13 * exp
                elif(c == 'e'):
                    to_return += 14 * exp
                elif(c == 'f'):
                    to_return += 15 * exp
                else:
                    return -1
        else:
            for i in range(0, length):
                c = num_string[i]
                
                if(c < '0' or c > '9'):
                    return -1
                else:
                    to_return += int(c) * (10 ** (length - i - 1))
        
        return to_return

def print_christmas_tree(size):
    """
    A christmas tree with size n is defined as a string having n + 1 rows, where the i'th row contains the (i-1)'th row's
    number of stars + 2, arranged in a symmetrical manner. the 0'th row should have 1 star. the last (n'th) row should
    be equivalent to the 0'th row (the trunk of the tree). the stars are asterisks: '*'. size is always >= 2.

    Example of a size 4 tree:
       *
      ***
     *****
    *******
       *

    The return should be a single string, with each row separated by '\n'. Mind the spacing in each row--there should
    be spaces before the '*'s on each row, but not after.

    size 4 tree as string:
        "   *\n  ***\n *****\n*******\n   *"

    **hint** print out your tree to the console a few times to make sure the spacing is correct.

    :param size: a number >=2
    :type size: int
    :return: string representation of a christmas tree
    :rtype: str
    """
    # replace the line below with your code
    
    to_return = ''
    
    for i in range(0, size):
        for j in range(0, size - i - 1):
            to_return += ' '
        
        for j in range(0, i * 2 + 1):
            to_return += '*'
        
        to_return += '\n'
    
    for j in range(0, size - 1):
        to_return += ' '
    
    to_return += '*'
    
    return to_return

def list_to_str(l):
    """
    Implement the __str()__ function for the list class. This function should take a list, and convert
    it to its string representation. You can assume that for each element in the list, the str() function
    will give the appropriate string to use for the entire list string. Some examples of list strings:
        [1, 2, 3, 4, 5, 6]
        [True, False, True, True, False]
        ['hi', 'my', 'name', 'is']

    * NOTICE: for string elements, the string itself is surrounded by single quotes. You are expected to
              implement this. this is the only special case you should be aware of
    * you will not be graded on the spacing of your string representation, i.e. [1,2,3] == [1, 2, 3] == [ 1, 2, 3 ]
    * you can assume that there will be no nested lists/dictionaries/tuples nested in the list
    * do NOT assume that all elements in the list are of the same type

    * YOU ARE EXPECTED TO USE str() FOR EACH ELEMENT IN THE LIST
    * DO NOT USE str() ON THE LIST ITSELF

    :param l: list to convert to string
    :type l: list
    :return: string representation of that list
    :rtype: str
    """
    # replace the line below with your code
    
    to_return = '['
    
    for element in l:
        if isinstance(element, str):
            to_return += '\''
            to_return += element
            to_return += '\''
        else:
            to_return += str(element)
        
        to_return += ', '
        
    to_return = to_return[0:len(to_return) - 2]
    to_return += ']'
    
    return to_return

def remove_substring_instances(in_str, substr):
    """
    given the string input, find all instances of substr and remove them from the input. Then, return the number of
    instances of substr that were removed, as well as the new string with all instances of substr removed, as a tuple.
    for example:
        return num_instances, new_string

    :param in_str: string to clean up
    :type in_str: str
    :param substr: substring to find and remove
    :type substr: str
    :return: a tuple where the first element is the number of elements removed, and the second is the string after
        cleaning
    :rtype: tuple
    """
    # replace the line below with your code
    
    in_str_length = len(in_str)
    substr_length = len(substr)
    num_instances = 0
    to_return = ""
    
    i = 0
    
    while i < in_str_length:
        if (i + substr_length) > in_str_length:
            to_return += in_str[i]
            i += 1
            
            continue
        
        flag = True
        
        for j in range(0, substr_length):
            if in_str[i + j] != substr[j]:
                flag = False
                break
                
        if flag == True:
            i += substr_length
            num_instances += 1
        else:
            to_return += in_str[i]
            i += 1
            
    return num_instances, to_return