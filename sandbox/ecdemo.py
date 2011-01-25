"""
elliptic curve demo script for nzmath & matplotlib
After running this script, it draws k-scaler multiplication of points in E(F_p).
"""

import nzmath.elliptic
from pylab import *

p = 37
A = 1 # A>0
B = 2 # B>0

E = nzmath.elliptic.ECoverFp([A, B], p)
while True:
    P = E.point()
    if E.pointorder(P) > E.order()//3:
        break

x_y = []
for i in range(E.pointorder(P)):
    pnt = E.mul(i, P)
    if len(pnt) > 1: # not point at infinity
        if pnt[1] > p//2:
            ele = [ [pnt[0]], [pnt[1] - p] ]
        else:
            ele = [ [pnt[0]], [pnt[1]] ]
        if i==1:
            x_y.append(ele + ["P"])
        else:
            x_y.append(ele + [str(i) + "P"])

figure()
grid(True)
axis([-p//2, p//2 + 1, 0, p])
xlabel("X")
ylabel("Y", rotation=0)

#title_str="$E(F_{" + str(p) +"}):\ y^2=x^3+"
#if A!=1:
#    title_str += str(A)
#title_str += "x+" + str(B) + "$"
#title(title_str)

for x, y, lab in x_y:
    plot(x, y, 'o')
    text(x[0], y[0], lab, size=15, weight='bold')
show()
#savefig('ecdemo_fig') # for not GUI environment
