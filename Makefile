# Thanks to python-oauth2 for Makefile template
PYTHON      = $(shell test -x bin/python && echo bin/python || \
                      echo `which python`)
PYVERS      = $(shell $(PYTHON) -c 'import sys; print "%s.%s" % sys.version_info[0:2]')
VIRTUALENV  = $(shell /bin/echo -n `which virtualenv || \
                                    which virtualenv-$(PYVERS) || \
                                    which virtualenv$(PYVERS)`)
VIRTUALENV += --no-site-packages
PAGER      ?= less
COVERAGE    = $(shell test -x bin/coverage && echo bin/coverage || echo true)
SETUP       = $(PYTHON) ./setup.py
EZ_INSTALL  = $(SETUP) easy_install
PYLINT      = bin/pylint
PLATFORM    = $(shell $(PYTHON) -c "from pkg_resources import get_build_platform; print get_build_platform()")
OS         := $(shell uname)
EGG        := $(shell $(SETUP) --fullname)-py$(PYVERS).egg
SDIST      := $(shell $(SETUP) --fullname).tar.gs
SRCDIR     := librerpg
SOURCES    := $(shell find $(SRCDIR) -type f -name \*.py -not -name 'test_*')
TESTS      := $(shell find $(SRCDIR) -type f -name test_\*.py)
COVERED    := $(SOURCES)
ROOT        = $(shell pwd)
ROOTCMD     = fakeroot
BUILD_NUMBER ?= 1


.PHONY: test dev clean extraclean

all: egg
egg: dist/$(EGG)

dist/$(EGG):
	$(SETUP) bdist_egg

sdist:
	$(SETUP) sdist

test: bin/nosetests
	rm -f .coverage
	$(SETUP) test --with-coverage --cover-package=librerpg

xunit.xml: bin/nosetests $(SOURCES) $(TESTS)
	$(SETUP) test --with-xunit --xunit-file=$@

bin/nosetests: bin/easy_install
	@$(EZ_INSTALL) nose

coverage: .coverage
	@$(COVERAGE) html -d $@ $(COVERED)

coverage.xml: .coverage
	@$(COVERAGE) xml $(COVERED)

.coverage: $(SOURCES) $(TESTS) bin/coverage bin/nosetests
	-@$(COVERAGE) run $(SETUP) test

bin/coverage: bin/easy_install
	@$(EZ_INSTALL) coverage

profile: .profile bin/pyprof2html
	bin/pyprof2html -o $@ $<

.profile: $(SOURCES) bin/nosetests
	-$(SETUP) test -q --with-profile --profile-stats-file=$@

bin/pyprof2html: bin/easy_install bin/
	@$(EZ_INSTALL) pyprof2html

docs: $(SOURCES) bin/epydoc
	@echo bin/epydoc -q --html --no-frames -o $@ ...
	@bin/epydoc -q --html --no-frames -o $@ $(SOURCES)

bin/epydoc: bin/easy_install
	@$(EZ_INSTALL) epydoc

bin/pep8: bin/easy_install
	@$(EZ_INSTALL) pep8

pep8: bin/pep8
	@bin/pep8 --repeat --ignore E225 $(SRCDIR)

pep8.txt: bin/pep8
	@bin/pep8 --repeat --ignore E225 $(SRCDIR) > $@

lint: bin/pylint
	-$(PYLINT) -f colorized $(SRCDIR)

lint.html: bin/pylint
	-$(PYLINT) -f html $(SRCDIR) > $@

lint.txt: bin/pylint
	-$(PYLINT) -f parseable $(SRCDIR) > $@

bin/pylint: bin/easy_install
	@$(EZ_INSTALL) pylint

README.html: README.mkd | bin/markdown
	bin/markdown -e utf-8 $^ -f $@

bin/markdown: bin/easy_install
	@$(EZ_INSTALL) Markdown


# Development setup
rtfm:
	$(PAGER) README.mkd

tags: TAGS.gz

TAGS.gz: TAGS
	gzip $^

TAGS: $(SOURCES)
	ctags -eR .

env: bin/easy_install

bin/easy_install:
	$(VIRTUALENV) .

dev: develop
develop: env
	nice -n 20 $(SETUP) develop
	@echo "            ---------------------------------------------"
	@echo "            To activate the development environment, run:"
	@echo "                           . bin/activate"
	@echo "            ---------------------------------------------"

clean:
clean:
	find . -type f -name \*.pyc -exec rm {} \;
	rm -rf build dist TAGS TAGS.gz digg.egg-info tmp .coverage \
	       coverage coverage.xml docs lint.html lint.txt profile \
	       .profile *.egg *.egg-info xunit.xml

xclean: extraclean
extraclean: clean
	rm -rf bin lib .Python include

