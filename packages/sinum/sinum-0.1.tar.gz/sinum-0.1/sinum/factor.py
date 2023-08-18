def isFactor(divider, number) :
    if type(number) == int and type(divider) == int :
        return True if divider != 0 and number % divider == 0 else False
    else :
        raise ValueError("Input is not a valid integer.")

def factors(number) :
    if type(number) == int :
        factorsList = []
        for factor in range(1, number+1) :
            if isFactor(factor, number) :
                factorsList.append(factor)
        return factorsList
    else :
        raise ValueError("Input is not a valid integer.")