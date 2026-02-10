"""Nox sessions."""

import shutil
from pathlib import Path

import nox
from nox.sessions import Session

nox.options.sessions = ["docs"]
owner, repository = "ylab-hi", "yanglab-guide"
labels = "labguide", "documentation"
bump_paths = (
    "README.md",
    "source/index.md",
    "source/developguide.md",
    "source/library.md",
)


@nox.session(name="prepare-release")
def prepare_release(session: Session) -> None:
    """Prepare a GitHub release."""
    args = [
        f"--owner={owner}",
        f"--repository={repository}",
        *[f"--bump={path}" for path in bump_paths],
        *[f"--label={label}" for label in labels],
        *session.posargs,
    ]
    session.install("click", "github3.py")
    session.run("python", "tools/prepare-github-release.py", *args, external=True)


@nox.session(name="publish-release")
def publish_release(session: Session) -> None:
    """Publish a GitHub release."""
    args = [f"--owner={owner}", f"--repository={repository}", *session.posargs]
    session.install("click", "github3.py")
    session.run("python", "tools/publish-github-release.py", *args, external=True)


nox.options.sessions = ["linkcheck"]


@nox.session(venv_backend="uv")
def docs(session: Session) -> None:
    """Build the documentation."""
    args = session.posargs or ["-W", "-n", "source", "source/_build"]

    if session.interactive and not session.posargs:
        args = ["-a", "--watch=source/_static", "--open-browser", *args]

    builddir = Path("source", "_build")
    if builddir.exists():
        shutil.rmtree(builddir)

    # Install dependencies from pyproject.toml into nox's venv
    session.run("uv", "pip", "install", "-r", "pyproject.toml", external=True)

    if session.interactive:
        session.run("sphinx-autobuild", *args)
    else:
        session.run("sphinx-build", *args)


@nox.session(venv_backend="uv")
def linkcheck(session: Session) -> None:
    """Check documentation links."""
    args = session.posargs or [
        "-b",
        "linkcheck",
        "-W",
        "--keep-going",
        "source",
        "source/_build",
    ]

    builddir = Path("docs", "_build")
    if builddir.exists():
        shutil.rmtree(builddir)

    # Install dependencies from pyproject.toml into nox's venv
    session.run("uv", "pip", "install", "-r", "pyproject.toml", external=True)

    session.run("sphinx-build", *args)


@nox.session(name="dependencies-table")
def dependencies_table(session: Session) -> None:
    """Print the dependencies table."""
    session.install("tomli")
    session.run("python", "tools/dependencies-table.py", external=True)
