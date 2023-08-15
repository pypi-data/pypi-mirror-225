API Compose
~~~~~~~~~~~~~~~~~~~~

Installation
============================

.. code-block::

   pip install .

Get Started
============================

.. code-block::

   acp scaffold <your_project_name>

Run the programme
============================

.. code-block::

   acp run

Examples
============================

- Examples are in **./examples** folder

`Bullish API <./examples/bullish>`_

`Cat API <./examples/cat_api>`_

Features
=====================

API Call Composition
---------------------------

- Declare your API calls as Models.

- Distinguish between **Compile Time Rendering** and **Run Time Rendering**

- Let the framework execute your API Calls in your specified order (using networkx)

- Expose **CalculatedField** which allows users to write dynamic data for each API Call in Python

Assertion
---------------------------

- Provides Basic means to make assertions of API Calls Result

    - Jinja Syntax
    - Python Syntax


Reporting
---------------------------

- Present Test Results nicely in HTML reports



Architectural Diagram
===========================

.. figure:: ./diagrams/framework_architecture.png
   :scale: 70%
   :align: center
   :alt: API Testing Framwork Architecture

   The above is the  API Testing Framwork Architecture.

   Lucid Chart here: `https://lucid.app/lucidchart/f8d1f9f9-bc93-46ec-8e4f-6561a4c822c3/edit?beaconFlowId=70D4EDD3B7971E6C&invitationId=inv_c7b45baf-050c-480b-923e-2979440ce4c8&page=0_0#`


.. figure:: ./diagrams/framework_building_blocks.png

    Hierarchical structure of the models

    Lucid Chart here: https://lucid.app/lucidchart/f8d1f9f9-bc93-46ec-8e4f-6561a4c822c3/edit?beaconFlowId=70D4EDD3B7971E6C&invitationId=inv_c7b45baf-050c-480b-923e-2979440ce4c8&page=p0OVapsRWlkY#



Jinja Templating
============================

Compile Time Rendering
--------------------------------

- To make templates reusable, the programme exposes the means to render template files using the below syntax:

.. code-block::

    block_start_string='[%'
    block_end_string='%]'
    variable_start_string='[['
    variable_end_string=']]'
    comment_start_string='[#'
    comment_end_string='#]'

Run Time Rendering
--------------------------------

- To allow for inter-API Call dependencies within a given scenario, the programme also exposes the means to render templated fields using the below syntax:

.. code-block::

    block_start_string='{%'
    block_end_string='%}'
    variable_start_string='{{'
    variable_end_string='}}'
    comment_start_string='{#'
    comment_end_string='#}'




Config File
============================

File name is `config.yaml`

.. code-block::

    # Logging level for all loggers
    LOGGER_LEVEL:  60

    # When null, do not write log file. Else. write to log file
    LOG_FILE_PATH: null

    # When empty, do not filter logs based on events. Else, only filter for events in list
    LOG_EVENT_FILTERS: []

    # debug mode or not
    IS_DEBUG: False