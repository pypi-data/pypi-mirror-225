Creating Pipelines
==================
|
Pipeline creation and management in the DataOps Platform SDK follows the structure and conventions that you're already
used to in the UI, while offering an extensible, programmatic interaction with pipeline objects.

For more details, refer to the `StreamSets DataOps Platform Documentation <https://docs.streamsets.com/portal/platform-controlhub/controlhub/UserGuide/Pipelines/Pipelines_title.html>`_
for pipelines.

Instantiating a Pipeline Builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the UI, a pipeline can be created and modified from the Pipelines section as seen below:

.. image:: ../_static/images/build/pipeline_ui.png
|
|
To accomplish the same task and create a pipeline using the SDK, the first step is to instantiate a
:py:class:`streamsets.sdk.sch_models.PipelineBuilder` instance. This class handles the majority of the pipeline
configuration on your behalf by building the initial JSON representation of the pipeline, and setting default values for
essential properties (instead of requiring each to be set manually). Use the :py:meth:`streamsets.sdk.ControlHub.get_pipeline_builder`
method to instantiate the builder object by passing in the ``engine_type`` for the pipeline you plan to create -
available engine types are ``'data_collector'``, ``'snowflake'``, or ``'transformer'``.

Instantiating a :py:class:`streamsets.sdk.sch_models.PipelineBuilder` instance for either
the ``'data_collector'`` or ``'transformer'`` engine types requires the Authoring Engine be specified for the pipeline.
It can be passed into the builder's instantiation via the ``engine_id`` parameter:

.. code-block:: python

    sdc = sch.engines.get(engine_url='<data_collector_url>')
    # Available engine types are 'data_collector', 'snowflake', or 'transformer'
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sdc.id)

The ``'transformer'`` engine type follows the same conventions:

.. code-block:: python

    transformer = sch.engines.get(engine_url='<transformer_url>', engine_type='TRANSFORMER')
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=transformer.id)

On the other hand, when instantiating a :py:class:`streamsets.sdk.sch_models.PipelineBuilder` instance for the
``'snowflake'`` engine type, the ``engine_id`` parameter should not be specified:

.. code-block:: python

    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

Adding Stages to the Pipeline Builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the pipeline is created, you can add stages to it using the Pipeline Canvas UI, seen below:

.. image:: ../_static/images/build/stages_unconnected.png
|
|
To add stages to the pipeline using the SDK, utilize the :py:meth:`streamsets.sdk.sch_models.PipelineBuilder.add_stage`
method - see the API reference for this method for details on the arguments this method takes.

As shown in the image above, the simplest type of pipeline directs one origin into one destination. For this example,
you can do this with ``Dev Raw Data Source`` origin and ``Trash`` destination, respectively:

.. code-block:: python

    dev_raw_data_source = pipeline_builder.add_stage('Dev Raw Data Source')
    trash = pipeline_builder.add_stage('Trash')

.. note::
  ``Dev Raw Data Source`` origin cannot be used in Transformer for Snowflake pipelines.
  Instead, use ``Snowflake Table`` or ``Snowflake Query``

Connecting the Stages
~~~~~~~~~~~~~~~~~~~~~

Once stages have been added in the Pipeline Canvas, linking the output of one stage to the input of another connects
them, as seen below:

.. image:: ../_static/images/build/pipeline_canvas.png
|
|
With :py:class:`streamsets.sdk.sch_models.SchSdcStage` instances in hand, you can connect them by using the ``>>``
operator. Connecting the ``Dev Raw Data Source`` origin and ``Trash`` destination from the example above would look
like the following:

.. code-block:: python

    dev_raw_data_source >> trash

**Output:**

.. code-block:: python

    <com_streamsets_pipeline_stage_destination_devnull_NullDTarget (instance_name=Trash_01)>

You can also connect stages using either the :py:meth:`streamsets.sdk.sch_models.SchSdcStage.connect_inputs` or :py:meth:`streamsets.sdk.sch_models.SchSdcStage.connect_outputs` method.
To connect a stage using these methods:

.. code-block:: python

    # connect dev_raw_data_source to trash
    dev_raw_data_source.connect_outputs(stages=[trash])
    # alternatively, you can also use connect_inputs to connect dev_raw_data_source to trash
    trash.connect_inputs(stages=[dev_raw_data_source])

Connecting Event Streams
~~~~~~~~~~~~~~~~~~~~~~~~

To add event streams on the Pipeline Canvas in the UI, click the 'Produce Events' checkbox on the stage you wish to generate events from as shown below:

