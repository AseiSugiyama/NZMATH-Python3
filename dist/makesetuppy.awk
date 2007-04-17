# Make setup.py the install script
#
# usage:
# % ls -R manual/ | awk -f makesetuppy.awk VERSION

BEGIN {
    version = ARGV[1];
    ARGV[1] = "";

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
    print "";
    print "    packages = ['nzmath', 'nzmath.factor'],";
    print "";
    print "    data_files = ["
}
/:/ {
    directory = substr($0, 1, length($0) - 1);
    if(directory !~ /CVS$/) {
	print "        (doc_prefix + '" directory "', [";
	cont = 0;
    }
}
/(css|html)$/ {
    print "         '" directory "/" $0 "',";
}
/^$/ && !cont{
    print "        ]),";
    cont = 1;
}
END {
    print "        ]),";
    print "    ]";
    print ")";
}
