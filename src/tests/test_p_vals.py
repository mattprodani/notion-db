# from turtle import update
# import unittest

# from notion.PropertyValues import *

# # 
# TYPES = [TitlePropertyValue, RichTextPropertyValue, NumberPropertyValue, SelectPropertyValue, MultiSelectPropertyValue, DatePropertyValue, CheckboxPropertyValue, FormulaPropertyValue, RelationPropertyValue]


# class TestPvals(unittest.TestCase):
#     # test initialization for all types

#     def setUp(self) -> None:
#         self.typemap = {}
#         for typ in TYPES:
#             self.typemap[typ.__name__.replace("PropertyValue", "")] = typ


#     def test_init(self):
#         for name, typ in self.typemap.items():
#             with self.subTest(name + "_init_test"):
#                 pval = typ()
#                 self.assertEqual(pval.type.lower(), name.lower())


# class Title(unittest.TestCase):
#     def setUp(self) -> None:
#         self.maxDiff = 1000
#         self.obj_data = {
#             "type": "title",
#             "title": [
#                 {
#                     "type": "text",
#                     "text": {
#                         "content": "My first database",
#                         "link": None
#                     },
#                     "annotations": {
#                         "bold": True,
#                         "italic": False,
#                         "strikethrough": False,
#                         "underline": False,
#                         "code": False,
#                         "color": "red"
#                     },
#                     "plain_text": "My first database",
#                     "href": None
#                 }
#             ]}

#         self.obj_from_json = TitlePropertyValue.from_json(self.obj_data)
#         self.obj_from_init = TitlePropertyValue("My first database", bold = True, color = "red")


#     def test_from_json(self):
#         self.assertEqual(self.obj_from_json.title, self.obj_data["title"])
#         self.assertEqual(self.obj_from_json.to_notion(), self.obj_data)

#     def test_from_init(self):
#         self.assertEqual(self.obj_from_init.title, self.obj_data["title"])
#         self.assertEqual(self.obj_from_init.to_notion(), self.obj_data)

#     def test_from_init_with_custom_attr(self):
#         obj = TitlePropertyValue("My first database", bold = True, color = "red", custom_attr = "custom")
#         self.assertEqual(obj.custom_attr, "custom")
#         updated_data = self.obj_data.copy()
#         updated_data.update({"custom_attr": "custom"})
#         self.assertEqual(obj.to_notion(), updated_data)

#     def test_set_custom_attr(self):
#         self.obj_from_init.custom_attr = "custom"
#         updated_data = self.obj_data.copy()
#         updated_data.update({"custom_attr": "custom"})
#         self.assertEqual(self.obj_from_init.to_notion(), updated_data)
#         del self.obj_from_init.custom_attr

#     def test_set_title(self):
#         dummy = TitlePropertyValue(self.obj_from_init.to_notion())
#         dummy.update(text = "New title")
#         truth = self.obj_data.copy()
#         truth["title"][0]["text"]["content"] = "New title"
#         truth["title"][0]["plain_text"] = "New title"
#         self.assertEqual(dummy.to_notion(), truth)
    

        



# if __name__ == '__main__':
#     unittest.main()
