======
README
======


Sandbox modules are experimental implementations for future NZMATH.
The following descriptions of each module will be updated by each
authors.  The modules followed by an asterisk are already in the
nzmath package.

modules
=======

__init__
--------
It's just a module for making the sandbox directory a Python package.
(mft)

_profile_finitefield
--------------------
profiling finitefield
(salt3des)

abstset
-------
(programming) object for set, group, etc.
(naoki_lab)

algebraicessence
----------------
(salt3des)

algorithm
---------
Abstract (higher order) functions
(mft, naoki_lab)

analytic
--------
A collection of analytic number theory related functions.
(mft)

cardinal
--------
Cardinal numbers
(mft)

cartesian
---------
A module provides cartesian product (of rings).
(mft)

cf
--
A module for continued fractions.
(mft)

chainop
-------
A module for abstract chains of operations, like binary powerings.
(mft)

cyclicgroup
-----------
Abstract Cyclic Group structure provided module.
(salt3des)

declarativegroup
----------------
Group by declaration.  Some kind of structures is treated as a group
by declaring it is a group.
(mft)

dlp
---
DLP(discrete logarithm problem) for finite field, which provides the
Silver-Pohlig-Hellman algorithm.
(mft)

ecdemo
------
elliptic curve demo script for nzmath & matplotlib
After running this script, it draws k-scaler multiplication of points in E(F_p).
(naoki_labo)

elliptic *
----------

ffextension
-----------
Extention of FiniteExtendedField .
(salt3des)

finitefield
-----------
A replacement for nzmath.finitefield (using poly).
(mft, salt3des)

fraction
--------
ring of fractions
(mft)

gftools
-------
gftools.py - efficiently interpreter tools for Galois fields.
function symbols starting with ``u_'' means ``unstable'', use sandbox version
of finitefield (module sandbox.finitefield).
(salt3des)

group
-----
Abstract Group structure provided module.
Support Group-like Properties.
(salt3des)

grouplikeset
------------
Abstract Group-like structure provided module.
Support Group-like Properties.
(salt3des)

hddb
----
DB for class numbers of imaginary quadratic fields.
(mft)

homo
----
A replacement of nzmath.ring, aimed to provide homomorphism, etc.
(mft)

linrec
------
Linearly Recurrent Sequence
(mft)

module
------
module, ideal etc. for number field
(naoki_labo)

padic
-----
p-adic numbers and their rings / fields.
(mft)

powdetect
---------
perfect power detection fuction
(mft)

powering
--------
For sample powering(or scalar multiplication in additive group) method.
You shouldn't use directly, but choose the proper method and take in your module as __pow__(multiplicative group) or __mul__(additive group).
(It should be taken in module such as algebraicessence.py or group.py.)
(naoki_labo)

pyexprfield
-----------
Python Expression field, another finite prime field characteristic two
definition.  field element is defined by bool(Python Expression).
This module is reference design for finite field characteristic two.
but I recommend that this field should be used only checking Python syntax.
(salt3des)

rewrite
-------
String rewrite systems.
(mft)

symbol
------
define short symbols (for user friendly initialization)
(naoki_labo)

ternary
-------
Ternary logic.
(mft)


algebraiccurve
==============
(salt3des)

algebraiccurve.elliptic
-----------------------
New implementation of nzmath.elliptic using nzmath.poly.

algebraiccurve._sup_elliptic
----------------------------
support modules of elliptic curves. (private)


poly
====
A new implementation of polynomials.

poly.factor_work
----------------
factor
(salt3des)

poly.irreducible
----------------
tests for irreducibility of integer coefficient polynomials.
(mft)

poly.semigroupalgebra
---------------------
Semigroup algebra is a kind of generalization to polynomial.
(mft)
