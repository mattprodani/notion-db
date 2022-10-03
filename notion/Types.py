from datetime import datetime
from optparse import Option
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional, Any, TypeVar
import json

class Property(ABC):
    """
        Subclass for database property
    """
    @abstractmethod
    def __init__(self, type: str, config: Optional[Dict] = {}, id: Optional[str] = None) -> None:
        """Creates schema property object"""
        self.type = type
        self.config = config

    @abstractmethod
    def compile(self, body) -> None:
        """ Creates notion property value object """
        d = {}
        d.update(self.config)
        return {"type": self.type, self.type: body, **d}

    @classmethod
    def from_notion_property(cls, property: Dict) -> 'Property':
        return cls(property['type'], property[property['type']], property['id'])

    # @abstractmethod
    def __repr__(self) -> str:
        return json.dumps({"type": self.type, self.type: self.config})

    def update(self, property: Dict) -> None:
        self.config.update(property)
        if "type" in self.config:
            del self.config["type"]
        if self.type in self.config:
            del self.config[self.type]
        
        

class RichText(Property):
    """
        RichText property
        Usage: RichText().compile("Hello World!", bold = True, italic = True, underline = True, color = "red")
    """
    def __init__(self, **kwargs) -> None:
        """
            Creates a RichText property. No args accepted.
        """
        if len(kwargs) > 0: raise ValueError("Custom Rich Text not yet supported.")
        super().__init__("rich_text", kwargs)
    def __repr__(self) -> str:
        return super().__repr__()
    def compile(self, text: str, bold = False, italic = False, strikethrough = False, underline = False, code = False, color = "default" ) -> None:
        """Creates notion propert value provided text and formatting options"""
        annotations = {"bold": bold, "italic": italic, "strikethrough": strikethrough, "underline": underline, "code": code, "color": color}
        d = Text().compile(text, annotations)
        return super().compile([d])

class Text(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("Text property does not support configuration.")
        super().__init__("text")

    def __repr__(self) -> str:
        return super().__repr__()
    
    def compile(self, text: str, annotations = None) -> None:
        d = super().compile(body = {"content": text})
        if annotations: d["annotations"] = annotations
        return d

    
class Title(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("Title property does not support configuration.")
        super().__init__("title")

    def compile(self, text: str, bold = False, italic = False, strikethrough = False, underline = False, code = False, color = "default" ) -> None:
        annotations = {"bold": bold, "italic": italic, "strikethrough": strikethrough, "underline": underline, "code": code, "color": color}
        d = Text().compile(text, annotations)
        return super().compile([d])

    

class Number(Property):
    def __init__(self, format: str = "number") -> None:
        """ Number property schema object.
            See https://developers.notion.com/reference/database for more information.

            :param format: The format of the number. Defaults to 'number'.
            format accepts the following values:
            number, number_with_commas, percent, dollar, canadian_dollar, euro, pound, yen, ruble, rupee, won, yuan, real, lira, rupiah, franc, hong_kong_dollar, new_zealand_dollar, krona, norwegian_krone, mexican_peso, rand, new_taiwan_dollar, danish_krone, zloty, baht, forint, koruna, shekel, chilean_peso, philippine_peso, dirham, colombian_peso, riyal, ringgit, leu
        """
        # if format not in ["number", "percent", "dollar", "euro", "pound", "yen", "ruble", "rupee", "won", "yuan"]: raise ValueError("Invalid format.")
        super().__init__("number", {"format": format})

    def compile(self, body) -> None:
        return super().compile(body)

class Select(Property):
    def __init__(self, options: List[str], colors: Dict[str, str] = {}) -> None:
        """ Select property schema object.
            See https://developers.notion.com/reference/database for more information.

            :param options: A list of options for the select property.
            :param colors: A dictionary of colors for each option. Defaults to empty.
        """
        config = {}
        config["options"] = [{"name": option} if option not in colors else {"name": option, "color": colors[option]} for option in options]
        super().__init__("select", config)


    def compile(self, option) -> object:
        return super().compile({"name": option})

class MultiSelect(Select):
    def __init__(self, options: List[str], colors: Dict[str, str] = {}) -> None:
        """ MultiSelect property schema object.
            See https://developers.notion.com/reference/database for more information.

            :param options: A list of options for the select property.
            :param colors: A dictionary of colors for each option. Defaults to empty.
        """
        super().__init__(options, colors)
        self.type = "multi_select"

class Date(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("Date property does not support configuration.")
        super().__init__("date")

    def compile(self, start, end = None, time_zone = None) -> None:
        """ Date can be a string in ISO format or a datetime object. Time Zone is stnadard IANA format """
        if isinstance(start, datetime):
            start = start.isoformat()
        if isinstance(end, datetime):
            end = end.isoformat()
        body = {"start": start}
        if end: body["end"] = end
        if time_zone: body["time_zone"] = time_zone
        return super().compile(body)

class People(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("People property does not support configuration.")
        super().__init__("people")
    def compile(self, people: List[str]) -> None:
        raise NotImplementedError("People property not yet implemented.")
        return super().compile(people)
class File(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("File property does not support configuration.")
        super().__init__("file")
    def compile(self, file: str) -> None:
        raise NotImplementedError("File property not yet implemented.")
        return super().compile(file)

class Checkbox(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("Checkbox property does not support configuration.")
        super().__init__("checkbox")
    def compile(self, checked: bool) -> None:
        return super().compile(checked)

class URL(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("URL property does not support configuration.")
        super().__init__("url")
    def compile(self, url: str) -> None:
        return super().compile(url)

class Email(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("Email property does not support configuration.")
        super().__init__("email")
    def compile(self, email: str) -> None:
        return super().compile(email)

class PhoneNumber(Property):
    def __init__(self, **kwargs) -> None:
        if len(kwargs) > 0: raise ValueError("PhoneNumber property does not support configuration.")
        super().__init__("phone_number")
    def compile(self, phone_number: str) -> None:
        return super().compile(phone_number)

class Formula(Property):
    def __init__(self, expression: str) -> None:
        """ Formula property schema object.
            See https://developers.notion.com/reference/database for more information.

            :param expression: The formula expression.
        """
        super().__init__("formula", {"expression": expression})

class Relation(Property):
    def __init__(self, database_id: str, relation_type: str = None) -> None:
        """ Relation property schema object.
            See https://developers.notion.com/reference/database for more information.

            :param database_id: The ID of the database to link to.
            :param relation_type: The type of relation (single_property or dual_property). Defaults to None.

        """
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
        super().__init__("rollup", {"relation_property_name": relation_property_name, "rollup_property_name": rollup_property_name, "function": function})

