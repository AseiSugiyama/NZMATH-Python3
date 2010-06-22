TMPDIR = /tmp/nzmath-build
PYTHON = python2.5
HTMLPY = $(PYTHON) rst2html.py
OLD_VER = 0.92.0
NEW_VER = 1.0.1

all: html sdist zip wininst

sdist: files setup.py
	(cd $(TMPDIR); $(PYTHON) setup.py sdist)

zip: files setup.py
	(cd $(TMPDIR); $(PYTHON) setup.py sdist --formats=zip)

wininst: files setup.py
	(cd $(TMPDIR); $(PYTHON) setup.py bdist_wininst; mv build build_wininst)
	for i in $(TMPDIR)/dist_wininst/*; do\
		chmod 755 $$i; \
		mv $$i `echo $$i | sed 's/.exe/Install.exe/'`; \
	done

setup.py: files
	(cd $(TMPDIR); ls -R manual | awk -f makesetuppy.awk $(NEW_VER) > setup.py)

html: files
	(cd $(TMPDIR); $(HTMLPY) README.txt | \
	 awk '/\(c\)/ {sub(/\(c\)/,"\\&copy;"); sub(/NZMATH/,"<font color=\"#FF0000\">N</font><font color=\"#FF8000\">Z</font><font color=\"#FFFF00\">M</font><font color=\"#00FF00\">A</font><font color=\"#0000FF\">T</font><font color=\"#FF00FF\">H</font>")} 1' > README.html)
	(cd $(TMPDIR); $(HTMLPY) tutorial.txt | \
	 awk '/\(c\)/ {sub(/\(c\)/,"\\&copy;"); sub(/NZMATH/,"<font color=\"#FF0000\">N</font><font color=\"#FF8000\">Z</font><font color=\"#FFFF00\">M</font><font color=\"#00FF00\">A</font><font color=\"#0000FF\">T</font><font color=\"#FF00FF\">H</font>")} 1' > tutorial.html)

files: clean
	mkdir -p $(TMPDIR)/manual
	cp *.txt MANIFEST.in makesetuppy.awk rst2html.py \
		logo.bmp setup.cfg nzmathconf.py.example $(TMPDIR)
	cp -a data $(TMPDIR)
	cp -p ../manual/*.pdf $(TMPDIR)/manual
	cp -a ../nzmath $(TMPDIR)

clean:
	rm -fr $(TMPDIR)

#tag:
#	for i in `cat target.files`; do \
#		echo hg tag release-`echo $(NEW_VER) | sed -e 's/\./_/g'` $$i; \
#	done

version:
	sed -i -e 's/$(OLD_VER)/$(NEW_VER)/g' README.txt
