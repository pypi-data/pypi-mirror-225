from __future__ import annotations
from pathlib import Path
from argparse import ArgumentParser
from pbite.parser import PathParser
from pbite import fmt_bite, __version__


def cli() -> None:
    parser = ArgumentParser(
        "PBite",
        description="""\
PBite: `ls` for project metadata. Use `pb .` to parse metadata from the current
directory.
""",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="The path to print data from (default: '.')",
    )
    parser.add_argument(
        "-p", "--path", dest="path", help="Specify a path to process data from."
    )
    parser.add_argument("--version", action="version", version=f"pb {__version__}")
    args = parser.parse_args()

    path = Path(args.path).resolve()
    for content in PathParser(path).parse():
        print(fmt_bite(content))
