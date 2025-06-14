#checks if two numbers have a common divisor
def CheckCD(a, b):
    if a != 1 and b != 1:
        a = abs(a)
        b = abs(b)

        min_val = min(a, b)
        for i in range(2, min_val + 1):
            if a % i == 0 and b % i == 0:
                return True
    return False

#finds the greatest common divisor of two numbers (assuming they have a common divisor)
def GCD(n1, n2):
    n1 = abs(n1) 
    n2 = abs(n2) 
    
    def FindFactors(num):
        arr = []
        for i in range(2, num):
            if num % i == 0:
                arr.append(i)
        return arr

    n1factors = FindFactors(n1)
    n2factors = FindFactors(n2)
    arrA = n1factors if len(n1factors) < len(n2factors) else n2factors
    arrB = n1factors if arrA == n2factors else n2factors
    for i in arrA:
        if i in arrB:
            return i    

#reduces fractions to simplified form
def FracRed(frac):
    n = int(frac.split("/")[0])
    d = int(frac.split("/")[1]) 

    if n % d == 0:
        return str(int(n / d)) + "/1"
    elif d == 1 or not CheckCD(n, d):
        return frac
    elif CheckCD(n, d):
        gcd = GCD(n, d)
        n = int(n / gcd)
        d = int(d / gcd)

        return str(n) + "/" + str(d)

#formats a polynomial arr with x variables and exponents
def Simplify(arr):
    pop = []
    for i in range(len(arr)):
        n = int(arr[i].split("/")[0])
        d = int(arr[i].split("/")[1])
        deg = len(arr) - (i + 1)

        if deg > 1:
            x = f"x^{deg}"
        elif deg == 1:
            x = "x"
        elif deg == 0:
            x = ""

        if n == 1 and d == 1:
            if deg == 0:
                message = "1"
            else:
                message = x
        elif n != 1 and d == 1:
            message = str(n) + x
        else:
            message = arr[i] + x
        

        if i == 0:
            arr[i] = message
        else:
            if n < 0:
                arr[i] = " - " + message[1:len(message)]
            elif n > 0:
                arr[i] = " + " + message
            elif n == 0:
                pop.append(i)
                arr[i] = " + " + message
    
    for i in range(len(pop)):
        if len(pop) > 0:
            arr.pop(pop[i])

    return "".join(arr)

#responsible for obtaining user input for the coefficients of each polynomial and returning a table of coefficients
#the coefficients will ALWAYS pass as strings; they will not be converted to integers until subtraction is needed between the minuend and the subtrahend
def CoeffsArray(deg):
    coeffs = []
    for i in range(deg + 1):
        term = "x^" + str(deg - i) + ": "
        if i == deg:
            term = "c: "
        
        #each coefficient is converted into a fraction to handle fraction coefficients
        inpt = input(term)
        if "/" in inpt:
            coeffs.append(FracRed(inpt))
        else:
            coeffs.append(inpt + "/1")
    
    return coeffs

#sets the degree of the dividend and initializes an array of its coefficients
degDvd = int(input("Degree Dividend: "))
dvdCoeffs = CoeffsArray(degDvd)

print("")

#sets the degree of the divisor and initializes an array of its coefficients
degDvs = int(input("Degree Divisor: "))
dvsCoeffs = CoeffsArray(degDvs)

#initializes the initial minuend coefficient sequence as a table
minCoeffs = [] 
for i in range(len(dvsCoeffs)):
    minCoeffs.append(dvdCoeffs[i])

#calculates the coefficient (assigned to variable a) of the term i (assigned to variable index) of the quotient polynomial for each iteration of the synthetic division
quotient = []
r = ""
for i in range(degDvd - degDvs + 1):
    index = degDvd - degDvs
    n1 = minCoeffs[0].split("/")[0] #numerator of first term of minuend
    d2 = dvsCoeffs[0].split("/")[1] #denominator of first term of divisor
    d1 = minCoeffs[0].split("/")[1] #denominator of first term of minuend
    n2 = dvsCoeffs[0].split("/")[0] #numerator of first term of divisor
    a = FracRed(str(int(n1) * int(d2)) + "/" + str(int(d1) * int(n2)))
    quotient.append(a)

    #initializes the subtrahend coefficient sequence for each iteration
    subCoeffs = []
    for j in range(len(dvsCoeffs)):
        numA = int(a.split("/")[0]) 
        numDvs = int(dvsCoeffs[j].split("/")[0]) 
        denA = int(a.split("/")[1]) 
        denDvs = int(dvsCoeffs[j].split("/")[1]) 

        product = str(numA * numDvs) + "/" + str(denA * denDvs)
        subCoeffs.append(FracRed(product))

    #subtracts the subtrahend coefficients from the minuend coefficients
    for j in range(len(minCoeffs)):
        dmin = int(minCoeffs[j].split("/")[1])
        dsub = int(subCoeffs[j].split("/")[1])
        
        if dmin != dsub:
            nmin = dsub * int(minCoeffs[j].split("/")[0])
            nsub = dmin * int(subCoeffs[j].split("/")[0])
            dboth = dmin * dsub

            print(str(nmin - nsub) + "/" + str(dboth))
            minCoeffs[j] = FracRed(str(nmin - nsub) + "/" + str(dboth))
        elif dmin == dsub:
            nmin = int(minCoeffs[j].split("/")[0])
            nsub = int(subCoeffs[j].split("/")[0])

            print(str(nmin - nsub) + "/" + str(dmin))
            minCoeffs[j] = FracRed(str(nmin - nsub) + "/" + str(dmin))

    #removes the zero from the minuend and adds the next term from the dividend
    minCoeffs.pop(0)
    if not (i == degDvd - degDvs):
        minCoeffs.append(dvdCoeffs[len(dvsCoeffs) + i])

print("Quotient: " + Simplify(quotient))

#formats the remainder
divisor = Simplify(dvsCoeffs)
remainder = Simplify(minCoeffs)
r = f"({remainder}) / ({divisor})" if remainder != "0" else "0"

print("Remainder: " + r)