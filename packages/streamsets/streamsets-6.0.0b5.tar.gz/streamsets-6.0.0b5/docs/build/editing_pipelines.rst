Editing Pipelines
=================
|
Editing Pipelines in the DataOps Platform SDK follows the structure and conventions that you're already familiar with in the UI,
while offering an extensible, programmatic interaction with pipeline objects.

For more details on Pipeline interaction and usage in the UI, refer to the `StreamSets DataOps Platform Documentation <https://docs.streamsets.com/portal/platform-controlhub/controlhub/UserGuide/Pipelines/Pipelines_title.html>`_
for pipelines.

Retrieving An Existing Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the Pipeline UI, you can see your existing Pipelines, and click into them as necessary, seen below

.. image:: ../_static/images/build/existing_pipelines.png
|
|
The :py:attr:`streamsets.sdk.ControlHub.pipelines` attribute can be used to retrieve all your Pipelines.
This attribute returns a :py:class:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Pipeline` objects:

.. code-block:: python

    sch.pipelines

Alternatively, you can retrieve specific pipelines by specifying ``pipeline_id``, ``name``, ``version``, or ``commit_id`` to filter the pipeline results
when calling the :py:meth:`streamsets.sdk.utils.SeekableList.get` or :py:meth:`streamsets.sdk.utils.SeekableList.get_all` methods:

.. code-block:: python

    pipeline = sch.pipelines.get(name='Test Pipeline')
    all_version_1_pipelines = sch.pipelines.get_all(version='1')

    pipeline
    all_version_1_pipelines

**Output:**

.. code-block:: python

    # pipeline
    <Pipeline (pipeline_id=5b67c7dc-729b-43cc-bee7-072d3feb184b:admin, commit_id=491cf010-da8c-4e63-9918-3f5ef3b182f6:admin, name=Test Pipeline, version=1)>

    # all_version_1_pipelines
    [<Pipeline (pipeline_id=88d58863-7e8b-4831-a929-8c56db629483:admin,
                commit_id=600a7709-6a13-4e9b-b4cf-6780f057680a:admin,
                name=Test Pipeline,
                version=1)>,
     <Pipeline (pipeline_id=5b67c7dc-729b-43cc-bee7-072d3feb184b:admin,
                commit_id=491cf010-da8c-4e63-9918-3f5ef3b182f6:admin,
                name=Test Pipeline 2,
                version=1)>]

Adding Stages To An Existing Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the pipeline is created, you can add stages to it using the Pipeline Canvas UI, seen below:

.. image:: ../_static/images/build/stages_unconnected.png
|
|
To add stages to an existing pipeline using the SDK, utilize the :py:meth:`streamsets.sdk.sch_models.Pipeline.add_stage`
method - see the API reference for this method for details on the arguments this method accepts.

As shown in the image above, the simplest type of pipeline directs one origin into one destination.
To recreate the example above via the SDK, you would use the ``Dev Raw Data Source`` origin and ``Trash`` destination, respectively:

.. code-block:: python

    dev_raw_data_source = pipeline.add_stage('Dev Raw Data Source')
    trash = pipeline.add_stage('Trash')

.. note::
  ``Dev Raw Data Source`` origin cannot be used in Transformer for Snowflake pipelines.
  Instead, use ``Snowflake Table`` or ``Snowflake Query``

Removing Stages From An Existing Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once a stage has been added, you can remove that stage using the Pipeline Canvas UI, seen below:

.. image:: ../_static/images/build/remove_stage.png
|
|
To remove stages from an existing pipeline using the SDK, utilize the :py:meth:`streamsets.sdk.sch_models.Pipeline.remove_stages`
method - see the API reference for this method for details on the arguments this method accepts.

To use the SDK to delete the stage as shown in the example above, you would delete the ``Trash`` destination as seen below:

.. code-block:: python

    pipeline.remove_stage(trash)

.. note::
  Removing a stage from an existing :py:class:`streamsets.sdk.sch_models.Pipeline` instance also removes all output & input lane references that any connected stages had to this stage.

Editing Pipeline/Stage Configuration Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Once a stage has been added, you can edit it's configuration values in the Pipeline Canvas like so:

.. image:: ../_static/images/build/edit_configuration.png
|
|
To edit configuration values in the SDK, you can access the ``configuration`` property in the :py:class:`streamsets.sdk.sch_models.Pipeline` or :py:class:`streamsets.sdk.sch_models.SchSdcStage` object

For example, if you wanted to check the ``configuration`` value of the ``dev_raw_data_source`` stage, you could do the following:

.. code-block:: python

    dev_raw_data_source.configuration.batch_size
|
|

**Output:**

.. code-block:: python

    1000

Setting the configuration value is as simple as directly setting the value in-memory

.. code-block:: python

    dev_raw_data_source.configuration.batch_size = 999
|
|
.. note::
  The same workflow can be followed to access/edit configuration values of :py:class:`streamsets.sdk.sch_models.Pipeline` objects

Once you have edited your :py:class:`streamsets.sdk.sch_models.Pipeline` or :py:class:`streamsets.sdk.sch_models.SchSdcStage`, the changes must be published to Control Hub.
This can be done by taking the updated :py:class:`streamsets.sdk.sch_models.Pipeline` instance and passing it into the :py:meth:`streamsets.sdk.sch.publish_pipeline` method as seen below:

.. code-block:: python

    sch.publish_pipeline(pipeline, commit_message='My Edited Pipeline')

.. note::
    All the above examples have focused on stages for SDC pipelines, however :py:class:`streamsets.sdk.sch_models.SchStStage` instances could be swapped into these examples for Transformer pipelines without issue.

Bringing It All Together
~~~~~~~~~~~~~~~~~~~~~~~~

The complete scripts from this section can be found below. Commands that only served to verify some output from the
example have been removed.

.. code-block:: python

    from streamsets.sdk import ControlHub

    sch = ControlHub(credential_id='<credential_id>', token='<token>')

    #all_pipelines = sch.pipelines
    #all_version_1_pipelines = sch.pipelines.get_all(version='1')
    pipeline = sch.pipelines.get(name='Test Pipeline')

    dev_raw_data_source = pipeline.add_stage('Dev Raw Data Source')
    trash = pipeline.add_stage('Trash')

    # Remove trash from the Pipeline
    #pipeline.remove_stages(trash)

    dev_raw_data_source.configuration.batch_size
    dev_raw_data_source.configuration.batch_size = 999

    sch.publish_pipeline(pipeline, commit_message='My Edited Pipeline')

