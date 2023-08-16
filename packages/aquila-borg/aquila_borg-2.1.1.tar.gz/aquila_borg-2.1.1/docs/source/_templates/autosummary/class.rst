.. default-domain:: py

{{ objname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ module }}.{{ objname }}
   :members:


.. rubric:: Methods

.. autosummary::
   {% for item in methods %}
   ~{{ module }}.{{ objname }}.{{ item }}
   {%- endfor %}
