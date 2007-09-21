TMPDIR = /tmp/nzmath-build
PYTHON = python2.3
HTMLPY = $(PYTHON) rst2html.py
OLD_VER = 0.6.0
NEW_VER = 0.7.0_beta0

all: html sdist

sdist: files setup.py
	(cd $(TMPDIR); $(PYTHON) setup.py sdist)

setup.py: files
	(cd $(TMPDIR); ls -R manual/ | awk -f makesetuppy.awk $(NEW_VER) > setup.py)

html: files
	(cd $(TMPDIR); $(HTMLPY) README.txt | \
	 awk '/\(c\)/ {sub(/\(c\)/,"\\&copy;"); sub(/NZMATH/,"<font color=\"#FF0000\">N</font><font color=\"#FF8000\">Z</font><font color=\"#FFFF00\">M</font><font color=\"#00FF00\">A</font><font color=\"#0000FF\">T</font><font color=\"#FF00FF\">H</font>")} 1' > README.html)
	(cd $(TMPDIR); $(HTMLPY) tutorial.txt | \
	 awk '/\(c\)/ {sub(/\(c\)/,"\\&copy;"); sub(/NZMATH/,"<font color=\"#FF0000\">N</font><font color=\"#FF8000\">Z</font><font color=\"#FFFF00\">M</font><font color=\"#00FF00\">A</font><font color=\"#0000FF\">T</font><font color=\"#FF00FF\">H</font>")} 1' > tutorial.html)

files: clean
	mkdir -p $(TMPDIR)/nzmath
	cp *.txt MANIFEST.in makesetuppy.awk rst2html.py $(TMPDIR)
	cp -a ../manual $(TMPDIR)
	cp -p ../*.py $(TMPDIR)/nzmath
	cp -a ../factor $(TMPDIR)/nzmath/
	cp -a ../poly $(TMPDIR)/nzmath/

clean:
	rm -fr $(TMPDIR)

tag:
	for i in `cat target.files`; do \
		echo cvs tag release-`echo $(NEW_VER) | sed -e 's/\./_/g'` $$i; \
	done

version:
	sed -i -e 's/$(OLD_VER)/$(NEW_VER)/g' README.txt
