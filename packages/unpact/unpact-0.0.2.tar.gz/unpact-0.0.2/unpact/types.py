from typing import Protocol, Tuple, TypedDict, Union


__all__ = ["ColumnDef", "ColumnFormatter", "ColumnSpec"]


class ColumnFormatter(Protocol):
    def __call__(self, data: dict, index: int = ...) -> dict:
        ...


class ColumnSpec(TypedDict, total=False):
    name: str
    formatter: ColumnFormatter


ColumnDef = Union[Tuple[str, ColumnSpec], str]