.. image:: ../_static/images/build/produce_events.png
|
|
Once the 'Produce Events' checkbox has been clicked, an event stream symbol should appear on the stage. Then, proceed to link the stage's event lane to another stage as shown below:

.. image:: ../_static/images/build/connect_event_lane.png
|
|
With :py:class:`streamsets.sdk.sch_models.SchSdcStage` instances in hand, you can connect a stage's event stream to another stage using the ``>=``
operator. Connecting the ``Dev Raw Data Source`` origin and ``Trash`` destination from the example above would look
like the following:

.. code-block:: python

    pipeline_finisher = pipeline_builder.add_stage('Pipeline Finisher Executor')
    dev_raw_data_source >= pipeline_finisher

You can also use the :py:meth:`streamsets.sdk.sch_models.SchSdcStage.connect_inputs` or :py:meth:`streamsets.sdk.sch_models.SchSdcStage.connect_outputs` methods to connect a stage's event stream to another stage.
To connect a stage's event stream to another stage using either of these methods, set the ``event_lane`` parameter to ``True``:

.. code-block:: python

    # connect dev_raw_data_source's event stream to pipeline_finisher
    dev_raw_data_source.connect_outputs(stages=[pipeline_finisher], event_lane=True)
    # alternatively, you can also use connect_inputs to connect dev_raw_data_source's event stream to pipeline_finisher
    pipeline_finisher.connect_inputs(stages=[dev_raw_data_source], event_lane=True)

Disconnecting the Stages
~~~~~~~~~~~~~~~~~~~~~~~~

To disconnect stages on the Pipeline Canvas in the UI, click on the stage's connection and click the Trash icon on the pop-up that appears, shown below:

.. image:: ../_static/images/build/delete_connection.png
|
|
To disconnect output lanes in the SDK, simply pass in the :py:class:`streamsets.sdk.sch_models.SchSdcStage` object to disconnect into the :py:meth:`streamsets.sdk.sch_models.SchSdcStage.disconnect_output_lanes` method.
In order to disconnect all stages receiving output from a specific stage, simply set ``all_stages`` to ``True`` within the :py:meth:`streamsets.sdk.sch_models.SchSdcStage.disconnect_output_lanes` method:

.. code-block:: python

    # disconnect dev_raw_data_source from trash
    dev_raw_data_source.disconnect_output_lanes(stages=[trash])
    # disconnect all stages receiving output from the dev_raw_data_source stage
    dev_raw_data_source.disconnect_output_lanes(all_stages=True)

To disconnect input lanes in the SDK, simply pass in the :py:class:`streamsets.sdk.sch_models.SchSdcStage` object to disconnect into the :py:meth:`streamsets.sdk.sch_models.SchSdcStage.disconnect_input_lanes` method.
In order to disconnect a specific stage from all other stages it receives input from, simply set ``all_stages`` to ``True`` within the :py:meth:`streamsets.sdk.sch_models.SchSdcStage.disconnect_input_lanes` method:

.. code-block:: python

    # disconnect trash from dev_raw_data_source
    trash.disconnect_input_lanes(stages=[dev_raw_data_source])
    # disconnect trash from all other stages it receives input from
    trash.disconnect_input_lanes(all_stages=True)

Removing Stages From the Pipeline Builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once a stage has been added, you can remove that stage using the Pipeline Canvas UI, seen below:

.. image:: ../_static/images/build/remove_stage.png
|
|
To remove stages from the pipeline_builder using the SDK, utilize the :py:meth:`streamsets.sdk.sch_models.PipelineBuilder.remove_stage`
method - see the API reference for this method for details on the arguments this method accepts.

For this example, you can delete the ``Dev Raw Data Source`` origin like this:

.. code-block:: python

    pipeline_builder.remove_stage(dev_raw_data_source)

.. note::
  Removing a stage from a :py:class:`streamsets.sdk.sch_models.PipelineBuilder` instance also removes all output & input lane references that any connected stages had to this stage.

Building the Pipeline From the PipelineBuilder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the stages are connected, you can build the :py:class:`streamsets.sdk.sch_models.Pipeline` instance with
the :py:meth:`streamsets.sdk.sch_models.PipelineBuilder.build` method:

.. code-block:: python

    pipeline = pipeline_builder.build('My first pipeline')
    pipeline

**Output:**

.. code-block:: python

    <Pipeline (pipeline_id=None, commit_id=None, name=My first pipeline, version=None)>

When building a Transformer for Snowflake pipeline, there are 4 parameters required by the Pipeline Canvas UI, seen
below:

