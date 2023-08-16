# -*- coding: utf-8 -*-

from aws_glue_artifact import api


def test():
    _ = api
    _ = api.GlueETLScriptArtifact
    _ = api.GluePythonLibArtifact


if __name__ == "__main__":
    from aws_glue_artifact.tests import run_cov_test

    run_cov_test(__file__, "aws_glue_artifact.api", preview=False)
