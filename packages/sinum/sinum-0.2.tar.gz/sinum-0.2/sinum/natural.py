def isNatural(number) :
    if type(number) == int :
        return True if number > 0 else False
    else :
        raise ValueError("Input is not a valid integer.")

def listNatural(limit) :
    if type(limit) == int :
        if limit>=0 :
            naturalList = [number+1 for number in range(limit)]
            return naturalList
        else :
            raise ValueError ('Limit must be positive or zero.')
    else :
        raise ValueError("Input is not a valid integer.")

def listNaturalBetween(start, end) :
    if type(start) == int and type(end) == int :
        if start >= 0 and end >= 0 :
            if start <= end :
                naturalList = [number for number in range(start, end) if isNatural(number)]
                return naturalList
            else :
                naturalList = [number for number in range(start, end, -1) if isNatural(number)]
                return naturalList
        else :
            raise ValueError('Range must be positive.')
    else :
        raise ValueError("Input is not a valid integer.")