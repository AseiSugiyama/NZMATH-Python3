def trialDivision(n):
    factor =[]
    i=2
    if i**2 <= n:
        if n % i == 0:
            k=0
            while n % i == 0:
                n = n / i
                k = k+1
            factor.append((i,k))
    i=3
    while i**2 <= n:
        if n % i == 0:
            k=0
            while n % i == 0:
                n = n / i
                k = k+1
            factor.append((i,k))   
        i=i+2    
        if i>=7:
            j=0
            while i**2 <= n:
                if n % i == 0:
                    k=0
                    while n % i == 0:
                        n = n / i
                        k = k+1
                    factor.append((i,k))
                j=j+1
                if j%8==1:
                    i=i+4
                elif j%8==2:
                    i=i+2
                elif j%8==3:
                    i=i+4
                elif j%8==4:
                    i=i+2
                elif j%8==5:
                    i=i+4
                elif j%8==6:
                    i=i+6
                elif j%8==7:
                    i=i+2
                elif j%8==0:
                    i=i+6
    if n != 1:
        factor.append((n,1))
    return factor
