
.. .. image:: https://readthedocs.org/projects/aws-glue-artifact/badge/?version=latest
    :target: https://aws-glue-artifact.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/aws_glue_artifact-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/aws_glue_artifact-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/aws_glue_artifact-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/aws_glue_artifact-project

.. image:: https://img.shields.io/pypi/v/aws-glue-artifact.svg
    :target: https://pypi.python.org/pypi/aws-glue-artifact

.. image:: https://img.shields.io/pypi/l/aws-glue-artifact.svg
    :target: https://pypi.python.org/pypi/aws-glue-artifact

.. image:: https://img.shields.io/pypi/pyversions/aws-glue-artifact.svg
    :target: https://pypi.python.org/pypi/aws-glue-artifact

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/aws_glue_artifact-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/aws_glue_artifact-project

------

.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://aws-glue-artifact.readthedocs.io/en/latest/

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://aws-glue-artifact.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/aws_glue_artifact-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/aws_glue_artifact-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/aws_glue_artifact-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/aws-glue-artifact#files


Welcome to ``aws_glue_artifact`` Documentation
==============================================================================
A lot of serverless AWS Service supports versioning and alias for deployment. It made the blue / green deployment, canary deployment and rolling back super easy.

- `AWS Lambda Versioning and Alias <https://docs.aws.amazon.com/lambda/latest/dg/configuration-versions.html>`_
- `AWS StepFunction Versioning and Alias <https://docs.aws.amazon.com/step-functions/latest/dg/auth-version-alias.html>`_
- `AWS SageMaker Model Registry Versioning <https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html>`_

However, AWS Glue does not support this feature. This library provides a way to manage AWS Glue versioning and alias so you can deploy AWS Glue Jobs with confident.

Please `read this tutorial <https://github.com/MacHu-GWU/aws_glue_artifact-project/blob/main/examples/deploy_versioned_glue_artifacts.ipynb>`_ to learn how to use this library.


.. _install:

Install
------------------------------------------------------------------------------

``aws_glue_artifact`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install aws-glue-artifact

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade aws-glue-artifact
