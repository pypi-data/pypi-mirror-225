def isWhole(number) :
    if type(number) == int :
        return True if number >= 0 else False
    else :
        raise ValueError("Input is not a valid integer.")

def listWhole(limit) :
    if type(limit) == int :
        if limit>=0 :
            wholeList = [number for number in range(limit)]
            return wholeList
        else :
            raise ValueError ('Limit must be positive or zero.')
    else :
        raise ValueError("Input is not a valid integer.")

def listWholeBetween(start, end) :
    if type(start) == int and type(end) == int :
        if start >= 0 and end >= 0 :
            if start <= end :
                wholeList = [number for number in range(start, end) if isWhole(number)]
                return wholeList
            else :
                wholeList = [number for number in range(start, end, -1) if isWhole(number)]
                return wholeList
        else :
            raise ValueError('Range must be positive or zero.')
    else :
        raise ValueError("Input is not a valid integer.")