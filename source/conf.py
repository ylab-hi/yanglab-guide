# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


import random

# -- Project information -----------------------------------------------------
from datetime import datetime
from pathlib import Path
from textwrap import dedent

import yaml
from sphinx.application import Sphinx
from sphinx.util import logging

LOGGER = logging.getLogger("conf")

project = "yanglab-guide"
author = "Yangang Li"
copyright = f"{datetime.now().year}, yanglab"

# The full version, including alpha/beta/rc tags
release = "1.0"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    # "sphinx_tabs.tabs",
    "sphinx_thebe",
    "sphinx_togglebutton",
    "sphinxcontrib.bibtex",
    "sphinxcontrib.youtube",
    "sphinxext.opengraph",
]

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

intersphinx_mapping = {
    "mypy": ("https://mypy.readthedocs.io/en/stable/", None),
    "python": ("https://docs.python.org/3.8", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}
source_suffix = [".rst", ".md"]
language = "en"
linkcheck_ignore = [
    "codeofconduct.html",
]
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"
html_title = "Lab Guide For Yang Lab"
html_copy_source = True
html_theme_options = {
    "repository_url": "https://github.com/ylab-hi/yanglab-guide",
    "use_repository_button": True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_logo = "_static/logo.png"

html_theme_options = {
    "path_to_docs": "source",
    "repository_url": "https://github.com/ylab-hi/yanglab-guide",
    # "repository_branch": "gh-pages",  # For testing
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "colab_url": "https://colab.research.google.com/",
        "deepnote_url": "https://deepnote.com/",
        "notebook_interface": "jupyterlab",
        "thebe": True,
        # "jupyterhub_url": "https://datahub.berkeley.edu",  # For testing
    },
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
    "use_download_button": True,
    # "logo_only": True,
    "show_toc_level": 2,
    # "announcement": (
    #     "⚠️The Lab Guide of Yang Lab, "
    #     "so double-check your custom CSS rules!⚠️"
    # ),
    # For testing
    # "use_fullscreen_button": False,
    # "home_page_in_toc": True,
    # "single_page": True,
    # "extra_footer": "<a href='https://google.com'>Test</a>",  # DEPRECATED KEY
    # "extra_navbar": "<a href='https://google.com'>Test</a>",
    # "show_navbar_depth": 2,
}

bibtex_bibfiles = ["references.bib"]

GITHUB_URL = "https://raw.githubusercontent.com/ylab-hi/yanglab-guide/main"


def get_img_path(name: str):
    """Get the correct source directory for the gallery."""
    static_path = Path(f"_static/covers/{name.replace(' ', '_')}.jpg")
    remote_image_path = f"{GITHUB_URL}/source/{static_path}"

    if Path("source").exists():
        local_image_path = Path(f"source/{static_path}")
    else:
        local_image_path = static_path

    return local_image_path, remote_image_path


def get_cover_images(items):
    default_cover = "https://raw.githubusercontent.com/ylab-hi/yanglab-guide/main/source/_static/book.jpg"
    for item in items:
        local_image_path, remote_image_path = get_img_path(item["name"])
        if not local_image_path.exists():
            LOGGER.info(f"Cover image {local_image_path} does not exist")
            item["image"] = default_cover
        else:
            item["image"] = remote_image_path


def build_gallery(app: Sphinx):
    # Build the gallery file
    LOGGER.info("building gallery...")
    LOGGER.info(f"current working directory: {Path.cwd()}")
    star = "⭐"
    grid_items = []
    books = yaml.safe_load((Path(app.srcdir) / "library.yml").read_text())
    amazon_domain = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dstripbooks&field-keywords="
    random.shuffle(books)

    get_cover_images(books)

    for item in books:
        star_num = 3 if not item.get("star") else int(item["star"])
        star_text = (
            f"![Star](https://img.shields.io/badge/Recommend-{star_num * star}-green)"
        )

        grid_items.append(
            f"""\
        `````{{grid-item-card}} {" ".join(item["name"].split())}
        :text-align: center
        <a href="{amazon_domain + item['name']}" target='_blank'>
        <img src="{item["image"]}" alt="logo" loading="lazy" style="max-width: 100%; max-height: 350px; margin-top: 1rem;" /> </a>
        +++

        ````{{grid}} 2 2 2 2
        :margin: 0 0 0 0
        :padding: 0 0 0 0
        :gutter: 1

        ```{{grid-item}}
        :child-direction: row
        :child-align: end
        {star_text}
        ```

        ````

        `````
        """
        )
    grid_items = "\n".join(grid_items)

    # :column: text-center col-6 col-lg-4
    # :card: +my-2
    # :img-top-cls: w-75 m-auto p-2
    # :body: d-none
    panels = f"""
![books](https://img.shields.io/badge/Total%20Books-{len(books)}-red?style=for-the-badge&logo=gitbook)
``````{{grid}} 1 2 3 3
:gutter: 1 1 2 2
:class-container: full-width
{dedent(grid_items)}
``````
    """
    (Path(app.srcdir) / "gallery.txt").write_text(panels)


def setup(app: Sphinx):
    app.add_css_file("custom.css")
    app.connect("builder-inited", build_gallery)
