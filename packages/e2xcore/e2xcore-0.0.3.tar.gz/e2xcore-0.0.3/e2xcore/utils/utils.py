import re
from typing import Any, Dict, List
from urllib.parse import parse_qsl, urlencode, urlparse

from nbgrader.apps import NbGrader


def get_nbgrader_config():
    nbgrader = NbGrader()
    nbgrader.initialize([])
    return nbgrader.config


def format_url(url: str, params: Dict[str, Any]) -> str:
    """Join a url with search parameters

    Args:
        url (str): The url
        params (Dict[str, Any]): A dictionary of parameters

    Returns:
        str: The url with encoded search parameters
    """
    parsed = urlparse(url)
    return parsed._replace(
        query=urlencode({**dict(parse_qsl(parsed.query)), **params})
    ).geturl()


def urljoin(*parts: List[str]) -> str:
    """Join a list of parts to produce an url

    Args:
        *parts (List[str]) - a list of parts

    Returns:
        str: url with leading slash

    Example:
        >>> urljoin("e2x", "api", "v1")
        '/e2x/api/v1'
    """
    return re.sub(r"/+", r"/", ("/" + "/".join(parts)))
