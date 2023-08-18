def isArmstrong(number) :
    if type(number) == int :
        number = abs(number)
        temp = number
        digits = len(str(temp))
        result = 0
        while number > 0 :
            result += (number % 10) ** digits
            number = number // 10
        return True if temp == result else False
    else :
        raise ValueError("Input is not a valid integer.")

def listArmstrong(limit) :
    if type(limit) == int :
        if limit >= 0 :
            number = 0
            armstrongList = []
            while limit > 0 :
                if isArmstrong(number) :
                    armstrongList.append(number)
                    limit -= 1
                number += 1
            return armstrongList
        else :
            raise ValueError ('Limit must be positive or zero.')
    else :
        raise ValueError("Input is not a valid integer.")

def listArmstrongBetween(start, end) :
    if type(start) == int and type(end) == int :
        if end >= start :
            armstrongList = [number for number in range(start, end) if isArmstrong(number)]
        elif end < start :
            armstrongList = [number for number in range(start, end, -1) if isArmstrong(number)]
        return armstrongList
    else :
        raise ValueError("Input is not a valid integer.")