# PBite

`ls` for project metadata.

Use `pb` to display project metadata contents from your file system.

```
pb on  master is 📦 v0.1.0 via 🐍 v3.11.3 
❯ pb .
Content
  Name: pb
  Version: 0.1.0
  Description: `ls` for project metadata
  Source: /Users/chrispryer/github/pb/pyproject.toml
```

## Installation

```
pip install pbite
```

You can add `pb` to any `venv` with
```
python -m venv .venv
./.venv/bin/pip install pbite
```

It's recommended to install `pb` using a package manager like `rye`.
```
rye install pbite
pb --version
```