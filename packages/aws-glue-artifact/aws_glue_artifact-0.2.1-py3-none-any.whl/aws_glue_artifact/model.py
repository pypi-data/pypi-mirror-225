# -*- coding: utf-8 -*-

"""
Todo: add docstring
"""

import typing as T
import dataclasses
from pathlib import Path as _Path

from func_args import NOTHING
from pathlib_mate import Path
from s3pathlib import S3Path
from boto_session_manager import BotoSesManager
from versioned.api import s3_only_backend

from .vendor.build import build_python_lib
from .vendor.hashes import hashes


PT = T.Union[str, _Path, Path]

LATEST_VERSION = s3_only_backend.LATEST_VERSION
Artifact = s3_only_backend.Artifact
Alias = s3_only_backend.Alias
Repository = s3_only_backend.Repository


@dataclasses.dataclass
class Base:
    """
    Base class for AWS Glue artifact.
    """

    aws_region: str = dataclasses.field()
    s3_bucket: str = dataclasses.field()
    s3_prefix: str = dataclasses.field()
    artifact_name: str = dataclasses.field()
    _repo: Repository = dataclasses.field(init=False)

    def _common_post_init(self, suffix: str):
        self._repo = Repository(
            aws_region=self.aws_region,
            s3_bucket=self.s3_bucket,
            s3_prefix=self.s3_prefix,
            suffix=suffix,
        )

    @property
    def repo(self) -> Repository:
        """
        Access the underlying artifact repository object.
        """
        return self._repo

    def bootstrap(self, bsm: BotoSesManager):  # pragma: no cover
        """
        Create necessary backend resources for the artifact store.

        :param bsm: ``boto_session_manager.BotoSesManager`` object.
        """
        return self.repo.bootstrap(bsm=bsm)

    def publish_artifact_version(
        self,
        bsm: BotoSesManager,
    ) -> Artifact:  # pragma: no cover
        """
        Creates a version from the latest artifact. Use versions to create an
        immutable snapshot of your latest artifact.

        :param bsm: ``boto_session_manager.BotoSesManager`` object.
        """
        return self.repo.publish_artifact_version(bsm=bsm, name=self.artifact_name)

    def list_artifact_versions(
        self,
        bsm: BotoSesManager,
    ) -> T.List[Artifact]:  # pragma: no cover
        """
        Return a list of artifact versions. The latest version is always the first item.
        And the newer version comes first.

        :param bsm: ``boto_session_manager.BotoSesManager`` object.
        """
        return self.repo.list_artifact_versions(bsm=bsm, name=self.artifact_name)

    def get_artifact_version(
        self,
        bsm: BotoSesManager,
        version: T.Optional[T.Union[int, str]] = None,
    ) -> Artifact:  # pragma: no cover
        """
        Return the information about the artifact or artifact version.

        :param bsm: ``boto_session_manager.BotoSesManager`` object.
        :param version: artifact version. If ``None``, return the latest version.
        """
        return self.repo.get_artifact_version(
            bsm=bsm,
            name=self.artifact_name,
            version=version,
        )

    def get_artifact_s3path(
        self,
        bsm: BotoSesManager,
        version: T.Optional[T.Union[int, str]] = None,
    ) -> S3Path:  # pragma: no cover
        """
        Get the S3 path of the versioned artifact.

        :param bsm: ``boto_session_manager.BotoSesManager`` object.
        :param version: artifact version. If ``None``, return the latest version.
        """
        return self.repo.get_artifact_version(
            bsm=bsm,
            name=self.artifact_name,
            version=version,
        ).s3path

    def get_latest_published_artifact_version_number(
        self,
        bsm: BotoSesManager,
    ) -> int:  # pragma: no cover
        """
        Return the latest published artifact version number,
        if no version has been published yet, return 0.

        :param bsm: ``boto_session_manager.BotoSesManager`` object.
        """
        return self.repo.get_latest_published_artifact_version_number(
            bsm=bsm,
            name=self.artifact_name,
        )

    def delete_artifact_version(
        self,
        bsm: BotoSesManager,
        version: T.Union[int, str],
    ):  # pragma: no cover
        """
        Deletes a specific version of artifact.

        :param bsm: ``boto_session_manager.BotoSesManager`` object.
        :param version: artifact version.
        """
        return self.repo.delete_artifact_version(
            bsm=bsm,
            name=self.artifact_name,
            version=version,
        )

    def purge_all(
        self,
        bsm: BotoSesManager,
    ):  # pragma: no cover
        """
        Completely delete all artifacts and aliases.
        This operation is irreversible. It will remove all related S3 artifacts.

        :param bsm: ``boto_session_manager.BotoSesManager`` object.
        """
        return self.repo.purge_artifact(bsm=bsm, name=self.artifact_name)

    def put_alias(
        self,
        bsm: BotoSesManager,
        alias: str,
        version: T.Optional[T.Union[int, str]] = None,
        secondary_version: T.Optional[T.Union[int, str]] = None,
        secondary_version_weight: T.Optional[int] = None,
    ) -> Alias:  # pragma: no cover
        """
        Creates an alias for an artifact version. If ``version`` is not specified,
        the latest version is used.

        You can also map an alias to split invocation requests between two versions.
        Use the ``secondary_version`` and ``secondary_version_weight`` to specify
        a second version and the percentage of invocation requests that it receives.

        :param bsm: ``boto_session_manager.BotoSesManager`` object.
        :param alias: alias name. alias name cannot have hyphen.
        :param version: artifact version. If ``None``, the latest version is used.
        :param secondary_version: see above.
        :param secondary_version_weight: an integer between 0 ~ 100.
        """
        return self.repo.put_alias(
            bsm=bsm,
            name=self.artifact_name,
            alias=alias,
            version=version,
            secondary_version=secondary_version,
            secondary_version_weight=secondary_version_weight,
        )

    def get_alias(
        self,
        bsm: BotoSesManager,
        alias: str,
    ) -> Alias:  # pragma: no cover
        """
        Return details about the alias.

        :param bsm: ``boto_session_manager.BotoSesManager`` object.
        :param alias: alias name. alias name cannot have hyphen.
        """
        return self.repo.get_alias(
            bsm=bsm,
            name=self.artifact_name,
            alias=alias,
        )

    def list_alias(
        self,
        bsm: BotoSesManager,
    ) -> T.List[Alias]:  # pragma: no cover
        """
        Returns a list of aliases for an artifact.

        :param bsm: ``boto_session_manager.BotoSesManager`` object.
        """
        return self.repo.list_aliases(
            bsm=bsm,
            name=self.artifact_name,
        )

    def delete_alias(
        self,
        bsm: BotoSesManager,
        alias: str,
    ):  # pragma: no cover
        """
        Deletes an alias.

        :param bsm: ``boto_session_manager.BotoSesManager`` object.
        :param alias: alias name. alias name cannot have hyphen.
        """
        return self.repo.delete_alias(
            bsm=bsm,
            name=self.artifact_name,
            alias=alias,
        )


