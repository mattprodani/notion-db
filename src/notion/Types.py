from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional, Any, TypeVar, TYPE_CHECKING, Union
import json


if TYPE_CHECKING: pass




class Property(ABC):
    """
        Subclass for database property
    """
    @abstractmethod
    def __init__(self, type: str, name: str, config: dict = {}, id: Optional[str] = None) -> None:
        """Creates schema property object"""
        if id is not None: raise NotImplementedError("id is not implemented yet")
        self.type = type
        self.name = name
        self.prop = {"type": type, "name": name, type: config}

    @classmethod
    def from_notion_property(cls, property: Dict) -> 'Property':
        obj = cls(property["name"])
        obj.prop = property
        obj.name = property["name"]
        obj.type = property["type"]
        return obj

    def property_object(self) -> Dict:
        return self.prop

    def to_notion_prop(self):
        return self.prop

    def rename(self, new_name):
        self.name = new_name
        self.prop["name"] = new_name

    # @abstractmethod
    # def property_value(self, body) -> None:
    #     """ Creates notion property value object """
    #     return {self.type: body}

    def __getattr__(self, __name: str) -> Any:
        if __name in self.__dict__:
            return self.__dict__[__name]
        elif __name in self.prop[self.type]:
            return self.prop[self.type][__name]
        else:
            return {}

    def __repr__(self) -> str:
        return "Property:" + json.dumps(self.prop)


class RichTextObject:
    """
        Subclass for rich text object
    """
    def __init__(self, text: str, annotations: Dict[str, Any], plain_text: str, href: Optional[str] = None, link = None) -> None:
        """Creates rich text object"""
        self.type = "text"
        self.text = {"content": text, "link": link}
        self.annotations = annotations
        self.plain_text = plain_text or text
        self.href = href

    @classmethod
    def from_args(cls, **kwargs) -> 'RichTextObject':
        cls.annotations = {}
        cls.annotations["bold"] = kwargs.get("bold", False)
        cls.annotations["italic"] = kwargs.get("italic", False)
        cls.annotations["strikethrough"] = kwargs.get("strikethrough", False)
        cls.annotations["underline"] = kwargs.get("underline", False)
        cls.annotations["code"] = kwargs.get("code", False)
        cls.annotations["color"] = kwargs.get("color", "default")
        return cls(kwargs.get("text", ""), cls.annotations, kwargs.get("plain_text", ""), kwargs.get("href", None), kwargs.get("link", None))


    @classmethod
    def from_notion_rich_text(cls, rich_text: Dict) -> 'RichTextObject':
        text = rich_text["text"]
        annotations = rich_text["annotations"]
        plain_text = rich_text["plain_text"]
        href = rich_text.get("href", None)
        link = rich_text.get("link", None)
        return cls(text, annotations, plain_text, href)

    
    def rich_text_object(self) -> Dict:
        return self.__dict__
    def __repr__(self) -> str:
        return "RichTextObject:" + json.dumps({"text": self.text, "annotations": self.annotations, "plain_text": self.plain_text, "href": self.href})

    
class RichText(Property):
    """
        RichText property
        Usage: RichText().compile("Hello World!", bold = True, italic = True, underline = True, color = "red")
    """
    def __init__(self, name:str, id:Optional[str] = None) -> None:
        """
            Creates a RichText property. No args accepted.
        """
        super().__init__("rich_text", name, id = id)

    def property_value(self, text: str, href = None, bold = False, italic = False, strikethrough = False, underline = False, code = False, color = "default") -> None:
        annotations = {"bold": bold, "italic": italic, "strikethrough": strikethrough, "underline": underline, "code": code, "color": color}

        rto = RichTextObject(text, annotations, text, href)
        return super().property_value([rto.rich_text_object()])


class Text(Property):
    def __init__(self, name:str) -> None:
        super().__init__("text", name)
    
    def property_value(self, text: str) -> None:
        raise ValueError("Text property cannot be used as a value. See Notion API or use RichText instead.")
    

