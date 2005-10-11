import nzmath.matrix as matrix
import nzmath.vector as vector
import nzmath.gcd as gcd

def modss(vect,mod): #self __mod__
    V=[]
    for i in range(len(vect)):
        V.append((vect[i+1].__int__() % mod.__int__()))
    return vector.Vector(V)

def mods(matrix,mod): #self __mod__
    M=matrix
    for i in range(M.row):
            M[i]=modss(M[i],mod)
    return M


def smith(mtr):

    n=mtr.row
    if(mtr.row!=mtr.column):
        raise ValueError,"not square matrix"
    M=mtr

    R=M.determinant().__int__()
    if(R<0):
      R=-R
    lst=[]

    while (n!=1):
        j=n
        c=0
        while(j!=1):
            j=j-1
            if(M[n,j]!=0):
                u,v,d= gcd.extgcd(M[n,n],M[n,j])
                B=u*M.getColumn(n)+v*M.getColumn(j)
                M.setColumn(j,modss(((M[n,n]//d)*M.getColumn(j)-(M[n,j]//d)*M.getColumn(n)),R))
                M.setColumn(n,modss(B,R))

        j=n
        while(j!=1):
            j=j-1
            if(M[j,n]!=0):
                u,v,d= gcd.extgcd(M[n,n],M[j,n])
                B=u*M.getRow(n)+v*M.getRow(j)
                M.setRow(j,modss(((M[n,n]//d)*M.getRow(j)-(M[j,n]//d)*M.getRow(n)),R))
                M.setRow(n,modss(B,R))
                c=c+1

        if(c<=0):
            b=M[n,n].__int__()
            flag=False
            for k in range(1,n):
                for l in range(1,n):
                    if((M[k,l] % b) !=0):
                        M.setRow(n,M.getRow(n)+M.getRow(k))
                        flag=True

            if(flag==False):
                dd=gcd.gcd(M[n,n],R)
                lst.append(dd)
                R=(R//dd)
                n=n-1

    dd=gcd.gcd(M[1,1],R)
    lst.append(dd)
    lst.reverse()
    return lst