@dataclasses.dataclass
class GlueETLScriptArtifact(Base):
    """
    AWS Glue ETL Script Artifact.

    :param aws_region: AWS region name of the artifact store.
    :param s3_bucket: S3 bucket name of the artifact store.
    :param s3_prefix: S3 prefix name of the artifact store.
    :param dynamodb_table_name: DynamoDB table name of the artifact store metadata.
    :param artifact_name: Name of the artifact. Eventually, the binary artifact
        will be stored at s3://${s3_bucket}/${s3_prefix}/${artifact_name}/LATEST.py
        the metadata will be stored in ${dynamodb_table_name} DynamoDB table.
    :param path_glue_etl_script: The path of the Glue ETL Python script for artifact.
    """

    path_glue_etl_script: PT = dataclasses.field()

    def __post_init__(self):
        self.path_glue_etl_script = Path(self.path_glue_etl_script).absolute()
        self._common_post_init(suffix=".py")

    def put_artifact(
        self,
        bsm: BotoSesManager,
        metadata: T.Dict[str, str] = NOTHING,
        tags: T.Dict[str, str] = NOTHING,
    ) -> Artifact:
        """
        Put the artifact to the artifact store.

        :param metadata: Additional custom metadata of the artifact.
        :param tags: Additional custom AWS resource tags of the artifact.
        """
        content = self.path_glue_etl_script.read_bytes()
        glue_etl_script_sha256 = hashes.of_bytes(content)
        final_metadata = {
            "glue_etl_script_sha256": glue_etl_script_sha256,
        }
        if metadata is not NOTHING:
            final_metadata.update(metadata)
        return self.repo.put_artifact(
            bsm=bsm,
            name=self.artifact_name,
            content=content,
            content_type="text/plain",
            metadata=final_metadata,
            tags=tags,
        )