class Title(Property):
    def __init__(self, name:str) -> None:
        super().__init__("title", name)

    def property_value(self, text: str, bold = False, italic = False, strikethrough = False, underline = False, code = False, color = "default" ) -> None:
        annotations = {"bold": bold, "italic": italic, "strikethrough": strikethrough, "underline": underline, "code": code, "color": color}
        rto = RichTextObject(text, annotations, text)
        return super().property_value([rto.rich_text_object()])

    

class Number(Property):
    def __init__(self, name:str, format: str = "number") -> None:
        """ Number property  object.
            See https://developers.notion.com/reference/database for more information.

            :param format: The format of the number. Defaults to 'number'.
            format accepts the following values:
            number, number_with_commas, percent, dollar, canadian_dollar, euro, pound, yen, ruble, rupee, won, yuan, real, lira, rupiah, franc, hong_kong_dollar, new_zealand_dollar, krona, norwegian_krone, mexican_peso, rand, new_taiwan_dollar, danish_krone, zloty, baht, forint, koruna, shekel, chilean_peso, philippine_peso, dirham, colombian_peso, riyal, ringgit, leu
        """
        super().__init__("number", name, {"format": format})

    def property_value(self, number: float) -> None:
        return super().property_value(number)

class Status(Property):
    def __init__(self, name:str, options: List[str] = [], colors:Dict[str, str]= {}) -> None:
        """ Status property schema object.
            See https://developers.notion.com/reference/database for more information.

            :param options: A list of options for the status property.
        """
        options = [Status.status_option_object(option, colors.get(option, None)) for option in options]
        super().__init__("status", name, {"options": options})
    
    def property_value(self, option: str, color: Optional[str] = None) -> None:
        """ Creates a status property value object.
            See https://developers.notion.com/reference/page for more information.

            :param option: The selected option.
            :param color: The color of the selected option. Defaults to None.
        """
        return super().property_value(Status.status_option_object(option, color))
    
    @staticmethod
    def status_option_object(name: str, color: Optional[str] = None) -> Dict:
        return {"name": name, "color": color} if color is not None else {"name": name}

class Select(Property):

    def __init__(self, name:str, options: List[str] = [], colors: Dict[str, str] = {}) -> None:
        """ Select property schema object.
            See https://developers.notion.com/reference/database for more information.

            :param options: A list of options for the select property.
            :param colors: A dictionary of colors for each option. Defaults to empty.
        """
        options = [Select.select_option_object(option, colors.get(option, None)) for option in options]
        super().__init__("select", name, {"options": options})

    def property_value(self, option: str, color: Optional[str] = None) -> None:
        """ Creates a select property value object.
            See https://developers.notion.com/reference/page for more information.

            :param option: The selected option.
            :param color: The color of the selected option. Defaults to None.
        """
        return super().property_value(Select.select_option_object(option, color))

    @staticmethod
    def select_option_object(name: str, color: Optional[str] = None) -> Dict:
        return {"name": name, "color": color} if color is not None else {"name": name}
    

class MultiSelect(Property):
    def __init__(self, name:str, options: List[str] = [], colors:Dict[str, str]= {}) -> None:
        """ MultiSelect property schema object.
            See https://developers.notion.com/reference/database for more information.

            :param options: A list of options for the multiselect property.
        """
        options = [MultiSelect.multiselect_option_object(option, colors.get(option, None)) for option in options]
        super().__init__("multi_select", name, {"options": options})
    
    def property_value(self, option: Union[str, List[str]], color: Optional[str] = None) -> None:
        """ Creates a multiselect property value object.
            See https://developers.notion.com/reference/page for more information.

            :param option: The selected option.
            :param color: The color of the selected option. Defaults to None.
        """
        if isinstance(option, str):
            option = [option]
        return super().property_value([MultiSelect.multiselect_option_object(o, color) for o in option])

    
    @staticmethod
    def multiselect_option_object(name: str, color: Optional[str] = None) -> Dict:
        return {"name": name, "color": color} if color is not None else {"name": name}

