import unittest
from notiondb import Row 
from notiondb.PropertyValues import *
from notiondb.Schema import Schema

"""
Row tests for test-driven development

Functionality:


    - Creation
        - From dict of column names to values
        - From list of column names, list of values
        - From list of column names, list of values, list of types
        - From list of column names, list of values, title column
        - From dict of column names to Property Value objects
        - From dict of column names to values, schema object

    - Incorrect creation (should raise errors)
        - From list of column names, no values
        - Size mismatch between column names and values
        - Size mismatch between column names and types
        - Both types and property values or schema objects are provided
        
    - Updating (using indexing by column name)
        - Update a value with a string or int (should update the prop value)
        - Update a value with a Property Value object (should replace the prop value)

    - Inferring types
        - Numeric types should be inferred as numbers
        - Datetime types should be inferred as dates
        - String types should be inferred as text
        - Boolean types should be inferred as checkboxes
        - List types should be inferred as multi-selects


    - Adding a column
        - By indexing with a new column name and Property Value object or plain text
    
    - Deleting a column
        - Using delete() method with column name
        
    

    - Printing
        - Print the row


"""

class TestRow(unittest.TestCase):

    def setUp(self):
        # Schema will be tested separately
        self.example_value_dict = {
            "Name": "John",
            "Age": 20,
            "Height": 6.0,
            "Is Cool": True}
        self.example_value_list = ["John", 20, 6.0, True]
        self.example_column_list = ["Name", "Age", "Height", "Is Cool"]
        self.example_type_list = ["title", "number", "number", "checkbox"]
        self.example_title_column = "Name"
        self.example_value_object_dict = {
            "Name": TitlePropertyValue("John"),
            "Age": NumberPropertyValue(20),
            "Height": NumberPropertyValue(6.0),
            "Is Cool": CheckboxPropertyValue(True)}
        self.example_schema = Schema(self.example_column_list, self.example_type_list)
        
    def test_creation_from_dict(self):
        row = Row(self.example_value_dict)
        self.assertEqual(row["Name"].value, "John")
        self.assertEqual(row["Age"].value, 20)
        self.assertEqual(row["Height"].value, 6.0)
        self.assertEqual(row["Is Cool"].value, True)
    
    def test_creation_from_list(self):
        row = Row(self.example_value_list, self.example_column_list)
        self.assertEqual(row["Name"].value, "John")
        self.assertEqual(row["Age"].value, 20)
        self.assertEqual(row["Height"].value, 6.0)
        self.assertEqual(row["Is Cool"].value, True)
    
    def test_creation_from_list_with_types(self):
        row = Row(self.example_value_list, self.example_column_list, self.example_type_list)
        self.assertEqual(row["Name"].value, "John")
        self.assertEqual(row["Age"].value, 20)
        self.assertEqual(row["Height"].value, 6.0)
        self.assertEqual(row["Is Cool"].value, True)
    
    def test_creation_from_list_with_title_column_key(self):
        row = Row(self.example_value_list, self.example_column_list, title_column = self.example_title_column)
        self.assertEqual(row["Name"].value, "John")
        self.assertEqual(row["Age"].value, 20)
        self.assertEqual(row["Height"].value, 6.0)
        self.assertEqual(row["Is Cool"].value, True)
        self.assertEqual(row["Name"].type, "title")

    def test_creation_from_list_with_title_column_index(self):
        row = Row(self.example_value_list, self.example_column_list, title_column = 0)
        self.assertEqual(row["Name"].value, "John")
        self.assertEqual(row["Age"].value, 20)
        self.assertEqual(row["Height"].value, 6.0)
        self.assertEqual(row["Is Cool"].value, True)
        self.assertEqual(row["Name"].type, "title")
    
    def test_creation_from_dict_with_value_objects(self):
        row = Row(self.example_value_object_dict)
        self.assertEqual(row["Name"].value, "John")
        self.assertEqual(row["Age"].value, 20)
        self.assertEqual(row["Height"].value, 6.0)
        self.assertEqual(row["Is Cool"].value, True)
    
    def test_creation_from_dict_with_schema(self):
        pass

    def test_creation_from_list_with_no_values(self):
        with self.assertRaises(ValueError):
            row = Row(self.example_column_list)

    def test_creation_from_list_with_size_mismatch(self):
        with self.assertRaises(ValueError):
            row = Row(self.example_value_list, self.example_column_list[:-1])
        with self.assertRaises(ValueError):
            row = Row(self.example_value_list[:-1], self.example_column_list)
    
    def test_creation_from_list_with_size_mismatch_with_types(self):
        with self.assertRaises(ValueError):
            row = Row(self.example_value_list, self.example_column_list[:-1], self.example_type_list)
        with self.assertRaises(ValueError):
            row = Row(self.example_value_list[:-1], self.example_column_list, self.example_type_list)
        with self.assertRaises(ValueError):
            row = Row(self.example_value_list, self.example_column_list, self.example_type_list[:-1])


    def test_update_title_with_string(self):
        row = Row(self.example_value_dict, title_column="Name")
        row["Name"] = "Jane"
        self.assertEqual(row["Name"].value, "Jane")
        self.assertEqual(row["Name"].type, "title")
    
    def test_update_text_with_string(self):
        row = Row(self.example_value_dict)
        row["Name"] = "Jane"
        self.assertEqual(row["Name"].value, "Jane")
        self.assertEqual(row["Name"].type, "rich_text")
    
    def test_update_with_int(self):
        row = Row(self.example_value_dict)
        row["Name"] = 20
        self.assertEqual(row["Name"].type, "number")
        self.assertEqual(row["Name"].value, 20)

    def test_update_with_value_object(self):
        row = Row(self.example_value_dict)
        row["Name"] = TitlePropertyValue("Jane")
        self.assertEqual(row["Name"].value, "Jane")
        self.assertEqual(row["Name"].type, "title")
    
    def test_type_inference_from_init(self):
        row = Row(self.example_value_dict, title_column = "Name")
        self.assertEqual(row["Name"].type, "title")
        self.assertEqual(row["Age"].type, "number")
        self.assertEqual(row["Height"].type, "number")
        self.assertEqual(row["Is Cool"].type, "checkbox")

    def test_delete(self):
        row = Row(self.example_value_dict)
        del row["Name"]
        with self.assertRaises(KeyError):
            row["Name"]
        row.delete("Age")
        with self.assertRaises(KeyError):
            row["Age"]

    def test_type_inference_from_update(self):
        row = Row(self.example_value_dict)
        row["Name"] = 20
        self.assertEqual(row["Name"].type, "number")
        row["Name"] = True
        self.assertEqual(row["Name"].type, "checkbox")
        row["Name"] = 6.0
        self.assertEqual(row["Name"].type, "number")
        row["Name"] = "Jane"
        self.assertEqual(row["Name"].type, "rich_text")
    

    def test_add_column_using_getitem(self):
        row = Row(self.example_value_dict)
        row["Weight"] = 150
        self.assertEqual(row["Weight"].value, 150)
        self.assertEqual(row["Weight"].type, "number")
    
    def test_add_column_using_getitem_with_value_object(self):
        row = Row(self.example_value_dict)
        row["Weight"] = NumberPropertyValue(150)
        self.assertEqual(row["Weight"].value, 150)
        self.assertEqual(row["Weight"].type, "number")
    
    def test_multi_select_inference_from_list(self):
        row = Row(self.example_value_dict)
        row["Name"] = ["A", "B"]
        self.assertEqual(row["Name"].type, "multi_select")

    def test_date_inference_from_datetime(self):
        row = Row(self.example_value_dict)
        row["Name"] = datetime.now()
        self.assertEqual(row["Name"].type, "date")
    
    def test_print(self):
        row = Row(self.example_value_dict)
        self.assertIsInstance(str(row), str)
        self.assertGreater(len(str(row)), 0)

    def test_len(self):
        row = Row(self.example_value_dict)
        self.assertEqual(len(row), 4)

    def test_empty_row(self):
        row = Row()
        self.assertEqual(len(row), 0)

    def test_methods_with_empty_row(self):
        # Just tests that these methods don't throw errors
        row = Row()
        self.assertEqual(len(row), 0)
        self.assertIsInstance(str(row), str)
        row.value
        row.to_pandas()
        row["Name"] = "John"
        self.assertEqual(len(row), 1)
        self.assertEqual(row["Name"].value, "John")
        
    def test_notion_repr(self):
        row = Row(self.example_value_dict)
        self.assertIsInstance(row.notion, dict)
        self.assertEqual(row.notion["properties"]["Name"]["type"], "rich_text")


    def test_from_schema(self):
        row = Row.from_schema(self.example_value_dict, self.example_schema)
        self.assertIsInstance(row, Row)
        self.assertEqual(len(row), 4)
        self.assertEqual(row["Name"].type, "title")
        self.assertEqual(row["Age"].type, "number")
        self.assertEqual(row["Height"].type, "number")
        self.assertEqual(row["Is Cool"].type, "checkbox")

if __name__ == "__main__":
    unittest.main()