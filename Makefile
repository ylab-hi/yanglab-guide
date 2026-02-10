# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= uv run sphinx-build
SPHINXAUTOBUILD ?= uv run sphinx-autobuild
PYTHON        ?= uv run python
NOX           ?= uv run nox
SOURCEDIR     = source
BUILDDIR      = source/_build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Install dependencies using uv
install:
	uv sync --all-extras

# Build documentation using nox
docs:
	$(NOX) --force-color --session=docs

# Build and serve documentation with auto-reload
auto:
	$(SPHINXAUTOBUILD) --open-browser "$(SOURCEDIR)" "$(BUILDDIR)"

# Check documentation links
linkcheck:
	$(NOX) --force-color --session=linkcheck

# Generate covers
covers:
	$(PYTHON) ./utils.py

# Clean build directory
clean:
	rm -rf $(BUILDDIR)
	rm -rf .nox

# Development setup
setup: install
	@echo "Development environment ready!"
	@echo "Run 'make docs' to build documentation"
	@echo "Run 'make auto' to build and serve with auto-reload"

.PHONY: help install docs auto linkcheck covers clean setup Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
