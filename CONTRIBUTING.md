# Contributor Guide

Thank you for your interest in improving this project.
This project is open-source under the [MIT license] and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- [Source Code]
- [Documentation]
- [Issue Tracker]
- [Code of Conduct]

[mit license]: https://opensource.org/licenses/mit
[source code]: https://github.com/ylab-hi/yanglab-guide
[documentation]: https://yanglab-guide.readthedocs.io/
[issue tracker]: https://github.com/ylab-hi/yanglab-guide/issues

# How to report a bug

Report bugs on the [Issue Tracker].

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.

# How to request a feature

Request features on the [Issue Tracker].

# How to set up your development environment

Install the package with development requirements:

```console
$ pip install -r requirements.txt
```

# How to build the project

Run the full test suite:

```console
$ make html
```

# How to get help

```console
$ make help
```

# How to submit changes

Open a [pull request] to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The test suite must pass without errors and warnings.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

To run linting and code formatting checks before committing your change, you can install pre-commit as a Git hook by running the following command:

```console
$ nox --session=pre-commit -- install
```

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.

[pull request]: https://github.com/ylab-hi/yanglab-guide/pulls

<!-- github-only -->

[code of conduct]: CODE_OF_CONDUCT.md
