NZMATH 0.1.0
============

Introduction
------------

NZMATH is a Python based number theory oriented calculation system.
It is developed at Tokyo Metropolitan University.

The version 0.1.0 is a minor bug fix release.
It is still on very early stage of development, and it should be
considered as an alpha quality product.

Installation
------------

To install NZMATH on your computer, you must have Python 2.3 or
better.  The latest release 2.3.2 is recommended.  If you don't have a
copy of Python, please install it first.  Python is available from
http://www.python.org/ .

The next step is to expand the NZMATH-0.1.0.tar.gz.  The way to do it
depends on your operating system.  On the systems with GNU tar, you can
do it with a single command::

 $ tar zxf NZMATH-0.1.0.tar.gz

where, $ is the command line prompt.  Or with standard tar, you can do
it as::

 $ gzip -cd NZMATH-0.1.0.tar.gz | tar xf -

Then, you have a child directory named NZMATH-0.1.0.

The third step is the last step, to install NZMATH to the standard
python path. Usually, this means to write files to somewhere under
/usr/lib or /usr/local/lib, and thus you have to have appropriate
write permission.  Typically, do as the following::

 $ cd NZMATH-0.1.0
 $ su
 # python setup.py install


Usage
-----

NZMATH is provided as a Python library package named 'nzmath', so
please use it as a usual package.  For more information please refer
"Tutorial" (*NOT YET AVAILABLE*).


Feedback
--------

Your feedbacks are always welcomed.  Please consider to join the
mailing list nzmath-user@tnt.math.metro-u.ac.jp.  You can join the
list with writing a mail containing a line of "subscribe" in the body
to nzmath-user-request@tnt.math.metro-u.ac.jp.  *Be careful* not to
send it to nzmath-user.


Copyright
---------

&copy; 2003-2004 NZMATH development group, all right reserved.
