TMPDIR = /tmp/nzmath-build
PYTHON = python2.6
WIN_PYTHON = /cygdrive/c/Python27/python
HTMLPY = $(PYTHON) rst2html.py
OLD_VER = 1.1.0
NEW_VER = 1.2.0

all: html sdist zip wininst
unix: rpm
win: build_win32 build_win64

sdist: files setup.py
	(cd $(TMPDIR); $(PYTHON) setup.py sdist --formats=gztar)

zip: files setup.py
	(cd $(TMPDIR); $(PYTHON) setup.py sdist --formats=zip)

rpm: files setup.py
	(cd $(TMPDIR); $(PYTHON) setup.py bdist_rpm; mv build build_rpm)

wininst: files setup.py
	(cd $(TMPDIR); $(PYTHON) setup.py bdist_wininst --user-access-control=auto; mv build build_wininst)
	for i in $(TMPDIR)/dist_wininst/*; do\
		chmod 755 $$i; \
		mv $$i `echo $$i | sed 's/.exe/Install.exe/'`; \
	done

build_win32: files setup.py
	(cd $(TMPDIR); $(WIN_PYTHON) setup.py build --plat-name=win32 bdist_wininst --user-access-control=auto; mv build build_wininst32)
	for i in $(TMPDIR)/dist_wininst/*; do\
		chmod 755 $$i; \
		mv $$i `echo $$i | sed 's/.exe/Install.exe/'`; \
	done

build_win64: files setup.py
	(cd $(TMPDIR); $(WIN_PYTHON) setup.py build --plat-name=win-amd64 bdist_wininst --user-access-control=auto; mv build build_wininst64)
	for i in $(TMPDIR)/dist_wininst/*; do\
		chmod 755 $$i; \
		mv $$i `echo $$i | sed 's/.exe/Install.exe/'`; \
		mv $$i `echo $$i | sed 's/win-amd64/win64/'`; \
	done

setup.py: files
	(cd $(TMPDIR); ls -R manual | awk -f makesetuppy.awk $(NEW_VER) > setup.py)

html: files
	(cd $(TMPDIR); $(HTMLPY) README.txt | \
	 awk '/\(c\)/ {sub(/\(c\)/,"\\&copy;"); sub(/NZMATH/,"<font color=\"#FF0000\">N</font><font color=\"#FF8000\">Z</font><font color=\"#FFFF00\">M</font><font color=\"#00FF00\">A</font><font color=\"#0000FF\">T</font><font color=\"#FF00FF\">H</font>")} 1' > README.html)
	(cd $(TMPDIR); $(HTMLPY) tutorial.txt | \
	 awk '/\(c\)/ {sub(/\(c\)/,"\\&copy;"); sub(/NZMATH/,"<font color=\"#FF0000\">N</font><font color=\"#FF8000\">Z</font><font color=\"#FFFF00\">M</font><font color=\"#00FF00\">A</font><font color=\"#0000FF\">T</font><font color=\"#FF00FF\">H</font>")} 1' > tutorial.html)

files: clean
	mkdir -p $(TMPDIR)/manual/
	mkdir -p $(TMPDIR)/manual/ja
	mkdir -p $(TMPDIR)/manual/en
	cp *.txt MANIFEST.in makesetuppy.awk rst2html.py \
		logo.bmp setup.cfg nzmathconf.py.example $(TMPDIR)
	cp -a data $(TMPDIR)
	cp -p ../manual/ja/*.pdf $(TMPDIR)/manual/ja
	cp -p ../manual/en/*.pdf $(TMPDIR)/manual/en
	cp -a ../nzmath $(TMPDIR)

clean:
	rm -fr $(TMPDIR)

#tag:
#	for i in `cat target.files`; do \
#		echo hg tag release-`echo $(NEW_VER) | sed -e 's/\./_/g'` $$i; \
#	done

version:
	sed -i -e 's/$(OLD_VER)/$(NEW_VER)/g' README.txt
