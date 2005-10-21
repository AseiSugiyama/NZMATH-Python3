from distutils.core import setup

setup (
    name = "NZMATH",
    version = "0.4.1",
    url = "http://tnt.math.metro-u.ac.jp/nzmath/",
    author = "NZMATH development group",
    author_email = "nzmath-user@tnt.math.metro-u.ac.jp",
    description = "number theory oriented calculation system",

    packages = ["nzmath", "nzmath.factor"] )
