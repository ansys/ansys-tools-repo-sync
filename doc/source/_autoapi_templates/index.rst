API reference
=============

This page contains the ``ansys-tools-repo-sync`` API reference.

.. toctree::
   :titlesonly:
   :maxdepth: 2

   {% for page in pages %}
   {% if (page.top_level_object or page.name.split('.') | length == 3) and page.display %}
   {{ page.include_path }}
   {% endif %}
   {% endfor %}
