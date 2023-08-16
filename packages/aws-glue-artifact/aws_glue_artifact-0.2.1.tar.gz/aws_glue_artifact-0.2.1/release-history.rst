.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.2.1 (2023-08-15)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Breaking Change**

- drop the s3 and dynamodb backend, use s3 only backend from 0.2.1
- the most of public method now requires a ``(bsm=...)`` arguments.

**Features and Improvements**

- add the following methods to ``GlueETLScriptArtifact``, ``GluePythonLibArtifact``:
    - ``bootstrap``
    - ``publish_artifact_version``
    - ``list_artifact_versions``
    - ``get_artifact_version``
    - ``get_artifact_s3path``
    - ``get_latest_published_artifact_version_number``
    - ``delete_artifact_version``
    - ``purge_all``
    - ``put_alias``
    - ``get_alias``
    - ``list_alias``
    - ``delete_alias``
- allow user to create alias for artifact version.


0.1.2 (2023-07-08)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Add a ``aws-glue-artifact.txt`` to the Glue Python library zip file to ensure that it is a folder.


0.1.1 (2023-07-07)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release.
- Add the following public API:
    - ``aws_glue_artifact.api.GlueETLScriptArtifact``
    - ``aws_glue_artifact.api.GluePythonLibArtifact``
