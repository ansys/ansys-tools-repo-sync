*********************
ansys-tools-repo-sync
*********************

The ``ansys-tools-repo-sync`` library is intended to synchronize the content
of two different repositories.

What does this library do?
--------------------------

For instance, because of intellectual properties concerns, it migth not be possible
to expose publicly the entire content of a private
repository. Its owner could decide to have a second repository, a public one.
Part of the content for this public repo would come from the private repository.

``ansys-tools-repo-sync`` allows you to do so by copying a folder and its content
from one repo to the other.
In addition, it is possible to filter the type of file's extension to be copied.

.. figure:: doc/images/repo_sync.png



How to use it?
~~~~~~~~~~~~~~

A common usage for this tool consist to integrate it in one of your CI/CD pipeline or workflow.
Firstly, the tool must be installed.

.. code:: yaml
    pip install ansys.tools.repo.synchronize


Then use it can be used in the considered workflow with the appropriate argument.



Installation
------------
Install with:

.. code:: yaml

    pip install ansys-tools-repo-sync


Run such as:

.. code:: yaml

    python -c "from ansys.tools.repo_sync import synchronize"; synchronize(
    manifest=os.path.join(ASSETS_DIRECTORY, "manifest.txt"),
    token=TOKEN,
    repository="ansys-tools-repo-sync",
    organization="ansys",
    protos_path=os.path.join("assets", "ansys", "api", "test", "v0"),
    dry_run=True,
    )"

.. note::
    The parameter ``dry_run`` can be set to ``True`` while establishing
    the entire workflow for the first. It helps preventing uncessary commit
    of sensitive data.

Issues
------
To post issues, questions, and code, go to `ansys-tools-repo-sync Issues
<https://github.com/ansys/ansys-tools-repo-sync/issues>`_.



License
-------
``ansys-tools-repo-sync`` is licensed under the MIT license.