from __future__ import annotations
from pathlib import Path
from typing import Any, Iterable
import rtoml  # type: ignore


class PathParser:
    """Helpful object for parsing `Content`s from paths."""

    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def path(self) -> Path:
        return self._path

    def parse(self) -> Iterable[Content]:
        if self.path.is_file() and is_toml_file(self.path):
            yield Content.toml(self.path)
        paths = self.path.glob("*.toml")  # TODO
        for path in paths:
            if is_toml_file(path):
                yield Content.toml(path)
            else:
                yield Content.file(path)


class Content:
    """Generic object for loading parsed contents into."""

    def __init__(self, name: str, data: dict[str, Any], source: Path) -> None:
        self.name = name
        self._data = data
        self._source = source

    @property
    def data(self) -> dict[str, Any]:
        return self._data

    @staticmethod
    def file(path: Path) -> Content:
        return Content(str(path), {}, source=path)  # TODO

    @staticmethod
    def toml(path: Path) -> Content:
        data = toml_data(path)
        project = data.get("project", {})
        if "version" in project:
            data["version"] = project.get("version")
        if "description" in project:
            data["description"] = project.get("description")
        name = project.get("name", str(path))
        return Content(name, data, source=path)

    @property
    def version(self) -> str:
        return self.data.get("version", "could not parse version")

    @property
    def description(self) -> str:
        return self.data.get("description", "could not parse description")

    @property
    def source(self) -> Path:
        return self._source

    def info(self) -> str:
        return f"""\
Content
  Name: {self.name}
  Version: {self.version}
  Description: {self.description}
  Source: {self.source}
"""


def toml_data(path: Path) -> dict[str, Any]:
    return rtoml.load(path)


def is_toml_file(path: Path) -> bool:
    return path.suffix == ".toml"
