import factor.trialdivision 

def euler(n):                    
    """
    This program returns Eulernumber for n
    """
    f = factor.trialdivision.trialDivision(n)
    p = 1
    for f0, f1 in f:
        p *=pow(f0,f1-1)*(f0-1)
    return p

def moebius(n):
    """
    This program returns Moebius function for n
    """
    f = factor.trialDivision(n)
    i=0
    while i < len(f):
        g=f[i]
        if g[1]>1:
            return 0
        i=i+1
    return pow(-1,len(f))

