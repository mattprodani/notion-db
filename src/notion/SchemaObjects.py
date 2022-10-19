
from abc import ABC, abstractmethod
from dataclasses import dataclass


class SchemaObject(ABC):
    
        """ Data class for all schema objects.

            All schema objects have:
                - type (string)
                - name (string). Optional
                - id (string). Optional if name is specified
                - config (dict). Optional, type specific following Notion API
            
            For example, to create a 'checkbox' column called 'In stock':
                >>> SchemaObject(type="checkbox", name="In stock")
                {'name': 'In stock', 'type': 'checkbox', 'checkbox': {}}

            To create a 'select' column called 'Color' with options 'red', 'green', 'blue':
                >>> SchemaObject(type="select", name="Color", config={"options": ["red", "green", "blue"]})
                {'name': 'Color', 'type': 'select', 'select': {'options': ['red', 'green', 'blue']}}

            To create a schema object from a notion response:
                >>> notion_response 
                {   "id": "fk%5EY",
                    "name": "In stock",
                    "type": "checkbox",
                    "checkbox": {} }
                >>> SchemaObject(**notion_response)
                {'id': 'fk%5EY', 'name': 'In stock', 'type': 'checkbox', 'checkbox': {}}
            
            To update the config of a schema object:
                >>> schema_object = SchemaObject(type='number', name='Price')
                >>> schema_object.config = {"format": "number"}
                >>> schema_object
                {'name': 'Price', 'type': 'number', 'number': {'format': 'number'}}

            Or use:
                >>> schema_object["format"] = "number"
                >>> schema_object
                {'name': 'Price', 'type': 'number', 'number': {'format': 'number'}}

            
            JSON structure:
            {
                "id": "Column ID",
                "type": "Column Type",
                "name": "Column Name",
                "Column Type": {
                    "Column Type Configuration"
                }
            }
        
        """
    
        def __init__(self, **kwargs):
            if "type" not in kwargs:
                raise ValueError("type must be specified")
            if "name" not in kwargs and "id" not in kwargs:
                raise ValueError("name or id must be specified")
            
            self._obj = kwargs

            if "config" in kwargs:
                self._obj[self.type] = kwargs["config"]
                del self._obj["config"]
            
            self._obj[self.type] = self._obj.get(self.type, {})
        @property
        def type(self):
            """ Type of the column """
            return self._obj.get("type")

        @property
        def key(self):
            """ Returns id if exists, otherwise name """
            return self.id or self.name

        @property
        def id(self):
            """ ID of the column """
            return self._obj.get("id", None)

        @property
        def name(self):
            """ Name of the column """
            return self._obj.get("name", None)
            
        @property
        def config(self):
            """ Returns the configuration of the column """
            return self._obj[self.type]

        @config.setter
        def config(self, value):
            self._obj[self.type] = value

        @property
        def notion(self):
            """ Returns the notion representation of the column """
            return self._obj
    

        def __getitem__(self, key):
            return self._obj[self.type][key]
        
        def __setitem__(self, key, value):
            self._obj[self.type][key] = value
        def __str__(self):
            return f"ID - {self.id} {self.name} ({self.type}) - Config: {self.config}"
    
        def __repr__(self):
            return str(self._obj)

        def __hash__(self) -> int:
            return hash(self.id or self.name)
