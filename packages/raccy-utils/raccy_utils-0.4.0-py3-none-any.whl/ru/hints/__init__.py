import os
import typing

Cast = typing.Optional[typing.Union[typing.Callable[[typing.Any], typing.Any], None]]
Path = typing.Union[str, os.PathLike[str]]
OpenPath = typing.Union[int, typing.Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]]
Config = typing.Dict[str, str]