class Date(Property):
    def __init__(self, name:str) -> None:
        super().__init__("date", name)
    
    def property_value(self, date: str) -> None:
        return super().property_value({"start": date})


class People(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("People property does not support configuration.")
        raise NotImplementedError("File property not yet implemented.")
        super().__init__("people")
    def compile(self, people: List[str]) -> None:
        raise NotImplementedError("People property not yet implemented.")
        return super().compile(people)
class File(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("File property does not support configuration.")
        raise NotImplementedError("File property not yet implemented.")
        super().__init__("file")
    def compile(self, file: str) -> None:
        raise NotImplementedError("File property not yet implemented.")
        return super().compile(file)

class Checkbox(Property):
    def __init__(self, name: str) -> None:
        super().__init__("checkbox", name)
        
    def compile(self, checked: bool) -> None:
        return super().compile(checked)

class URL(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("URL property does not support configuration.")
        raise NotImplementedError("File property not yet implemented.")
        super().__init__("url")
    def compile(self, url: str) -> None:
        return super().compile(url)

class Email(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("Email property does not support configuration.")
        raise NotImplementedError("File property not yet implemented.")
        super().__init__("email")
    def compile(self, email: str) -> None:
        return super().compile(email)

class PhoneNumber(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("PhoneNumber property does not support configuration.")
        raise NotImplementedError("File property not yet implemented.")
        super().__init__("phone_number")
    def compile(self, phone_number: str) -> None:
        return super().compile(phone_number)

class Formula(Property):
    def __init__(self, name: str, expression: str = None) -> None:
        """ Formula property schema object.
            See https://developers.notion.com/reference/database for more information.

            :param expression: The formula expression.
        """
        super().__init__("formula", {"expression": expression})

    def property_value(self, expression) -> None:
        """ Creates a formula property value object.
            See https://developers.notion.com/reference/page for more information.

            :param expression: The formula expression.
        """
        return super().property_value({"expression": expression})
        # THIS IS LIKELY NOT WORKING

class Relation(Property):
    def __init__(self, database_id: str, relation_type: str = None) -> None:
        """ Relation property schema object.
            See https://developers.notion.com/reference/database for more information.

            :param database_id: The ID of the database to link to.
            :param relation_type: The type of relation (single_property or dual_property). Defaults to None.

        """
        raise NotImplementedError("File property not yet implemented.")
        if relation_type not in [None, "single_property", "dual_property"]: raise ValueError("Invalid relation type.")
        if relation_type: super().__init__("relation", {"database_id": database_id, "relation_type": relation_type})
        else: super().__init__("relation", {"database_id": database_id})

class Rollup(Property):
    def __init__(self, relation_property_name: str, rollup_property_name: str, function: str) -> None:
        """ Rollup property schema object.
            See https://developers.notion.com/reference/database for more information.

            :param relation_property_name: The name of the relation property.
            :param rollup_property_name: The name of the rollup property.
            :param function: The function to use for the rollup. The function accepts the following values:
            count, count_values, count_unique_values, count_empty, count_not_empty, percent_empty, percent_not_empty, sum, average, median, min, max, range, formula
        """
        raise NotImplementedError("File property not yet implemented.")
        super().__init__("rollup", {"relation_property_name": relation_property_name, "rollup_property_name": rollup_property_name, "function": function})


class PropertyFactory:
    TYPE_MAP = {'title': Title, 'text': RichText, 'rich_text': RichText, 'number': Number, 'select': Select, 'multi_select': MultiSelect, 'date': Date, 'people': People, 'file': File, 'checkbox': Checkbox, 'url': URL, 'email': Email, 'phone_number': PhoneNumber, 'formula': Formula, 'relation': Relation, 'rollup': Rollup}


    @staticmethod
    def create_type(type, **kwargs):
        if type not in PropertyFactory.TYPE_MAP:
            raise ValueError("Invalid type: {}".format(type))
        return PropertyFactory.TYPE_MAP[type](**kwargs)
        