def listFibonacci(limit) :
    if type(limit) == int :
        if limit > 0 :
            fibonacciList = [0, 1]
            if limit < 3 :
                return fibonacciList[:limit]
            else :
                for i in range(limit-2) :
                    fibonacciList.append(fibonacciList[i] + fibonacciList[i+1])
                return fibonacciList
        else :
            raise ValueError('Limit must be positive or zero.')
    else :
        raise ValueError("Input is not a valid integer.")