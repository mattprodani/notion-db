import pandas as pd
from typing import List, Dict, Tuple, Optional, Any, TypeVar

from .Schema import Schema

class DatabaseRow:

    def __init__(self, data: Dict[str, Any], schema: Schema = None, types: Dict[str, str] = None) -> None:
        """
            Creates database row,
            either from a list of values or from a dictionary of values.

            :param data: A dictionary of values

            Must provide one of:
            :param schema: The schema of the database
            :param types: A dictionary of labels to types

            Example:
            row = DatabaseRow({"Name": "John", "Age": 20}, schema = schema)
            
            OR

            row = DatabaseRow({"Name": "John", "Age": 20}, types = {"Name": "text", "Age": "number"})
        """
        self.values = data
        if schema:
            self.schema = schema
        elif types:
            labels = list(data.keys())
            self.schema = Schema(labels, [types[label] for label in labels])
        else:
            raise ValueError("Must provide either a schema or a dictionary of types.")

        self._compile()

    def _compile(self) -> Dict[str, Any]:
        """
            Compiles the row into a dictionary of values.
        """
        data = {}
        for label, value in self.values.items():
            data[label] = self.schema[label].compile(value)
        self.notion_properties = data
        return data

    @classmethod
    def from_pandas(cls, row: pd.Series, schema: Optional[Any] = None) -> 'DatabaseRow':
        """
            Creates a DatabaseRow from a pandas Series.
        """
        return cls(row.to_dict(), schema = schema)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value
        self._compile()