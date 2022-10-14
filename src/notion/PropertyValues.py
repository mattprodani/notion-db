from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional, Any, TypeVar, TYPE_CHECKING, Union
from .Types import RichTextObject
import json

if TYPE_CHECKING: pass


# class PropertyValueFactory:
#     """
#         Factory for creating PropertyValue objects
#     """
#     @staticmethod
#     def create_property_value(name: str, value: Any) -> "PropertyValue":
#         """
#             Creates a PropertyValue object
#             :param name: The name of the property
#             :param value: The value of the property
#         """
#         if isinstance(value, RichTextObject):
#             return RichTextPropertyValue(name, value)
#         elif isinstance(value, list):
#             if all(isinstance(item, RichTextObject) for item in value):
#                 return RichTextListPropertyValue(name, value)
#             elif all(isinstance(item, str) for item in value):
#                 return TitlePropertyValue(name, value)
#             elif all(isinstance(item, dict) for item in value):
#                 return MultiSelectPropertyValue(name, value)
#             else:
#                 raise ValueError("Invalid value type")
#         elif isinstance(value, str):
#             return TitlePropertyValue(name, value)
#         elif isinstance(value, dict):
#             return SelectPropertyValue(name, value)
#         elif isinstance(value, bool):
#             return CheckboxPropertyValue(name, value)
#         elif isinstance(value, datetime):
#             return DatePropertyValue(name, value)
#         elif isinstance(value, int):
#             return NumberPropertyValue(name, value)
#         elif isinstance(value, float):
#             return NumberPropertyValue(name, value)
#         else:
#             raise ValueError("Invalid value type")

#     @staticmethod
#     def from_notion(notion: Dict) -> "PropertyValue":
#         """
#             Creates a property value from a dictionary.
#             :param notion: The dictionary
#         """
#         name = notion["name"]
#         value = notion["value"]
#         if "rich_text" in value:
#             return RichTextPropertyValue.from_json(name, value)
#         elif "title" in value:
#             return TitlePropertyValue.from_json(name, value)
#         elif "select" in value:
#             return SelectPropertyValue.from_json(name, value)
#         elif "multi_select" in value:
#             return MultiSelectPropertyValue.from_json(name, value)
#         elif "checkbox" in value:
#             return CheckboxPropertyValue.from_json(name, value)
#         elif "date" in value:
#             return DatePropertyValue.from_json(name, value)
#         elif "number" in value:
#             return NumberPropertyValue.from_json(name, value)
#         elif "relation" in value:
#             return RelationPropertyValue.from_json(name, value)
#         elif "rollup" in value:
#             return RollupPropertyValue.from_json(name, value)
#         elif "files" in value:
#             return FilesPropertyValue.from_json(name, value)
#         elif "people" in value:
#             return PeoplePropertyValue.from_json(name, value)
#         elif "formula" in value:
#             return FormulaPropertyValue.from_json(name, value)
#         elif "created_time" in value:
#             return CreatedTimePropertyValue.from_json(name, value)
#         elif "created_by" in value:
#             return CreatedByPropertyValue.from_json(name, value)
#         elif "last_edited_time" in value:
#             return LastEditedTimePropertyValue.from_json(name, value)
#         elif "last_edited_by" in value:
#             return LastEditedByPropertyValue.from_json(name, value)
#         elif "url" in value:
#             return URLPropertyValue.from_json(name, value)
#         else:
#             raise ValueError("Invalid property value")

class PropertyValue(ABC):
    """
    Base class for all Property Values.

    Contains all properties held by the property value.
    """

    @abstractmethod
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if value is not None: setattr(self, key, value)

    
    @classmethod
    def from_json(cls, json: Dict) -> "PropertyValue":
        """
            Creates a property value from a JSON object.
            :param json: The JSON object
        """
        return cls(raw = json)

    @classmethod
    def from_notion(cls, json: Dict):
        """
            Creates a property value from a JSON object.
            Alias for from_json.
            :param json: The JSON object
        """
        return cls.from_json(json)


    @abstractmethod
    def update(self, value: Any) -> None:
        """

            Updates the property value.
            :param value: The new value
        """
        pass


    def to_json(self) -> Dict:
        """
            Returns the property value as a JSON object.
        """
        return self.__dict__


    def to_dict(self) -> Dict:
        """
            Returns the property value as a dictionary.
        """
        return self.__dict__
    
    def to_notion(self) -> Dict:
        """
            Returns the property value as a dictionary.
            Alias for to_dict.
        """
        return self.to_dict()

    def __str__(self) -> str:
        """
            Returns the string representation of the property value.
        """
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        """
            Checks if the property value is equal to another property value.
            :param other: The other property value
        """
        return self.__str__ == other.__str__ and self.__class__ == other.__class__

    @abstractmethod
    def __repr__(self) -> str:
        """
            Returns the string representation of the property value.
        """
        pass    


