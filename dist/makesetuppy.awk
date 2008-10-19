# Make setup.py the install script
#
# usage:
# % ls -R manual | awk -f makesetuppy.awk VERSION

BEGIN {
    version = ARGV[1];
    ARGV[1] = "";
    openbracket = 0;

    print "from distutils.core import setup";
    print "";
    print "doc_prefix = 'share/doc/NZMATH-" version "/'";
    print "";

    print "setup (";
    print "    name = 'NZMATH',";
    print "    version = '" version "',";
    print "    url = 'http://tnt.math.metro-u.ac.jp/nzmath/',";
    print "    author = 'NZMATH development group',";
    print "    author_email = 'nzmath-user@tnt.math.metro-u.ac.jp',";
    print "    description = 'number theory oriented calculation system',";
    print "    classifiers = ['Development Status :: 4 - Beta',";
    print "                   'License :: OSI Approved :: BSD License',";
    print "                   'Operating System :: OS Independent',";
    print "                   'Programming Language :: Python',";
    print "                   'Topic :: Scientific/Engineering :: Mathematics',";
    print "                  ],";
    print "";
    print "    packages = ['nzmath', 'nzmath.factor', 'nzmath.poly'],";
    print "";
    print "    data_files = ["
}
/:/ {
    directory = substr($0, 1, length($0) - 1);
    if(directory !~ /CVS$/) {
	print "        (doc_prefix + '" directory "', [";
	cont = 0;
	openbracket = openbracket + 1;
    }
}
/(css|html)$/ {
    print "         '" directory "/" $0 "',";
}
/^$/ && !cont {
    print "        ]),";
    cont = 1;
    openbracket = openbracket - 1;
}
END {
    for(i = openbracket; i > 0; i = i - 1) {
	print "        ]),";
    }
    print "    ]";
    print ")";
}
