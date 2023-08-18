def isPrime(number) :
    if type(number) == int :
        if number > 1 :
            for num in range(2, number) :
                if number % num == 0 :
                    return False
            else :
                return True
        else :
            return False
    else :
        raise ValueError("Input is not a valid integer.")

def listPrimeBetween(start, end) :
    if type(start) == int and type(end) == int :
        if start < 0 or end < 0:
            raise ValueError('Range must be positive.')
        elif start <= end :
            primeList = [number for number in range(start, end) if isPrime(number)]
            return primeList
        elif start > end :
            primeList = [number for number in range(start, end, -1) if isPrime(number)]
            return primeList
    else :
        raise ValueError("Input is not a valid integer.")

def listPrime(limit) :
    if type(limit) == int :
        if limit >= 0 :
            number = 2
            primeList = []
            while(limit > 0) :
                if (isPrime(number)) :
                    primeList.append(number)
                    limit -= 1
                number += 1
            return primeList
        else :
            raise ValueError ('Limit must be positive or zero.')
    else :
        raise ValueError("Input is not a valid integer.")