from turtle import title
from typing import List, Dict, Tuple, Optional, Any, TypeVar
from enum import Enum
from abc import ABC, abstractmethod
from collections import OrderedDict, defaultdict
import pandas
from .Connector import Connector
from .Types import *

class Schema:
    SUPPORTED_TYPES = ['title', 'rich_text', 'number', 'select', 'multi_select', 'date', 'people', 'file', 'checkbox', 'url', 'email', 'phone_number', 'formula', 'relation', 'rollup']
    TYPE_MAP = {'title': Title, 'text': RichText, 'rich_text': RichText, 'number': Number, 'select': Select, 'multi_select': MultiSelect, 'date': Date, 'people': People, 'file': File, 'checkbox': Checkbox, 'url': URL, 'email': Email, 'phone_number': PhoneNumber, 'formula': Formula, 'relation': Relation, 'rollup': Rollup}
    def __init__(self, labels: List[str] = None, types: Optional[List[str]] = None, objects = None, title_column = 0) -> None:
        """
            Create a DatabaseSchema object. Required when creating a new database in Notion.
            Properties are column datatypes in Notion. 
            See https://developers.notion.com/reference/database for more information.
            Properties MUST contain exactly ONE 'title' value, this maps to the title column.

            Can be initialized in one of three ways:
            :param labels: A list of column names
            :param types: Optional, a list of column types (Will infer 'text' if not provided)
            :param title_column: Optional, If types is not provided, the index of the title column, otherwise
            no effect. Defaults to 0.

            OR

            :param objects: A list of Schema objects

            Example:

            schema = Schema(['Store', 'City', 'State'])

            schema = Schema(['Name', 'Age', 'Favorite Color'], ['title', 'number', 'select'])
            
            schema = Schema(objects = [Title("User"), Number("Age"), Select("Favorite Color", options = ["Red", "Blue", "Green"])])

            Defaults to text objects.
            
            Supported datatypes: 
            title, 
            rich_text, 
            number, 
            select, 
            multi_select, 
            date, 
            people, 
            file, 
            checkbox, 
            url, 
            email, 
            phone_number, 
            formula, 
            relation, 
            rollup

            Example:
            DatabaseSchema(properties={'Name': 'title', 'Age': 'number', 'Favorite Color': 'select'})
        """

        self.properties = OrderedDict()
        if objects:
            self.properties = OrderedDict([(obj.name, obj) for obj in objects])
        else:
            if types:
                if len(labels) != len(types):
                    raise ValueError("Labels and types must be the same length.")
                for label, _type in zip(labels, types):
                    self.add(label, _type = _type)
            else:
                for i, label in enumerate(labels):
                    if i == title_column:
                        self.add(label, _type = "title")
                    else:
                        self.add(label)


    @classmethod
    def from_notion_db(cls, connector: Connector, db_id: str):
        """
            Create a DatabaseSchema object from an existing database in Notion.
            :param connector: A Connector object
            :param db_id: The database id
        """
        response = connector.get_db_schema(db_id)
        properties = response['properties']
        schema_objects = [ cls.TYPE_MAP[property['type']].from_notion_property(property) for property in properties.values() ]
        # for name, property in properties.items():
        #     schema_objects[name] = Schema.TYPE_MAP[property['type']].from_notion_property(property)
        return cls(objects = schema_objects)

    def labels(self):
        """
            Return a list of column names.
        """
        return list(self.properties.keys())
    
    def types(self):
        """
            Return a list of column types.
        """
        return [self.properties[name].type for name in self.properties]
    
    def objects(self):
        """
            Return a list of Schema objects.
        """
        return list(self.properties.values())


    def __getitem__(self, key):
        return self.properties[key]
    
    def __setitem__(self, key, value):
        self.properties[key] = value
        self._update()
        

    def add(self, name: str = None, _type: str = "text", object: Optional[Property] = None):
        """
            Add a new column to the schema.
            :param name: The name of the column
            :param _type: The type of the column. Defaults to 'text' 

            Can override the empty Schema object with:
            :param object: A Schema object
            """
        if name in self.properties:
            raise ValueError("Duplicate column name encountered.")
        if object: 
            self.properties[object.name] = object
        elif _type:
            self.properties[name] = self.TYPE_MAP[_type](name)
        else:
            raise ValueError("Must provide either a type or a Schema object.")
        self._update()

    def remove(self, column_name: str) -> None:
        """
            Remove a column from the schema.
            :param column_name: The name of the column to remove
        """
        if column_name not in self.properties:
            raise ValueError("Column name not found in properties.")
        
        del self.properties[column_name]
        self._update()
    
    def update_type(self, name, _type: Optional[str] = None, object: Optional[Any] = None):
        """
            Update the type of a column in the schema.
            :param name: The name of the column

            Must provide one of:
            :param _type: The type of the column 
            :param object: A Schema object
            """
        if object: 
            self.properties[name] = object
        elif _type:
            self.properties[name] = self.TYPE_MAP[_type](name)
        else:
            raise ValueError("Must provide either a type or a Schema object.")
        self._update()



    @classmethod
    def from_pandas(cls, df: pandas.core.frame.DataFrame, title_column: Any = None) -> 'Schema':
        """
            Create a DatabaseSchema object from a pandas DataFrame.
            The first column of the DataFrame will be the title column.
            All other columns will be of type 'rich_text' or 'number' depending on dtype.

            :param df: The DataFrame to create the schema from
        """
        title_column = title_column or df.columns[0]
        types = []
        labels = []
        for label, dtype in df.dtypes.items():
            if label == title_column:
                types.append('title')
            elif dtype == 'int64' or dtype == 'float64':
                types.append('number')
            else:
                types.append('rich_text')
            labels.append(label)
        return cls(labels, types, title_column = 0)

    def _update(self):
        """
            Update the schema to reflect changes.
        """
        self.columns = self.labels = list(self.properties.keys())
        if len(self.columns) != len(set(self.columns)):
            raise ValueError("Duplicate column names found.")
        title = None
        for label, object in self.properties.items():
            if isinstance(object, Title):
                title = label
                break
        if not title: Warning("No title column found. Please add a title column.")
        self.title = title
        # if not title: Warning("No title column found for schema. Unless \
        # one is provided, the first column will be used as the title column.")
        

    def __repr__(self):
        return f"NotionDB Schema Object: {str(self.properties)}"
    def __str__(self) -> str:
        return f"NotionDB Schema Object: {str(self.properties)}"
    


    def _check_props(self, props):
        titles = 0
        seen_labels = set()
        for key, value in props.items():
            if value not in self.SUPPORTED_TYPES:
                raise ValueError("Invalid property type.")
            if value == 'title':
                titles += 1
            if key in seen_labels:
                raise ValueError("Duplicate property label.")
            seen_labels.add(key)

        return titles == 1
