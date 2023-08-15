
from typing import Tuple, Union

from .tree import ColumnSpec

__all__ = ['ColumnDef']

ColumnDef = Union[Tuple[str, ColumnSpec], str]
