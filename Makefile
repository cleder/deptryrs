.PHONY: docs docs-clean

SPHINXBUILD = sphinx-build
SOURCEDIR   = docs
BUILDDIR    = docs/_build

docs:
	$(SPHINXBUILD) -W -b html $(SOURCEDIR) $(BUILDDIR)/html

docs-clean:
	rm -rf $(BUILDDIR)
