TMPDIR = /tmp/nzmath-build
PYTHON = python2.3
HTMLPY = /home/tetsushi/work/docutils/tools/html.py

all: html sdist

sdist: files
	(cd $(TMPDIR); $(PYTHON) setup.py sdist)

html: files
	(cd $(TMPDIR); $(HTMLPY) README.txt | sed 's/&amp;copy;/\&copy;/' > README.html)

files: clean
	mkdir -p $(TMPDIR)/nzmath
	cp *.txt setup.py MANIFEST.in $(TMPDIR)
	cp -p ../*.py $(TMPDIR)/nzmath

clean:
	rm -fr $(TMPDIR)
