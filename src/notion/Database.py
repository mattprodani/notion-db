from multiprocessing.sharedctypes import Value
import pandas as pd
from typing import List, Dict, Tuple, Optional, Any, TypeVar, Union, TYPE_CHECKING

from .Schema import Schema

if TYPE_CHECKING:
    from .Types import Property



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
        if isinstance(data, DatabaseRow): return data
        if isinstance(data, list): raise ValueError("Failed parsing Row input, attr: data must be a Dictionary")
        self.values = data
        if schema:
            self.schema = schema
        elif types:
            labels = list(data.keys())
            self.schema = Schema(labels, [types[label] for label in labels])
        else:
            raise ValueError("Must provide either a schema or a dictionary of types.")
        self.columns = list(self.values.keys())
        self._compile()

    def update_type(self, name:str, _type: Union["Property", str]):
        """
            Update the type of a column in the schema.
            :param name: The name of the column
            :param _type: The type of the column. Either a string or property object

            Example:
            row.update_type("Name", "text")
            row.update_type("Salary", types.Number("Salary", format = "dollar"))

        """
        self.schema.update_type(name, _type)
        self._compile()

    def _compile(self) -> Dict[str, Any]:
        """
            Compiles the row into a dictionary of values.
        """
        data = {}
        for label, value in self.values.items():
            data[label] = self.schema[label].property_value(value)
        self.notion_properties = data
        return data

    def __getattr__(self, __name: str) -> Any:
        if __name in self.__dict__:
            return self.__dict__[__name]
        else:
            return self.values[__name]


    @classmethod
    def from_pandas(cls, row: pd.Series, schema: Optional[Any] = None) -> 'DatabaseRow':
        """
            Creates a DatabaseRow from a pandas Series.
            Infers the schema from the pandas Series if no schema is provided.
        """
        if isinstance(row, pd.DataFrame):
            row = row.iloc[0]

        return cls(row.to_dict(), schema = Schema(row.index.to_list()))

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value
        self._compile()

    def __setitem__(self, key, value):
        self.values[key] = value
        self._compile()

class Database:

    def __init__(self, data, schema: Optional["Schema"] = None, name = None, id =  None, cover = None):
        """
            Creates a Database object.
            :param data: A list of DatabaseRow objects
            :param schema: A Schema object
            :param name: The name of the database
            :param id: The id of the database
            :param cover: The cover of the database
        """
        self.rows = []
        for row in data:
            if isinstance(row, DatabaseRow):
                self.rows.append(row)
            else:
                self.rows.append(DatabaseRow(row, schema = schema))
        self.schema = schema or self.rows[0].schema
        self.name = name
        self.id = id
        self.cover = cover
        self.columns = self.schema.labels()
        self.df = self.to_pandas()

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.rows[key]
        elif isinstance(key, str):
            return self.schema[key]
        elif isinstance(key, slice):
            return self.rows[key]
        elif isinstance(key, tuple):
            return self.rows[key[0]][key[1]]
        
    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.rows[key] = value
        elif isinstance(key, str):
            self.schema[key] = value
        elif isinstance(key, slice):
            self.rows[key] = value
        elif isinstance(key, tuple):
            self.rows[key[0]][key[1]] = value

    def to_pandas(self) -> pd.DataFrame:
        """
            Converts the database to a pandas DataFrame.
        """
        return pd.DataFrame([row.values for row in self.rows], columns = self.columns)

    def __repr__(self) -> str:
        return self.df.__repr__()

    def __str__(self) -> str:
        return self.df.__str__()

    @classmethod
    def from_pandas(cls, df: pd.DataFrame, schema: Optional["Schema"] = None) -> 'Database':
        """
            Creates a Database object from a pandas DataFrame.
            Infers the schema from the pandas DataFrame if no schema is provided.
        """
        if schema:
            return cls(df.to_dict('records'), schema = schema)
        else:
            return cls(df.to_dict('records'), schema = Schema.from_pandas(df))
        
