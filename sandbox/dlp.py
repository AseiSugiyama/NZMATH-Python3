"""
DLP --- discrete logarithm problem

DLP for Finite Field.
"""
from __future__ import division
import nzmath.arith1 as arith1
import nzmath.factor.misc as factor_misc


def SilverPohligHellman(target, base, p):
    """
    Silver-Pohlig-Hellman method of DLP for finite prime fields.

    x, the discrete log of target, can be determined for each prime
    power factor of p - 1 (passed through factored_order):
      x = \sum s_j p_i**j mod p_i**e (0 <= s_j < p_i)

    Lidl, Niederreiter, 'Intro. to finite fields and their
    appl.' (revised ed) pp.356 (1994) CUP.
    """
    log_mod_factor = {}
    order = p - 1
    factored_order = factor_misc.FactoredInteger(order)
    base_inverse = arith1.inverse(base, p)
    for p_i, e in factored_order:
        log_mod_factor[p_i] = 0
        smallorder = order
        modtarget = target
        primitive_root_of_unity = pow(base, order // p_i, p)
        p_i_power = 1
        for j in range(e):
            smallorder //= p_i
            targetpow = pow(modtarget, smallorder, p)
            if targetpow == 1:
                s_j = 0
            else:
                root_of_unity = primitive_root_of_unity
                for k in range(1, p_i):
                    if targetpow == root_of_unity:
                        s_j = k
                        break
                    root_of_unity = root_of_unity * primitive_root_of_unity % p
                log_mod_factor[p_i] += s_j * p_i_power
            modtarget = modtarget * pow(base_inverse, s_j * p_i_power, p) % p
            p_i_power *= p_i
        if p_i < p_i_power:
            log_mod_factor[p_i_power] = log_mod_factor[p_i]
            del log_mod_factor[p_i]

    if len(log_mod_factor) == 1:
        return log_mod_factor.values()[0]
    return arith1.CRT([(r, p) for (p, r) in log_mod_factor.items()])
