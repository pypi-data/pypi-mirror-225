"""
Copyright 2021 Daniel Afriyie

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import re
import stat
import errno
import shutil
import typing
import threading

from ru.hints import Path
from ru.constants import constants

_MUTEX = threading.Lock()
_PATTERN = re.compile(r"[0-9]+")
_FILENAMES: dict[str, int] = {}  # cache to keep track of filenames

Func = typing.Callable[..., typing.Any]


def get_data(
        fn: Path,
        split: typing.Optional[bool] = False,
        split_char: typing.Optional[str] = None,
        filter_blanks: typing.Optional[bool] = False
) -> typing.Union[str, typing.List[str]]:
    """
    :param fn: filename to open
    :param split: if you want to split the data read
    :param split_char: character you want to split the data on
    :param filter_blanks: remove empty strings if split=True
    Example:
    >>>data = get_data("file.txt", split=True, split_char=",")
    >>>print(data)
    [1, 2, 3, 4]
    """
    with open(fn, encoding=constants.ENCODING) as f:
        data = f.read()
        if split:
            if split_char:
                data_split = data.split(split_char)
                if filter_blanks:
                    data_split = [s.strip() for s in data_split if s.strip() != ""]
                    return data_split
                return data_split
    return data


def mk_dir(*paths: Path) -> None:
    with _MUTEX:
        for p in paths:
            os.makedirs(p, exist_ok=True)


def key(s: str) -> int:
    try:
        return int("".join(_PATTERN.findall(str(s))))
    except (ValueError, TypeError):
        return 0


def get_filename(name: str, path: Path, is_folder: typing.Optional[bool] = False) -> Path:
    with _MUTEX:
        split = name.split(".")
        if is_folder is False:
            ext = f".{split.pop(-1)}"
            fn = "".join(split)
        else:
            fn = name
            ext = ""

        results = _FILENAMES.get(fn, None)
        if results is not None:
            n = results + 1
            _FILENAMES[fn] = n
            return os.path.join(path, f"{fn}({n}){ext}")

        filename = os.path.join(path, name)
        if not os.path.exists(filename):
            _FILENAMES[fn] = 0
            return filename

        lower = fn.lower()
        files = [f for f in os.listdir(path) if lower in f.lower()]
        files.sort(key=key, reverse=True)
        f0 = files[0]
        n = key(f0) + 1
        _FILENAMES[fn] = n
        return os.path.join(path, f"{fn}({n}){ext}")


def handle_remove_read_only(func: typing.Callable[[Path], None], path: Path, exc: typing.Sequence[typing.Any]) -> None:
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        func(path)
    else:
        raise


def remove_dir(p: Path) -> None:
    with _MUTEX:
        try:
            shutil.rmtree(p, ignore_errors=False, onerror=handle_remove_read_only)
        except:
            pass
