"""
=====================
Test installed NZMATH
=====================

To test installed NZMATH is one of the purpose of the test package.
Be sure that the versions of test and main distribution match.
Otherwise, some tests may fail.

Running testAll.py from the test directory:
 % python testAll.py
tests all the NZMATH modules.

Instead of testAll.py, running testArith1.py, for example:
 % python testArith1.py
tests only the nzmath.arith1 module.

========================
Test before installation
========================

Another usage is to test NZMATH before its installation: just before
the installation or during development. Since the path where the main
package resides is probably not known to python interpreter, the first
task is to set PYTHONPATH environment variable to the parent directory
of 'nzmath' directory.

The rest of the process is same as above.

=========
Copyright
=========

The package is a part of NZMATH, and is distributed under the BSD
license.  See LICENSE.txt for detail.
"""
