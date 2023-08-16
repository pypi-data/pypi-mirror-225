"""Enable grouping and ordering of commands."""
from importlib.metadata import PackageNotFoundError, version

from click_groups.core import GroupedGroup

try:
    __version__ = version("click-groups")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Lukasz G. Migas"
__email__ = "lukas.migas@yahoo.com"

__all__ = ["GroupedGroup"]
