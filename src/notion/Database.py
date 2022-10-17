import pandas as pd
from typing import List, Dict, Tuple, Optional, Any, TypeVar, Union, TYPE_CHECKING
from .PropertyValues import _PropertyValueFactory, PropertyValue
from .Schema import Schema

if TYPE_CHECKING:
    from .Types import Property


class Row:
    """
    Database Row object for Notion API

    Creating a row:
    ===============

    Can be created in a few different ways:
    1. From a dictionary `data` that maps column names to values, as well as a list of `types` that maps column names to types
    Example:
        >>> row = Row(data = {"Name": "John", "Age": 20}, types = {"Name": "title", "Age": "number"})

    2. From a dictionary `data` that maps column names to Property Value objects
    Example:
        >>> row = Row({"Name": Title("John"), "Age": Number(20)})
    
    3. Using lists
    Example:
        >>> row = Row(data = ["John", 20], columns = ["Name", "Age"], types = ["title", "number"])
    
    4. An empty row can be created by passing no arguments
    
    Args:
        data (dict|list|series|Iterable, optional): 
            A dictionary that maps column names to values, or a dictionary that maps column names to Property Value objects, or a list of values, or a dataframe, or an iterable of values. Defaults to None.
        columns (list|dict, optional): 
            If `data` is a list, then `columns` is a list of column names. If `data` is a dictionary, then `columns` is a dictionary that maps column names to types. Defaults to None.
        types (list, optional): 
            A list or dict of types. Could be string or Property Schema objects. (This is useful when trying to update an existing database)
        title_column (str|int, optional): The column name or index that contains the title of the row. Defaults to 0.

    Raises:
        ValueError: If `data` is a dictionary, then `columns` must be a dictionary that maps column names to types.
        ValueError: If `data` is a list, then `columns` must be a list of column names.
        ValueError: If list size of `data` does not match the size of `columns`.

    Returns:
        Row: A row object that can be added to a database


    Modify or add to a row:
    =============

    To add or modify a row, simply set the value of a column to a new value.
    Example:
        >>> row = Row(data = {"Name": "John", "Age": 20}, types = {"Name": "title", "Age": "number"})
        >>> row["Name"] = "Jane"
        >>> row["Age"] = 25
        >>> row["Is Student"] = CheckboxPropertyValue(True)
        >>> row["Is Student"] = True # This will automatically infer the type
        >>> row
        {'Name': 'Jane', 'Age': 25, 'Is Student': True}

    To delete a column, use the `del` keyword or the `delete` method
    Example:
        >>> del row["Age"]
        >>> row.delete("Is Student")
        >>> row
        {'Name': 'Jane'}


    """
    def __init__(self, data = None, columns:List[str] = None, types: List[str] = None, title_column: Any = 0):

        data = data or {}

        if isinstance(data, list):
            if not isinstance(columns, list) or len(columns) != len(data):
                raise ValueError("Must provide a list of column names if data is a list")
            else:
                if title_column not in columns and isinstance(title_column, int):
                    title_column = columns[title_column]
                if types:
                    if len(types) != len(data):
                        raise ValueError("Length of types must match length of data")
                    types = dict(zip(columns, types))
                data = dict(zip(columns, data))
        if isinstance(data, pd.Series):
            data = data.to_dict()
        if isinstance(data, pd.DataFrame):
            data = data.iloc[0].to_dict()
        
        if types and not isinstance(types, dict):
                raise ValueError("Types must be a dictionary if data and columns are dictionaries")
        
        if not isinstance(data, dict): raise ValueError("Arguments provided are invalid")

        self.data = {}


        for key in data:
            if not types:
                type = "title" if key == title_column else None
            else:
                type = types[key]
            self._add(key, data[key], type)


    @property
    def value(self):
        """ Value representation of the row using underlying representation of the property values
            for readability and simplicity purposes.

            Example:
                >>> row = Row({"Name": "John", "Age": 20}, {"Name": "title", "Age": "number"})
                >>> row.value
                {"Name": "John", "Age": 20}

            As opposed to row.data which returns the PropertyValue objects
        """
        return {key: value.value for key, value in self.data.items()}


    @property
    def notion(self):
        """ Returns the notion representation of the row """
        obj = {}
        for key in self.data:
            obj[key] = self.data[key].notion
        return {"properties": obj}            

    def delete(self, key):
        """ 
            Delete a column from the row
        """

        if key in self.data:
            del self.data[key]
        else: 
            raise ValueError("Column does not exist")

    def to_pandas(self):
        """ 
            Convert the row to a Pandas series
        """
        return pd.Series(self.value)

    def __repr__(self):
        return str(self.data)
    
    def __str__(self):
        return self._tabulate()

    def _tabulate(self):
        return pd.Series(self.value).to_string()


    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            raise KeyError("Column does not exist")
    
    def __setitem__(self, key, value):
        if isinstance(value, PropertyValue):
            self.data[key] = value
        else:
            self._add(key, value)

    def __delitem__(self, key):
        del self.data[key]
    
    
    def __iter__(self):
        return iter(self.data)

        
    def _add(self, label, value, type = None):
        # if updating the title and type is not given, keep title and don't infer
        if label in self.data and self.data[label].type == 'title':
            type = type or 'title'

        if isinstance(value, PropertyValue):
            self.data[label] = value
        elif type:
            self.data[label] = _PropertyValueFactory.from_type(type, value)
        else:    
            self.data[label] = _PropertyValueFactory.infer_from_value(value)

        
        
# class Database:

#     def __init__(self, data, schema: Optional["Schema"] = None, name = None, id =  None, cover = None):
#         """
#             Creates a Database object.
#             :param data: A list of DatabaseRow objects
#             :param schema: A Schema object
#             :param name: The name of the database
#             :param id: The id of the database
#             :param cover: The cover of the database
#         """
#         self.rows = []
#         for row in data:
#             if isinstance(row, DatabaseRow):
#                 self.rows.append(row)
#             else:
#                 self.rows.append(DatabaseRow(row, schema = schema))
#         self.schema = schema or self.rows[0].schema
#         self.name = name
#         self.id = id
#         self.cover = cover
#         self.columns = self.schema.labels()
#         self.df = self.to_pandas()

#     def __getitem__(self, key):
#         if isinstance(key, int):
#             return self.rows[key]
#         elif isinstance(key, str):
#             return self.schema[key]
#         elif isinstance(key, slice):
#             return self.rows[key]
#         elif isinstance(key, tuple):
#             return self.rows[key[0]][key[1]]
        
#     def __setitem__(self, key, value):
#         if isinstance(key, int):
#             self.rows[key] = value
#         elif isinstance(key, str):
#             self.schema[key] = value
#         elif isinstance(key, slice):
#             self.rows[key] = value
#         elif isinstance(key, tuple):
#             self.rows[key[0]][key[1]] = value

#     def to_pandas(self) -> pd.DataFrame:
#         """
#             Converts the database to a pandas DataFrame.
#         """
#         return pd.DataFrame([row.values for row in self.rows], columns = self.columns)

#     def __repr__(self) -> str:
#         return self.df.__repr__()

#     def __str__(self) -> str:
#         return self.df.__str__()

#     @classmethod
#     def from_pandas(cls, df: pd.DataFrame, schema: Optional["Schema"] = None) -> 'Database':
#         """
#             Creates a Database object from a pandas DataFrame.
#             Infers the schema from the pandas DataFrame if no schema is provided.
#         """
#         if schema:
#             return cls(df.to_dict('records'), schema = schema)
#         else:
#             return cls(df.to_dict('records'), schema = Schema.from_pandas(df))
        
