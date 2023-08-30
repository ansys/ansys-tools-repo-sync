*********************
ansys-tools-repo-sync
*********************

|pyansys| |python| |pypi| |GH-CI| |codecov| |MIT| |black| |pre-commit|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-tools-repo-sync?logo=pypi
   :target: https://pypi.org/project/ansys-tools-repo-sync
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-tools-repo-sync.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-tools-repo-sync
   :alt: PyPI

.. |codecov| image:: https://codecov.io/gh/ansys/ansys-tools-repo-sync/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/ansys-tools-repo-sync
   :alt: Codecov

.. |GH-CI| image:: https://github.com/ansys/ansys-tools-repo-sync/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/ansys-tools-repo-sync/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/ansys/ansys-tools-repo-sync/main.svg
   :target: https://results.pre-commit.ci/latest/github/ansys/ansys-tools-repo-sync/main
   :alt: pre-commit.ci status


The ``ansys-tools-repo-sync`` library is intended to synchronize the content
of two different repositories.

What does this library do?
~~~~~~~~~~~~~~~~~~~~~~~~~~

For instance, due to intellectual properties concerns, it might not be possible
to expose publicly the entire content of a private repository.
Its owner could decide to have a second repository, a public one.
Part of the content for this public repo would come from the private repository.

``ansys-tools-repo-sync`` allows you to do so by copying a folder and its content
from one repo to the other.

By default, nothing is synced to the secondary repository (in order to avoid undesired
content). For that purpose, users have to provide a ``manifest`` file (in ASCII format)
that contains regular expressions for the files accepted.

For example, if we wanted to sync all ``*.py`` files, one should generate a
``manifest`` file as follows:

.. code:: bash

   *.py

.. image:: images/repo_sync.png
    :align: center


How to use it?
~~~~~~~~~~~~~~

A common usage for this tool consist to integrate it in one of your CI/CD pipeline or workflow.
Firstly, the tool must be installed.

.. code:: bash

    pip install ansys-tools-repo-sync


Then, it can be used in the considered workflow with the appropriate arguments.

Run it as follows:

.. code:: bash

    repo-sync \
      --token <token> \
      --owner <organization-name> \
      --repository <repository-name> \
      --from-dir <path-to-dir-containing-files-to-sync> \
      --to-dir <target-dir-for-sync> \
      --include-manifest <path-to-manifest>

The options above are **compulsory** in order to run the tool. If an option is missing,
the operation will fail. For more information on all the available options for this tool,
users can run:

.. code:: bash

   repo-sync --help

.. note::
    The ``--dry-run`` flag can be set while establishing the entire
    workflow for the first time. It helps preventing unnecessary commits
    of sensitive data. It will print the content expected to be committed in the
    public repository.

Issues
------
To post issues, questions, and code, go to `ansys-tools-repo-sync Issues
<https://github.com/ansys/ansys-tools-repo-sync/issues>`_.

License
-------
``ansys-tools-repo-sync`` is licensed under the MIT license.