@dataclasses.dataclass
class GluePythonLibArtifact(Base):
    """
    AWS Glue Python Library Artifact.

    :param aws_region: AWS region name of the artifact store.
    :param s3_bucket: S3 bucket name of the artifact store.
    :param s3_prefix: S3 prefix name of the artifact store.
    :param dynamodb_table_name: DynamoDB table name of the artifact store metadata.
    :param artifact_name: Name of the artifact. Eventually, the binary artifact
        will be stored at s3://${s3_bucket}/${s3_prefix}/${artifact_name}/LATEST.zip
        the metadata will be stored in ${dynamodb_table_name} DynamoDB table.
    :param dir_glue_python_lib: The directory of the Python library to be built
        for artifact.
    :param dir_glue_build: The temporary directory to store the intermedia
        built artifact. Note that this directory will be removed for reset before
        building the artifact.
    """

    dir_glue_python_lib: PT = dataclasses.field()
    dir_glue_build: PT = dataclasses.field()

    def __post_init__(self):
        self.dir_glue_python_lib = Path(self.dir_glue_python_lib).absolute()
        self.dir_glue_build = Path(self.dir_glue_build).absolute()
        self._common_post_init(suffix=".zip")

    @property
    def dir_glue_build_temp(self) -> Path:
        """
        example: ``${dir_glue_build}/tmp/``
        """
        return self.dir_glue_build.joinpath("tmp")

    @property
    def dir_glue_python_lib_build(self) -> Path:
        """
        example: ``${dir_glue_build}/tmp/${glue_python_lib}/``
        """
        return self.dir_glue_build_temp.joinpath(self.dir_glue_python_lib.basename)

    @property
    def path_glue_python_lib_build_zip(self) -> Path:
        """
        example: ``${dir_glue_build}/${glue_python_lib}.zip``
        """
        return self.dir_glue_build.joinpath(f"{self.dir_glue_python_lib.basename}.zip")

    def put_artifact(
        self,
        bsm: BotoSesManager,
        metadata: T.Dict[str, str] = NOTHING,
        tags: T.Dict[str, str] = NOTHING,
    ) -> Artifact:
        """
        Put the artifact to the artifact store.

        :param metadata: Additional custom metadata of the artifact.
        :param tags: Additional custom AWS resource tags of the artifact.
        """
        self.dir_glue_build.remove_if_exists()
        self.dir_glue_build.mkdir_if_not_exists()
        build_python_lib(
            dir_python_lib_source=self.dir_glue_python_lib,
            dir_python_lib_target=self.dir_glue_python_lib_build,
        )
        self.dir_glue_build_temp.joinpath("aws-glue-artifact.txt").write_text(
            "built by aws-glue-artifact: https://github.com/MacHu-GWU/aws_glue_artifact-project"
        )
        self.dir_glue_build_temp.make_zip_archive(
            dst=self.path_glue_python_lib_build_zip,
            include_dir=False,
        )
        glue_python_lib_sha256 = hashes.of_paths(paths=[self.dir_glue_python_lib_build])
        final_metadata = {
            "glue_python_lib_sha256": glue_python_lib_sha256,
        }
        if metadata is not NOTHING:
            final_metadata.update(metadata)
        return self.repo.put_artifact(
            bsm=bsm,
            name=self.artifact_name,
            content=self.path_glue_python_lib_build_zip.read_bytes(),
            content_type="application/zip",
            metadata=final_metadata,
            tags=tags,
        )
