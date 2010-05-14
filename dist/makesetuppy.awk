# Make setup.py the install script
#
# usage:
# % ls -R manual | awk -f makesetuppy.awk VERSION

BEGIN {
    version = ARGV[1];
    ARGV[1] = "";
    openbracket = 0;

    print "from distutils.core import setup";
    print "import glob";
    print "";
    print "version = '" version "'";
    print "doc_prefix = 'doc/NZMATH-%s/' % version";
    print "data_prefix = 'nzmath/'";
    print "";

    print "setup(";
    print "    name='NZMATH',";
    print "    version=version,";
    print "    url='http://tnt.math.metro-u.ac.jp/nzmath/',";
    print "    author='NZMATH development group',";
    print "    author_email='nzmath-user@tnt.math.metro-u.ac.jp',";
    print "    description='number theory oriented calculation system',";
#    print "    classifiers=['Development Status :: 4 - Beta',";
    print "    classifiers=['Development Status :: 5 - Production/Stable',";
    print "                 'License :: OSI Approved :: BSD License',";
    print "                 'Operating System :: OS Independent',";
    print "                 'Programming Language :: Python',";
    print "                 'Topic :: Scientific/Engineering :: Mathematics',";
    print "                ],";
    print "";
    print "    packages=['nzmath', 'nzmath.factor', 'nzmath.poly', 'nzmath.plugin', 'nzmath.plugin.math'],";
    print "";
#    print "    data_files=["
#    print "        (data_prefix, ['data/discriminant.csv']),";
#    print "        (doc_prefix + 'manual',";
#    print "            ['manual/default.css'] + glob.glob('manual/*.html')),";
#    print "        (doc_prefix + 'manual/modules',";
#    print "            glob.glob('manual/modules/*.html')),";
#    print "    ]";
     print "    data_files=["
     print "        (data_prefix, ['data/discriminant.csv']),";
     print "        (doc_prefix + 'manual',";
     print "            glob.glob('manual/*.pdf')),";
     print "    ]";
    print ")";
}
