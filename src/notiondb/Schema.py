from typing import List, Dict, Tuple, Optional, Any, TypeVar, Union, TYPE_CHECKING
from collections import OrderedDict
from .SchemaProperty import SchemaProperty


class Schema:
    """
    Database Schema object for Notion API

    Properties:
    ===========
    labels (list): A list of column names
    types (list): A list of types


    Creating a schema:
    ===============
    Can be created in a few different ways:
    1. From a dictionary that maps column names to types:
    Example:
        >>> schema = Schema({"Name": "title", "Age": "number"})

    2. From a list of column names and a list of types:
    Example:
        >>> schema = Schema( = ["Name", "Age"], types = ["title", "number"])

    Args:
        columns (dict|list): A dictionary that maps column names to types, or a list of column names.
        types (list, optional): Required if `columns` is a list. A list of types. Defaults to None.
    Raises:
        ValueError: If `columns` is a list, then `types` must be a list of types.
        ValueError: If list size of `columns` does not match the size of `types`.
    Returns:
        Schema: A schema object that can be used to update, create a new database, or create a new row

    Modify or add to a schema:
    =============
    To add a new column, simply set the value of a column to a new type.
    Example:
        >>> schema = Schema({"Name": "title", "Age": "number"})
        >>> schema["Is Student"] = "checkbox"
        >>> schema
        {'Name': 'title', 'Age': 'number', 'Is Student': 'checkbox'}

    To update a property's configuration, use get and access the property object directly.
    Example:
        >>> schema = Schema({"Name": "title", "Salary": "number"})
        >>> schema["Salary"]["format"] = "dollar"


    To update a notion database
    ===========================
    These are not yet implemented.
    This will allow you to update a database's schema using id and names
    for notion columns:
        >>> schema = Schema({"Name": "title", "Salary": "number"})
        >>> schema.rename("Name", "Full Name")
    """

    @property
    def labels(self) -> List[str]:
        return list(self._columns.keys())

    @property
    def types(self) -> List[str]:
        return [self._columns[key].type for key in self._columns]

    @property
    def columns(self) -> Dict[str, SchemaProperty]:
        return self.labels

    @property
    def notion(self) -> Dict[str, Any]:
        return {key: self._columns[key].notion for key in self._columns}

    def __init__(
        self,
        columns: Union[Dict[str, str], List[str]],
        types: Optional[List[str]] = None,
        id=False,
    ):
        if id:
            raise NotImplementedError

        self._columns = OrderedDict()
        if isinstance(columns, list):
            if types is None:
                raise ValueError(
                    "If columns is a list, then types must be a list of types."
                )
            if len(columns) != len(types):
                raise ValueError(
                    "List size of columns does not match the size of types."
                )
            for i in range(len(columns)):
                self._add_column(columns[i], types[i])
        else:
            for key in columns:
                self._add_column(key, columns[key])

    @classmethod
    def from_notion(cls, data: Dict[str, Any]):
        """alias for from_database"""
        return cls.from_database(data)

    @classmethod
    def from_database(cls, response: Dict[str, Any]):
        schema = cls({})
        props = response["properties"]
        for name, obj in props.items():
            schema._add_column(name, SchemaProperty(**obj))
        return schema

    def _add_column(self, name: str, type: str):
        if isinstance(type, str):
            type = SchemaProperty(name=name, type=type)
        self._columns[name] = type

    def __getitem__(self, key: str) -> SchemaProperty:
        return self._columns[key]

    def __setitem__(self, key: str, value: str):
        self._add_column(key, value)

    def __delitem__(self, key: str):
        del self._columns[key]

    def __iter__(self):
        return iter(self._columns)

    def __len__(self):
        return len(self._columns)

    def __repr__(self):
        return str(self._columns)

    def __str__(self):
        return str(self._columns)

    def __eq__(self, other):
        return self._columns == other._columns
