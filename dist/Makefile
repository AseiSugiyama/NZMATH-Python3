TMPDIR = /tmp/nzmath-build
PYTHON = python2.3
HTMLPY = /home/tetsushi/work/docutils/tools/rst2html.py
OLD_VER = 0.3.0
NEW_VER = 0.3.1

all: html sdist

sdist: files
	(cd $(TMPDIR); $(PYTHON) setup.py sdist)

html: files
	(cd $(TMPDIR); $(HTMLPY) README.txt | \
	 awk '/\(c\)/ {sub(/\(c\)/,"\\&copy;"); sub(/NZMATH/,"<font color=\"#FF0000\">N</font><font color=\"#FF8000\">Z</font><font color=\"#FFFF00\">M</font><font color=\"#00FF00\">A</font><font color=\"#0000FF\">T</font><font color=\"#FF00FF\">H</font>")} 1' > README.html)
	(cd $(TMPDIR); $(HTMLPY) tutorial.txt | \
	 awk '/\(c\)/ {sub(/\(c\)/,"\\&copy;"); sub(/NZMATH/,"<font color=\"#FF0000\">N</font><font color=\"#FF8000\">Z</font><font color=\"#FFFF00\">M</font><font color=\"#00FF00\">A</font><font color=\"#0000FF\">T</font><font color=\"#FF00FF\">H</font>")} 1' > tutorial.html)

files: clean
	mkdir -p $(TMPDIR)/nzmath
	cp *.txt setup.py MANIFEST.in $(TMPDIR)
	cp -p ../*.py $(TMPDIR)/nzmath
	cp -a ../factor $(TMPDIR)/nzmath/

clean:
	rm -fr $(TMPDIR)

tag:
	for i in `cat target.files`; do \
		echo cvs tag release-`echo $(NEW_VER) | sed -e 's/\./_/g'` $$i; \
	done
	@echo "Do the following also (until release 0.4.0 at least):"
	@echo "  cvs tag -rrelease-`echo $(OLD_VER) | sed -e 's/\./_/g'` release-`echo $(NEW_VER) | sed -e 's/\./_/g'` ../elliptic.py"
## equation should be ignored
