import unittest
from notiondb.SchemaProperty import SchemaProperty

class TestSchemaObject(unittest.TestCase):
    """ Tests based on following functionality
        Data class for all schema objects.

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

    Tests:
        - test_type_must_be_specified
        - test_name_or_id_must_be_specified
        - test_create_checkbox
        - test_create_select
        - test_create_schema_object_from_notion_response
        - test_update_config_of_schema_object
        - test_update_config_of_schema_object_2
    """

    def test_type_must_be_specified(self):
        """ Test that an error is raised if type is not specified """
        with self.assertRaises(ValueError):
            SchemaProperty()

    def test_name_or_id_must_be_specified(self):
        """ Test that an error is raised if name or id is not specified """
        with self.assertRaises(ValueError):
            SchemaProperty(type="checkbox")

    def test_create_checkbox(self):
        """ Test that a checkbox object is created correctly """
        checkbox = SchemaProperty(type="checkbox", name="In stock")
        self.assertEqual(checkbox.notion, {'name': 'In stock', 'type': 'checkbox', 'checkbox': {}})

    def test_create_select(self):
        """ Test that a select object is created correctly """
        select = SchemaProperty(type="select", name="Color", config={"options": ["red", "green", "blue"]})
        self.assertEqual(select.notion, {'name': 'Color', 'type': 'select', 'select': {'options': ['red', 'green', 'blue']}})

    def test_create_schema_object_from_notion_response(self):
        """ Test that a schema object is created correctly from a notion response """
        notion_response = {
            "id": "fk%5EY",
            "name": "In stock",
            "type": "checkbox",
            "checkbox": {}
        }
        schema_object = SchemaProperty(**notion_response)
        self.assertEqual(schema_object.notion, notion_response)

    def test_update_config_of_schema_object(self):
        """ Test that the config of a schema object can be updated """
        schema_object = SchemaProperty(type='number', name='Price')
        schema_object.config = {"format": "number"}
        self.assertEqual(schema_object.notion, {'name': 'Price', 'type': 'number', 'number': {'format': 'number'}})

    def test_update_config_of_schema_object_2(self):
        """ Test that the config of a schema object can be updated """
        schema_object = SchemaProperty(type='number', name='Price')
        schema_object["format"] = "number"
        self.assertEqual(schema_object.notion, {'name': 'Price', 'type': 'number', 'number': {'format': 'number'}})
    
if __name__ == '__main__':
    unittest.main()