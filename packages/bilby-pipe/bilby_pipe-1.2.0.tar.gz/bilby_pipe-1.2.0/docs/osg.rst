===================================
The Open Science Grid and IGWN-grid
===================================

The `IGWN Grid <https://computing.docs.ligo.org/guide/condor/>`_ is now the
recommended way to submit :code:`bilby_pipe` analyses using LVK resources.
The IGWN Grid allows access to all dedicated resources (i.e. CIT, LHO), but also
resources such as the Open Science Grid.

To run jobs through the OSG, login to

.. code-block:: console

   ssh albert.einstein@ldas-osg.ligo.caltech.edu

Then submit usual :code:`bilby_pipe` jobs, but with the flag

.. code-block:: console

   osg = True

in your configuration (ini) files.

When running on the IGWN-grid, the software you run needs to be available on
the compute nodes. This is most easily done by using the `IGWN conda
distribution available through cvmfs
<https://computing.docs.ligo.org/conda/>`_. To this end, you should either
submit your job using an IGWN environment, or use the :code:`conda-env` flag to
choose one of the IGWN environments.

When using the IGWN-grid, you can specify which site you would like your job
to run on by using the :code:`desired-sites` option.
