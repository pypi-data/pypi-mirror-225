def isEven(number) :
    if type(number) == int :
        return True if number % 2 ==0 else False
    else :
        raise ValueError("Input is not a valid integer.")

def listEven(limit) :
    if type(limit) == int :
        if limit >= 0 :
            evenList = [number for number in range(0,limit*2,+2) if isEven(number)]
            return evenList
        else :
            raise ValueError ('Limit must be positive or zero.')
    else :
        raise ValueError("Input is not a valid integer.")

def listEvenBetween(start, end) :
    if type(start) == int and type(end) == int :
        if end >= start :
            evenList = [number for number in range(start, end) if isEven(number)]
        elif end < start :
            evenList = [number for number in range(start, end, -1) if isEven(number)]
        return evenList
    else :
        raise ValueError("Input is not a valid integer.")