class TitlePropertyValue(PropertyValue):
    """
    Title property value.

    Args:
        text (str, optional): text. Defaults to "".
        id (str, optional): id. Defaults to None.
        bold (bool, optional): bold. Defaults to False.
        italic (bool, optional): italic. Defaults to False.
        strikethrough (bool, optional): strikethrough. Defaults to False.
        underline (bool, optional): underline. Defaults to False.
        code (bool, optional): code. Defaults to False.
        color (str, optional): color. Defaults to "default".
        raw (obj, optional): Used only for json-based initialization. Defaults to None.

    Returns:
            TitlePropertyValue: Title property value object.
    
    Example:
        >>> title = TitlePropertyValue("Hello World")
        >>> title
        Hello World
        >>> title.to_notion()
        {'title': [{'text': {'content': 'Hello World'}}]}
        >>> title.bold = True
        >>> title.to_notion()
        {'title': [{'text': {'content': 'Hello World', 'link': None, 'annotations': {'bold': True, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}}}]}
        >>> title.update("Hello World 2")
        >>> title.link_to("https://google.com")
    
    """        

    def __init__(self,  text: str = "", id = None, bold = False, italic = False, strikethrough = False, underline = False, code = False, color = "default", raw = None, **kwargs) -> None:
        if raw: return super().__init__(**raw)
        annotations = {"bold": bold, "italic": italic, "strikethrough": strikethrough, "underline": underline, "code": code, "color": color}
        rto = RichTextObject(text, annotations, text)
        return super().__init__(type = "title", id = id, title = [rto.rich_text_object()], **kwargs)

    def update(self, text: str, **kwargs) -> None:
        """_summary_: Updates the title property value.

        Args:
            text (str): new text to update the title property value with.
            **kwargs: additional arguments to pass to the Rich Text Object, such as bold, italic, etc.

        Example:
            >>> title = TitlePropertyValue("Hello World")
            >>> title
            Hello World
            >>> title.update("Hello World 2")
            >>> title
            Hello World 2

        """
        raise NotImplementedError("Title property values cannot be updated.")
        

    def __repr__(self) -> str:
        """
            Returns the string representation of the title property value.
        """
        return self.title[0]["plain_text"]

    



class RichTextPropertyValue(PropertyValue):        
    """
        Rich Text Property Value Object.

        :param text: Input text to display
        :type text: str, optional
        :param id: id, defaults to None
        :type id: str, optional
        :param bold: bold, defaults to False
        :type bold: bool, optional
        :param italic: italic, defaults to False
        :type italic: bool, optional
        :param strikethrough: strikethrough, defaults to False
        :type strikethrough: bool, optional
        :param underline: underline, defaults to False
        :type underline: bool, optional
        :param code: code, defaults to False
        :type code: bool, optional
        :param color: color, defaults to "default"
        :type color: str, optional
        :param raw: object for json intialization, defaults to None
        :type raw: obj, optional
        :return: RichTextPropertyValue
        :rtype: RichTextPropertyValue

        Example:
            >>> rich_text = RichTextPropertyValue("Hello World")
            >>> rich_text
            Hello World
            >>> rich_text.to_notion()
            {'rich_text': [{'text': {'content': 'Hello World'}}]}

        """

    def __init__(self, text: str = None, id = None, bold = False, italic = False, strikethrough = False, underline = False, code = False, color = "default", raw = None) -> None:

        if raw: return super().__init__(**raw)

        annotations = {"bold": bold, "italic": italic, "strikethrough": strikethrough, "underline": underline, "code": code, "color": color}
        rto = RichTextObject(text, annotations, text)
        return super().__init__(type = "rich_text", id = id, rich_text = [rto.rich_text_object()])

    def update(self, text: Any, **kwargs) -> None:
        """Updates the rich text property value.

        Args:
            text (str): text to update the rich text property value with.
            **kwargs: additional arguments to pass to the Rich Text Object, such as bold, italic, etc.

        """        
        raise NotImplementedError("Rich text property values cannot be updated.")


    def __repr__(self) -> str:
        """Returns the string representation of the rich text property value."""
        return self.rich_text[0]["plain_text"]


