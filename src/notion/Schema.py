from typing import List, Dict, Tuple, Optional, Any, TypeVar, Union
from turtle import title
from enum import Enum
from abc import ABC, abstractmethod
from collections import OrderedDict, defaultdict
import pandas
from .Connector import Connector
from .Types import *

class Schema:
    """
        Schema objects are used to define the structure of a Notion Database.
        This class is used to create and maintain Schema objects which are used
        to create and update Notion Databases. 

        The simplest way to use this is by creating a Schema object from an existing
        Notion Database using the Schema.from_database() method.    

        If you want to create and maintain databases programatically then use the
        default initializer.

        These will allow you to use more advanced table features in Notion databases.
        At a minimum, the title property is required.

        See https://developers.notion.com/reference/database for more information.
        Properties MUST contain exactly ONE 'title' value, this maps to the title column.

        Args:
            labels (List[str], optional): list of column names. Defaults to None.
            types (Optional[List[str]], optional): list of types. Defaults to None.
            objects (Property, optional): Property schema object. Defaults to None.
            title_column (key, optional): index or key for title column. Defaults to 0.
        
        **Supported Types**: 
        text, 
        number, 
        title, 
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

        Can be initialized in one of two ways:
        
            1. Provide a list of labels and types (can provide title_column instead)
            2. Provide a list of Schema Property objects    


        Example:

            >>> schema = Schema(['Store', 'City', 'State'])
         
            >>> schema = Schema(['Store', 'City', 'State'], title_column = 0)
         
            >>> schema = Schema(['Name', 'Age', 'Favorite Color'], ['title', 'number', 'select'])
         
            >>> schema = Schema(objects = [Title("User"), Number("Age"), Select("Favorite Color", options = ["Red", "Blue", "Green"])])

        """

    _SUPPORTED_TYPES = ['title', 'rich_text', 'number', 'select', 'multi_select', 'date', 'people', 'file', 'checkbox', 'url', 'email', 'phone_number', 'formula', 'relation', 'rollup']
    _TYPE_MAP = {'title': Title, 'text': RichText, 'rich_text': RichText, 'number': Number, 'select': Select, 'multi_select': MultiSelect, 'date': Date, 'people': People, 'file': File, 'checkbox': Checkbox, 'url': URL, 'email': Email, 'phone_number': PhoneNumber, 'formula': Formula, 'relation': Relation, 'rollup': Rollup}
    def __init__(self, labels: List[str] = None, types: Optional[List[str]] = None, objects = None, title_column = 0) -> None:
        self.properties = OrderedDict()
        if objects:
            self.properties = OrderedDict([(obj.name, obj) for obj in objects])
        else:
            if types:
                if len(labels) != len(types):
                    raise ValueError("Labels and types must be the same length.")
                for label, _type in zip(labels, types):
                    self.add(label, datatype = _type)
            else:
                for i, label in enumerate(labels):
                    if i == title_column:
                        self.add(label, datatype = "title")
                    else:
                        self.add(label)


    @classmethod
    def from_database(cls, connector: Connector, db_id: str):
        """
        Creates a Schema object from an existing Notion database.
        Create a Connector object prior to calling this method.

        Args:
            connector (Connector): Connector object
            db_id (str): Notion database ID

        Returns:
            Schema: Schema object
        
        Raises:
            ValueError: If database ID not found
        
        Example:
            >>> connector = Connector("API_token")
            >>> schema = Schema.from_database(connector, "db_id")
            >>> schema
            Schema: {'Name': Title, 'Age': Number, 'Favorite Color': Select}

        """        
        response = connector.get_db_schema(db_id)
        properties = response['properties']
        schema_objects = [ cls._TYPE_MAP[property['type']].from_notion_property(property) for property in properties.values() ]
        # for name, property in properties.items():
        #     schema_objects[name] = Schema.TYPE_MAP[property['type']].from_notion_property(property)
        return cls(objects = schema_objects)





    @classmethod
    def from_pandas(cls, df, title_column: Any = None) -> 'Schema':
        """
            Creates a Schema by inferring objects from a pandas DataFrame.
            Infers only number and text columns. 

            Args: 
                df (pd.DataFrame): A pandas DataFrame
                title_column (Any): The column index to use as the title. Defaults to the first column.
            
            Returns:
                A Schema object
            
        """

        values = df.iloc[0].values
        types = cls._infer_from_values(values)
        title_column = 0 or title_column
        types[title_column] = "title"
        labels = df.columns
        return cls(labels, types)


    def add(self, name: str = None, datatype: str = "text", object: Optional[Property] = None):
        """Add a column to the schema.

        Can be added in one of two ways:
        1. Provide a name and datatype
        2. Provide a Schema Property object

        Args:
            name (str, optional): column name. Defaults to None.
            datatype (str, optional): property type. Defaults to "text".
            object (Property, optional): property object. Defaults to None.

        Raises:
            ValueError: Duplicate Column Names
            ValueError: No arguments provided
        
        """        

        if name in self.properties:
            raise ValueError("Duplicate column name encountered.")
        if object: 
            self.properties[object.name] = object
        elif datatype:
            self.properties[name] = self._TYPE_MAP[datatype](name)
        else:
            raise ValueError("Must provide either a type or a Schema object.")
        self._update()

    def remove(self, column_name: str) -> None:
        """Removes a column from the schema

        Args:
            column_name (str): column name to remove

        Raises:
            ValueError: If column name not found

        """
        if column_name not in self.properties:
            raise ValueError("Column name not found in properties.")
        
        del self.properties[column_name]
        self._update()
    
    def update_type(self, name:str, datatype: Union[str, Property], **kwargs):
        """Update the type of a column

        Args:
            name (str): 
            datatype (str or Property): New type of column
            **kwargs: Additional arguments to pass to the new Property object initializer
        
        Raises:
            ValueError: If the column name is not found
        
        Example:
            >>> schema = Schema(['Store', 'City', 'State'])
            >>> schema.update_type('Store', 'select', options = ['A', 'B', 'C'])

        """        
        if name not in self.properties:
            raise ValueError("Column name not found in properties.")
        if isinstance(datatype, str):
            self.properties[name] = self._TYPE_MAP[datatype](name, **kwargs)
        else:
            self.properties[name] = datatype
        self._update()


    def rename_column(self, old_name: str, new_name: str) -> None:
        """
            Rename a column in the schema.
            :param old_name: The current name of the column
            :param new_name: The new name of the column
        """
        if old_name not in self.properties:
            raise ValueError("Column name not found.")
        if new_name in self.properties:
            raise ValueError("Duplicate column name encountered.")
        self.properties[new_name] = self.properties.pop(old_name).rename(new_name)
        self._update()



    @property
    def labels(self):
        """
        Returns a list of column names.
        """
        return list(self.properties.keys())

    @property
    def types(self):
        """
        Returns a mapping of column names to column types.
        """
        return {name: self.properties[name].type for name in self.properties}
    
    @property
    def objects(self):
        """
        Returns a mapping of column names to column objects.
        """
        return self.properties



    @staticmethod
    def _infer_from_values(values):
        types = [Schema._infer(val) for val in values]


    @staticmethod
    def _infer(val):
        return "number" if isinstance(val, int) or isinstance(val, float) else "rich_text"

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
        



    def _check_props(self, props):
        titles = 0
        seen_labels = set()
        for key, value in props.items():
            if value not in self._SUPPORTED_TYPES:
                raise ValueError("Invalid property type.")
            if value == 'title':
                titles += 1
            if key in seen_labels:
                raise ValueError("Duplicate property label.")
            seen_labels.add(key)

        return titles == 1

    def __getitem__(self, key):
        return self.properties[key]
    
    def __setitem__(self, key, value):
        self.properties[key] = value
        self._update()
        
    
    def __repr__(self):
        return f"NotionDB Schema Object: {str(self.properties)}"
    def __str__(self) -> str:
        return f"NotionDB Schema Object: {str(self.properties)}"
    


    def _to_notion(self, name = None, parent_id = None, parent_type = None):
        # SHOULD REMOVE THIS
        properties = {}
        for name, property in self.properties.items():
            properties[name] = property.to_notion_prop()
        

        return {
            'properties': properties
        }