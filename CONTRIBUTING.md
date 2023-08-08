# Contributing

We absolutely welcome any code contributions and we hope that this
guide will facilitate an understanding of the ``ansys-tools-repo-sync`` code
repository. It is important to note that while the ``ansys-tools-repo-sync`` software
package is maintained by ANSYS and any submissions will be reviewed
thoroughly before merging, we still seek to foster a community that can
support user questions and develop new features to make this software
a useful tool for all users. As such, we welcome and encourage any
questions or submissions to this repository.

For contributing to this project, please refer to the [PyAnsys Developer's Guide].

[PyAnsys Developer's Guide]: https://dev.docs.pyansys.com/index.html

## Installation

Installing in developer mode allows you to modify the source and enhance it.

Before contributing to the project, please refer to the [PyAnsys Developer's guide](https://dev.docs.pyansys.com/). You will
need to follow these steps:

1. Start by cloning this repository:

   ```bash
   git clone https://github.com/ansys/pre-commit-hooks
   ```

2. Create a fresh-clean Python environment and activate it:

   ```bash
   # Create a virtual environment
   python -m venv .venv

   # Activate it in a POSIX system
   source .venv/bin/activate

   # Activate it in Windows CMD environment
   .venv/Scripts/Activate.bat

   # Activate it in Windows Powershell
   .venv/Scripts/Activate.ps1
   ```

3. Install the project in editable mode:

   ```bash
   python -m pip install -e .
   ```

## Raw testing

If required, you can always call the style commands ([black](https://black.readthedocs.io/en/stable/), [isort](https://pycqa.github.io/isort/),
[flake8](https://flake8.pycqa.org/en/latest/)) or unit testing ones ([pytest](https://docs.pytest.org/en/stable/)) from the command line. However,
this does not guarantee that your project is being tested in an isolated
environment, which is the reason why tools like [tox](https://tox.readthedocs.io/en/latest/) exist.