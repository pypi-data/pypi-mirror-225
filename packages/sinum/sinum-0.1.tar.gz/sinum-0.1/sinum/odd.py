def isOdd(number) :
    if type(number) == int :
        return True if number % 2 !=0 else False
    else :
        raise ValueError("Input is not a valid integer.")

def listOdd(limit) :
    if type(limit) == int :
        if limit >= 0 :
            oddList = [number for number in range(1,limit*2,+2) if isOdd(number)]
            return oddList
        else :
            raise ValueError ('Limit must be positive or zero.')
    else :
        raise ValueError("Input is not a valid integer.")

def listOddBetween(start, end) :
    if type(start) == int and type(end) == int :
        if end >= start :
            oddList = [number for number in range(start, end) if isOdd(number)]
        elif end < start :
            oddList = [number for number in range(start, end, -1) if isOdd(number)]
        return oddList
    else :
        raise ValueError("Input is not a valid integer.")