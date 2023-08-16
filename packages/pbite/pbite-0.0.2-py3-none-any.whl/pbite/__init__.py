from pbite.parser import Content

__version__ = "0.0.2"


def fmt_bite(content: Content) -> str:
    """Format a content bite."""
    return info(content)  # TODO


def info(content: Content) -> str:
    return content.info()
