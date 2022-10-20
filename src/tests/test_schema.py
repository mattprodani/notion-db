import unittest
from notiondb.Schema import Schema

class TestSchema(unittest.TestCase):
    """ 
        Tests for Schema class
    """

    def test_create_from_dict(self):
        schema = Schema({"Name": "title", "Age": "number"})
        self.assertEqual(schema.labels, ["Name", "Age"])
        self.assertEqual(schema.types, ["title", "number"])

    def test_create_from_list(self):
        schema = Schema(["Name", "Age"], ["title", "number"])
        self.assertEqual(schema.labels, ["Name", "Age"])
        self.assertEqual(schema.types, ["title", "number"])

    def test_create_from_list_no_types(self):
        with self.assertRaises(ValueError):
            schema = Schema(["Name", "Age"])

    def test_create_from_list_wrong_size(self):
        with self.assertRaises(ValueError):
            schema = Schema(["Name", "Age"], ["title", "number", "checkbox"])

    def test_add_column(self):
        schema = Schema({"Name": "title", "Age": "number"})
        schema["Is Student"] = "checkbox"
        self.assertEqual(schema.labels, ["Name", "Age", "Is Student"])
        self.assertEqual(schema.types, ["title", "number", "checkbox"])

    def test_update_column(self):
        schema = Schema({"Name": "title", "Salary": "number"})
        schema["Salary"]["format"] = "dollar"
        self.assertEqual(schema.labels, ["Name", "Salary"])
        self.assertEqual(schema.types, ["title", "number"])
        self.assertEqual(schema["Salary"]["format"], "dollar")

    def test_delete_column(self):
        schema = Schema({"Name": "title", "Salary": "number"})
        del schema["Salary"]
        self.assertEqual(schema.labels, ["Name"])
        self.assertEqual(schema.types, ["title"])

    def test_from_notion(self):
        schema = Schema.from_notion({
            "properties": {
                "Name": {
                    "name": "Name",
                    "type": "title",
                    "title": {}
                },
                "Salary": {
                    "name": "Salary",
                    "type": "number",
                    "number": {
                        "format": "dollar"
                        }
                }
            }
        })
        self.assertEqual(schema.labels, ["Name", "Salary"])
        self.assertEqual(schema.types, ["title", "number"])
        self.assertEqual(schema["Salary"]["format"], "dollar")
    

if __name__ == '__main__':
    unittest.main()