class SelectPropertyValue(PropertyValue):
    """Initializes a select property value.

    Args:
        name (str): name of the select option.
        color (str, optional): color option. Defaults to None.
        id (str, optional): property_value_id. Defaults to None.

    Returns:
        SelectPropertyValue: Select property value object.

    Example:
        >>> select = SelectPropertyValue("Option 1")
        >>> select
        Option 1
        >>> select.to_notion()
        {'select': {'name': 'Option 1'}}
    """            

    def __init__(self, name: str, color: str = None, id: str = None, raw: Dict = None) -> None:
        if raw: return super().__init__(**raw)

        return super().__init__(type = "select", id = id, select = self._select_option_object(name, color))


    def update(self, name: str = None, color: str = None) -> None:
        """Updates the select property value arguments.

        Args:
            name (str, optional): name of option. Defaults to None.
            color (str, optional): color type. Defaults to None.
        
        Example:
            >>> select = SelectPropertyValue("Option 1")
            >>> select
            Option 1
            >>> select.update("Option 2")
            >>> select
            Option 2
        """        

        if name is not None:
            self.select["name"] = name
        if color is not None:
            self.select["color"] = color
        

    def __repr__(self) -> str:
        """
            Returns the string representation of the select property value.
        """
        return self.select["name"]



    @staticmethod
    def _select_option_object(name: str, color: Optional[str] = None) -> Dict:
        """Object to represent a select option."""
        return {"name": name, "color": color} if color is not None else {"name": name}

class MultiSelectPropertyValue(PropertyValue):
    """Similar to SelectPropertyValue, but allows for multiple options to be selected.

    Args:
        names (List[str]): list of names of the select options.
        colors (List[str], optional): list of colors of the select options. Defaults to None. **Note**: currently not supported.
        id (str, optional): property_value_id. Defaults to None.
    
    Returns:
        MultiSelectPropertyValue: MultiSelect property value object.

    Example:
        >>> multi_select = MultiSelectPropertyValue(["Option 1", "Option 2"])
        >>> multi_select
        ['Option 1', 'Option 2']
    """    

    def __init__(self, names: List[str], id = None, raw = None) -> None:
        if raw: return super().__init__(**raw)
        return super().__init__(type = "multi_select", id = id, multi_select = [{"name": name} for name in names])


    def update(self, names: List[str]) -> None:
        """Updates the multi_select property value.

        Args:
            names (List[str]): new list of options to update the multi_select property value with.
        """        
        if isinstance(names, str): names = [names]
        self.multi_select = [{"name": name} for name in names]


    def __repr__(self) -> str:
        """
            Returns the string representation of the multi-select property value.
        """
        return ", ".join([option["name"] for option in self.multi_select])


class NumberPropertyValue(PropertyValue):
    """Number property value object.

    Create a number object. Either pass in a number or a string that can be converted to a number.
    Will convert to a float if a string is passed in.

    Note: 
        Options such as number format are provided to the parent schema object and not the property value.
        They apply to the whole database column

    Args:
        number (numeric): number to initialize the number property value with.
        id (str, optional): property_value_id. Defaults to None.

    Returns:
        NumberPropertyValue: Number property value object.
    
    Example:
        >>> number = NumberPropertyValue(1)
        >>> number
        1
        >>> number.to_notion()
        {'number': 1.0}

    """    
    def __init__(self, number: float, id = None, raw = None) -> None:
        """
            Initializes the number property value.
            :param number: The number
        """
        if raw: return super().__init__(**raw)
        if isinstance(number, str): number = float(number)
        return super().__init__(type = "number", id = id, number = number)

    def update(self, number) -> None:
        """Updates number object

        Args:
            number (numeric): new number
        """        
        if isinstance(number, str): number = float(number)
        self.number = number

    def __repr__(self) -> str:
        """
            Returns the string representation of the number property value.
        """
        return str(self.number)


