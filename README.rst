*********************
ansys-tools-repo-sync
*********************

The ``ansys-tools-repo-sync`` library is intended to synchronize the content of two different repositories.

What does this library do?
--------------------------

For instance, because of intellectual properties concerns, it migth not be possible to expose publicly the entire content of a private
repository. Its owner could decide to have a second repository, a public one.
Part of the content for this public repo would come from the private repository.
``ansys-tools-repo-sync`` allows you to do so by copying a folder and its content from one repo to the other.
In addition, it is possible to filter the type of file's extension to be copied.

.. figure:: images/Guidelines_chart.png



How to use it?
~~~~~~~~~~~~~~

Install the tool on the build agent during your workflow.

.. code:: bash
    pip install ansys.tools.repo.synchronize


Then use it in your workflow with the appropriate argument.

Installation
------------
Install with:

.. code::

   pip install ansys-tools-repo-sync



Issues
------
To post issues, questions, and code, go to `ansys-tools-repo-sync Issues
<https://github.com/ansys/ansys-tools-repo-sync/issues>`_.



License
-------
``ansys-tools-repo-sync`` is licensed under the MIT license.