.. image:: ../_static/images/build/snowflake_required_parameters.png
|
|
Default values for them can be set in your account (My Account > Snowflake Settings > Snowflake Pipeline Defaults). If
they aren't set, or you want to modify those values, you must do so before publishing the pipeline:

.. code-block:: python

    pipeline.configuration['connectionString'] = <Account URL>
    pipeline.configuration['warehouse'] = <Warehouse>
    pipeline.configuration['db'] = <Database>
    pipeline.configuration['schema'] = <Schema>

Importing a Pipeline into the Pipeline Builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to use an existing pipeline as the starting point when creating another pipeline.

Creating a Pipeline based off of an existing Pipeline entails importing an existing :py:class:`streamsets.sdk.sch_models.Pipeline` instance into the :py:class:`streamsets.sdk.sch_models.PipelineBuilder` object.

Importing a pipeline into the :py:class:`streamsets.sdk.sch_models.PipelineBuilder` instance can be performed by making use of the :py:meth:`streamsets.sdk.sch_models.PipelineBuilder.import_pipeline` method:

.. code-block:: python


    pipeline_to_import = sch.pipelines.get(name='Pipeline To Import')
    pipeline_builder.import_pipeline(pipeline_to_import)

Add the Pipeline to DataOps Platform
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add (commit) the pipeline to your DataOps Platform organization, you can use the Check In button as seen below:

.. image:: ../_static/images/build/pipeline_check_in.png
|
|
To add a pipeline to your DataOps Platform organization using the SDK, pass the built pipeline to the
:py:meth:`streamsets.sdk.ControlHub.publish_pipeline` method:

.. code-block:: python

    sch.publish_pipeline(pipeline, commit_message='First commit of my first pipeline')

**Output:**

.. code-block:: python

    <streamsets.sdk.sch_api.Command object at 0x7f8f2e0579b0>


.. note::
    All the above examples have focused on stages for SDC pipelines, however :py:class:`streamsets.sdk.sch_models.SchStStage` instances could be swapped into these examples for Transformer pipelines without issue.

Bringing It All Together
~~~~~~~~~~~~~~~~~~~~~~~~

The complete scripts from this section can be found below. Commands that only served to verify some output from the
example have been removed.

.. code-block:: python

    from streamsets.sdk import ControlHub

    sch = ControlHub(credential_id='<credential_id>', token='<token>')
    sdc = sch.engines.get(engine_url='<data_collector_url>')
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sdc.id)
    #transformer = sch.engines.get(engine_url='<transformer_url>', engine_type='TRANSFORMER')
    #pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=transformer.id)

    dev_raw_data_source = pipeline_builder.add_stage('Dev Raw Data Source')
    trash = pipeline_builder.add_stage('Trash')
    dev_raw_data_source >> trash

    # connect dev_raw_data_source to trash
    #dev_raw_data_source.connect_outputs(stages=[trash])
    # alternatively, you can also use connect_inputs to connect dev_raw_data_source to trash
    #trash.connect_inputs(stages=[dev_raw_data_source])

    # connect dev_raw_data_source's event stream to pipeline_finisher
    #dev_raw_data_source >= pipeline_finisher
    #dev_raw_data_source.connect_outputs(stages=[pipeline_finisher], event_lane=True)
    # alternatively, you can also use connect_inputs to connect dev_raw_data_source's event stream to pipeline_finisher
    #pipeline_finisher.connect_inputs(stages=[dev_raw_data_source], event_lane=True)

    # disconnect dev_raw_data_source from trash
    #dev_raw_data_source.disconnect_output_lanes(stages=[trash])
    # alternatively, you can also use disconnect_input_lanes to disconnect dev_raw_data_source from trash
    #trash.disconnect_input_lanes(stages=[dev_raw_data_source])

    # Remove an existing stage by passing it into the remove_stage method
    # pipeline_builder.remove_stage(dev_raw_data_source)

    # Import an existing pipeline into the pipeline_builder object to use as a starting point
    #pipeline_to_import = sch.pipelines.get(name='Pipeline To Import')
    #pipeline_builder.import_pipeline(pipeline_to_import)

    pipeline = pipeline_builder.build('My first pipeline')
    sch.publish_pipeline(pipeline, commit_message='First commit of my first pipeline')

.. code-block:: python

    from streamsets.sdk import ControlHub

    sch = ControlHub(credential_id='<credential_id>', token='<token>')
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    snowflake_query_origin = pipeline_builder.add_stage('Snowflake Query')
    trash = pipeline_builder.add_stage('Trash')
    snowflake_query_origin >> trash
    pipeline = pipeline_builder.build('My first pipeline')
    sch.publish_pipeline(pipeline, commit_message='First commit of my first pipeline')
