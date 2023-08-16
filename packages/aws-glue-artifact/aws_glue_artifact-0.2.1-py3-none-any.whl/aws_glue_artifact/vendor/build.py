# -*- coding: utf-8 -*-

import typing as T
import shutil
from pathlib import Path


def do_we_include(
    relpath: Path,
    include: T.List[str],
    exclude: T.List[str],
) -> bool:
    """
    Based on the include and exclude pattern, do we ignore this file?

    explicit exclude > explicit include > implicit include
    """
    if len(include) == 0 and len(exclude) == 0:
        return True
    elif len(include) > 0 and len(exclude) > 0:
        match_any_include = any([relpath.match(pattern) for pattern in include])
        match_any_exclude = any([relpath.match(pattern) for pattern in exclude])
        if match_any_exclude:
            return False
        else:
            return match_any_include
    elif len(include) > 0 and len(exclude) == 0:
        return any([relpath.match(pattern) for pattern in include])
    elif len(include) == 0 and len(exclude) > 0:
        return not any([relpath.match(pattern) for pattern in exclude])
    else:  # pragma: no cover
        raise NotImplementedError


def build_python_lib(
    dir_python_lib_source: T.Union[str, Path],
    dir_python_lib_target: T.Union[str, Path],
    include: T.Optional[T.Union[str, T.List[str]]] = None,
    exclude: T.Optional[T.Union[str, T.List[str]]] = None,
):
    """
    This function build python library source code distribution. It walks through
    the python library source code directory, include and exclude files based on
    definition, and copy the files to the target directory.

    :param dir_python_lib_source: where your python library source code is.
    :param dir_python_lib_target: where you want to copy the source code to.
    :param include: list of glob patterns to include.
    :param exclude: list of glob patterns to exclude.
    """
    dir_python_lib_source = Path(dir_python_lib_source).absolute()
    dir_python_lib_target = Path(dir_python_lib_target).absolute()
    if include is None:  # pragma: no cover
        include = []
    elif isinstance(include, str):  # pragma: no cover
        include = [include]
    else:  # pragma: no cover
        include = include
    if exclude is None:  # pragma: no cover
        exclude = []
    elif isinstance(exclude, str):  # pragma: no cover
        exclude = [exclude]
    else:  # pragma: no cover
        exclude = exclude
    exclude.extend(["__pycache__", "*.pyc", "*.pyo"])

    if dir_python_lib_target.exists():
        shutil.rmtree(dir_python_lib_target)

    for path in dir_python_lib_source.glob("**/*"):
        if path.is_file():
            relpath = path.relative_to(dir_python_lib_source)
            if do_we_include(relpath, include=include, exclude=exclude):
                path_new = dir_python_lib_target.joinpath(relpath)
                try:
                    path_new.write_bytes(path.read_bytes())
                except FileNotFoundError:
                    path_new.parent.mkdir(parents=True, exist_ok=True)
                    path_new.write_bytes(path.read_bytes())
        else:
            pass
