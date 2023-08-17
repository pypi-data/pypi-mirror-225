tomwer
======

tomwer is offering tools to automate acquisition and reconstruction processes for Tomography.
It contains:

- a library to access each acquisition process individually
- gui and applications to control main processes (reconstruction, data transfert...) and execute them as a stand alone application.
- an orange add-on to help users defining their own workflow (http://orange.biolab.si)



.. image:: http://www.edna-site.org/pub/doc/tomwer/extra/tomwer_start_short.gif


.. |Gitlab Status| image:: https://gitlab.esrf.fr/tomotools/tomwer/badges/master/pipeline.svg
    :target: https://gitlab.esrf.fr/tomotools/tomwer/pipelines


Documentation
-------------

Documentation of latest release is available at http://www.edna-site.org/pub/doc/tomwer/latest

Installation
------------

Step 1 - Create a virtual env (recommended)
'''''''''''''''''''''''''''''''''''''''''''

It is recommended to create a python virtual environment to run the workflow tool.
Virtual environment might avoid some conflict between python packages. But you can also install it on your 'current' python environment and move to step 1.

.. code-block:: bash

   virtualenv --python=python3 --system-site-packages myvirtualenv


Then activate the virtual environment

.. code-block:: bash

   source myvirtualenv/bin/activate

First update pip and setuptools to avoid some potential errors

.. code-block:: bash

   pip install --upgrade pip
   pip install setuptools --upgrade


.. note:: To quit the virtual environment

   .. code-block:: bash

      deactivate

Step 2 - tomwer (madatory)
''''''''''''''''''''''''''

To install it with all 'features':

.. code-block:: bash

    pip install tomwer[full]

alternatively you can install the master branch from

.. code-block:: bash

    pip install git+https://gitlab.esrf.fr/tomotools/tomwer/#egg=tomwer[full]


Step 3 - update orange-canvas-core and orange-widget-base (recommended)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

To access 'processing' wheels you might want to install forks of update orange-canvas-core and orange-widget-base

.. code-block:: bash

    pip install https://github.com/payno/orange-canvas-core --no-deps --upgrade
    pip install https://github.com/payno/orange-widget-base --no-deps --upgrade


Launching applications
::::::::::::::::::::::

After the installation tomwer is embedding several applications.

Those applications can be launched by calling:

.. code-block:: bash

   tomwer appName {options}

.. note:: if you only call `tomwer` then the man page will be displayed.

.. note:: You can access each application help using ``

    .. code-block:: bash

       tomwer appName --help


tomwer canvas - orange canvas
'''''''''''''''''''''''''''''

You can launch the canvas to create workflows from the different 'bricks'

.. code-block:: bash

   tomwer canvas

.. note:: you can also use `orange-canvas`

.. note:: if your installed a virtual environment do not forget to active it :

    .. code-block:: bash

       source myvirtualenv/bin/activate


Documentation
:::::::::::::

.. code-block:: bash

   cd doc
   make html

The documentation is build in doc/build/html and the entry point is index.html

.. code-block:: bash

   firefox build/html/index.html

.. note:: the build of the documentation need sphinx to be installed. This is not an hard dependacy. So you might need to install it.


You also should generate documentation to be accessible from Orange GUI (pressing the F1 key).

.. code-block:: bash

   cd doc
   make htmlhelp