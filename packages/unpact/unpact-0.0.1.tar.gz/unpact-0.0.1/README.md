# unpact

A lightweight library for tabulating dictionaries.

## Usage

A basic example:

```python
from unpact import unwind, ColumnDef

columns: List[ColumnDef] = [
    'calendar.year',
    'calendar.date',
    'locations.location',
    'locations.x',
    'locations.y'
]

 # columns of the same child and the same length are considered 'adjacent'
 # adjacent columns are zipped together.
 # here, 'x' and 'y' are considered 'adjacent'
data = {
    'calendar': {'year': 2022, 'date': 'Aug 14'},
    'locations': [
        {'location': 'Loc1', 'x': [1,2,3,4], 'y': [1,2,3,4]},
        {'location': 'Loc2', 'x': [11,22,33,44], 'y': [11,22,33,44]},
        {'location': 'Loc2', 'x': [11], 'y': [11]},
    ],
    'ignored': "This isn't in the ColumDefs so won't be included"
}

table = unwind(data, columns)
print(pl.from_dicts(table))

--
shape: (9, 5)
┌──────┬────────┬──────────┬─────┬─────┐
│ year ┆ date   ┆ location ┆ x   ┆ y   │
│ ---  ┆ ---    ┆ ---      ┆ --- ┆ --- │
│ i64  ┆ str    ┆ str      ┆ i64 ┆ i64 │
╞══════╪════════╪══════════╪═════╪═════╡
│ 2022 ┆ Aug 14 ┆ Loc1     ┆ 1   ┆ 1   │
│ 2022 ┆ Aug 14 ┆ Loc1     ┆ 2   ┆ 2   │
│ 2022 ┆ Aug 14 ┆ Loc1     ┆ 3   ┆ 3   │
│ 2022 ┆ Aug 14 ┆ Loc1     ┆ 4   ┆ 4   │
│ 2022 ┆ Aug 14 ┆ Loc2     ┆ 11  ┆ 11  │
│ 2022 ┆ Aug 14 ┆ Loc2     ┆ 22  ┆ 22  │
│ 2022 ┆ Aug 14 ┆ Loc2     ┆ 33  ┆ 33  │
│ 2022 ┆ Aug 14 ┆ Loc2     ┆ 44  ┆ 44  │
│ 2022 ┆ Aug 14 ┆ Loc2     ┆ 11  ┆ 11  │
└──────┴────────┴──────────┴─────┴─────┘
```

A more complex example using ColumnSpecs:

```python
import polars as pl
from unpact import unwind, ColumnDef

# You can pass in a pass in a 'ColumnSpec' to change the behavior of a column
# current values are 'formatter' which accepts a callable and 'name', a string which will rename the column
columns: List[ColumnDef] = [
    'calendar.year',
    'calendar.date',
    ('locations.location', {'name': 'loc'}),
    ('locations.coords', {'formatter': lambda coords: {'x': coords[0], 'y': coords[1]}})
]

data = {
    'calendar': {'year': 2022, 'date': 'Aug 14'},
    'locations': [
        {'location': 'Loc1', 'coords': [[1,1], [2,2], [3,3]]},
        {'location': 'Loc2', 'coords': [[1,1], [2,2], [3,3]]},
        {'location': 'Loc2', 'coords': [[1,1], [2,2], [3,3]]},
    ],
    'ignored': "This isn't in the ColumDefs so won't be included"
}

table = unwind(data, columns)
print(pl.from_dicts(table))

---
shape: (9, 5)
┌──────┬────────┬──────┬─────┬─────┐
│ year ┆ date   ┆ loc  ┆ x   ┆ y   │
│ ---  ┆ ---    ┆ ---  ┆ --- ┆ --- │
│ i64  ┆ str    ┆ str  ┆ i64 ┆ i64 │
╞══════╪════════╪══════╪═════╪═════╡
│ 2022 ┆ Aug 14 ┆ Loc1 ┆ 1   ┆ 1   │
│ 2022 ┆ Aug 14 ┆ Loc1 ┆ 2   ┆ 2   │
│ 2022 ┆ Aug 14 ┆ Loc1 ┆ 3   ┆ 3   │
│ 2022 ┆ Aug 14 ┆ Loc2 ┆ 1   ┆ 1   │
│ 2022 ┆ Aug 14 ┆ Loc2 ┆ 2   ┆ 2   │
│ 2022 ┆ Aug 14 ┆ Loc2 ┆ 3   ┆ 3   │
│ 2022 ┆ Aug 14 ┆ Loc2 ┆ 1   ┆ 1   │
│ 2022 ┆ Aug 14 ┆ Loc2 ┆ 2   ┆ 2   │
│ 2022 ┆ Aug 14 ┆ Loc2 ┆ 3   ┆ 3   │
└──────┴────────┴──────┴─────┴─────┘

```

A demonstration showing 'adjacency' at multiple levels of nesting:

```python

columns: List[ColumnDef] = [
    'calendar.year',
    'calendar.date',
    ('locations_1.location', {'name': 'loc'}),
    ('locations_1.coords', {'formatter': lambda coords: {'x': coords[0], 'y': coords[1]}}),
    ('locations_2.location', {'name': 'loc'}),
    ('locations_2.coords', {'formatter': lambda coords: {'x': coords[0], 'y': coords[1]}})
]

data = {
    'calendar': {'year': 2022, 'date': 'Aug 14'},
    'locations_1': [
        {'location': 'Loc1', 'coords': [[1,1], [2,2], [3,3]]},
        {'location': 'Loc2', 'coords': [[1,1], [2,2], [3,3]]},
    ],
    'locations_2': [
        {'location': 'Loc1', 'coords': [[1,1], [2,2], [3,3]]},
        {'location': 'Loc2', 'coords': [[1,1], [2,2], [3,3]]},
    ],
    'ignored': "This isn't in the ColumDefs so won't be included"
}

table = unwind(data, columns)
assert len(table) == 12 # 3 rows per record, 4 records
print(pl.from_dicts(table))

---
shape: (12, 5)
┌──────┬────────┬──────┬─────┬─────┐
│ year ┆ date   ┆ loc  ┆ x   ┆ y   │
│ ---  ┆ ---    ┆ ---  ┆ --- ┆ --- │
│ i64  ┆ str    ┆ str  ┆ i64 ┆ i64 │
╞══════╪════════╪══════╪═════╪═════╡
│ 2022 ┆ Aug 14 ┆ Loc1 ┆ 1   ┆ 1   │
│ 2022 ┆ Aug 14 ┆ Loc1 ┆ 2   ┆ 2   │
│ 2022 ┆ Aug 14 ┆ Loc1 ┆ 3   ┆ 3   │
│ 2022 ┆ Aug 14 ┆ Loc2 ┆ 1   ┆ 1   │
│ …    ┆ …      ┆ …    ┆ …   ┆ …   │
│ 2022 ┆ Aug 14 ┆ Loc1 ┆ 3   ┆ 3   │
│ 2022 ┆ Aug 14 ┆ Loc2 ┆ 1   ┆ 1   │
│ 2022 ┆ Aug 14 ┆ Loc2 ┆ 2   ┆ 2   │
│ 2022 ┆ Aug 14 ┆ Loc2 ┆ 3   ┆ 3   │
└──────┴────────┴──────┴─────┴─────┘

```
