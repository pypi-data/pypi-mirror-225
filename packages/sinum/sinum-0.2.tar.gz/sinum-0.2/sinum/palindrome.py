def isPalindrome(number) :
    if type(number) == int :
        return True if int(str(abs(number))[::-1]) == abs(number) else False
    else :
        raise ValueError("Input is not a valid integer.")

def listPalindrome(limit) :
    if type(limit) == int :
        if limit >= 0 :
            number = 0
            palindromeList = []
            while limit > 0 :
                if isPalindrome(number) :
                    palindromeList.append(number)
                    limit -= 1
                number += 1
            return palindromeList
        else :
            raise ValueError ('Limit must be positive or zero.')
    else :
        raise ValueError("Input is not a valid integer.")

def listPalindromeBetween(start, end) :
    if type(start) == int and type(end) == int :
        if end >= start :
            palindromeList = [number for number in range(start, end) if isPalindrome(number)]
        elif end < start :
            palindromeList = [number for number in range(start, end, -1) if isPalindrome(number)]
        return palindromeList
    else :
        raise ValueError("Input is not a valid integer.")