class DatePropertyValue(PropertyValue):
    """Date property value object.

    Notion's date supports only iso8601 format. 
    The initializer expects either a string or a datetime object.
    If a string is passed in, no conversion or validation is done.

    Args:
        start (str or datetime): date to initialize the date property value with.
        end (str or datetime, optional): end date. Defaults to None.
        timezone (str, optional): timezone according to Notion timezone str. Defaults to None. Example: "America/Los_Angeles"
        id (str, optional): property_value_id. Defaults to None.

    Returns:
        DatePropertyValue: Date property value object.
    
    """    
    def __init__(self, start: Union[str, "datetime"], end: Union[str, "datetime"] = None, 
    timezone: str = None, id = None, raw = None) -> None:
        if raw: return super().__init__(**raw)

        if isinstance(start, datetime): start = start.isoformat()
        if isinstance(end, datetime): end = end.isoformat()
        return super().__init__(type = "date", id = id, date = {"start": start, "end": end, "timezone": timezone})


    def update(self, start: Union[str, "datetime"] = None, end: Union[str, "datetime"] = None, timezone: str = None) -> None:
        """Updates properties of the date property value.

        Args:
            start (Union[str, datetime], optional): start date. Defaults to None.
            end (Union[str, datetime], optional): end date. Defaults to None.
            timezone (str, optional): timezone. Defaults to None.
        """        

        if start is not None:
            if isinstance(start, datetime): start = start.isoformat()
            self.date["start"] = start
        if end is not None:
            if isinstance(end, datetime): end = end.isoformat()
            self.date["end"] = end
        if timezone is not None:
            self.date["timezone"] = timezone
        


    def __repr__(self) -> str:
        """
            Returns the string representation of the date property value.
        """
        s = ""
        if self.date["timezone"] is not None:
            s += self.date["timezone"] + " "
        s += self.date["start"]
        if self.date["end"] is not None:
            s += " to " + self.date["end"]

        return s

class FormulaPropertyValue(PropertyValue):
    """
        Formula property value.

        Only accepts a formula attribute, no other attributes are allowed.

        Args:
            formula (str): formula to initialize the formula property value with.
            id (str, optional): property_value_id. Defaults to None.
        
        Returns:
            FormulaPropertyValue: Formula property value object.
        
        Example:
            >>> formula = FormulaPropertyValue("=1+1")
            >>> formula
            '=1+1'
    """

    def __init__(self, formula: PropertyValue, id = None, raw = None) -> None:
        if raw: return super().__init__(**raw)

        return super().__init__(type = "formula", id = id, formula = formula)


    def update(self, formula: str) -> None:
        """
            Updates the formula property value.

            Args:
                formula (str): new formula to update the formula property value with.
        """
        self.formula = formula

    def __repr__(self) -> str:
        """
            Returns the string representation of the formula property value.
        """
        return self.formula.__repr__()


class RelationPropertyValue(PropertyValue):
    def __init__(self, **kwargs):
        raise NotImplementedError("RelationPropertyValue is not implemented yet.")



class CheckboxPropertyValue(PropertyValue):
    """ 
    Checkbox property value object.

    Args:
        checked (bool): checked to initialize the checkbox property value with.
        id (str, optional): property_value_id. Defaults to None.
    
    Returns:
        CheckboxPropertyValue: Checkbox property value object.
    
    Example:
        >>> checkbox = CheckboxPropertyValue(True)
        >>> checkbox
        True
    """    

    def __init__(self, checked: bool, raw = None, **kwargs):
        if raw: return super().__init__(**raw)
        return super().__init__(type = "checkbox", checkbox = checked, **kwargs)

    def update(self, checked: bool) -> None:
        self.checkbox = checked
    
    def __repr__(self) -> str:
        return str(self.checkbox)