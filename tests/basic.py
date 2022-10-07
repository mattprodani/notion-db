

# Schema

from notion import Schema
from notion.Types import *
from notion import DatabaseRow

def schema_tests():
    # Title provided
    types = ['title', 'rich_text', 'number', 'select', 'multi_select', 'date']
    labels = [str(i) for i in range(len(types))]

    s = Schema(labels = labels, types = types)

    assert s['0'].name == '0'
    assert s['0'].type == 'title'
    assert s['1'].name == '1'
    assert s['1'].type == 'rich_text'
    assert s['2'].name == '2'
    assert s['2'].type == 'number'
    assert s['3'].name == '3'
    assert s['3'].type == 'select'
    assert s['4'].name == '4'
    assert s['4'].type == 'multi_select'
    assert s['5'].name == '5'
    assert s['5'].type == 'date'
    

    # Check update type
    s.update_type('1', 'select')
    assert s['1'].type == 'select'

    

    s = None
    labels = None
    # Title not provided
    labels = [str(i) for i in range(len(types))]

    s = Schema(labels = labels, title_column=1)

    
    assert s['0'].name == '0'
    assert s['0'].type == 'rich_text'
    assert s['1'].name == '1'
    assert s['1'].type == 'title'

    # expected fail
    try:
        s['inv']
    except KeyError:
        pass
    else:
        assert False
    
    # Assume title 0
    s = Schema(labels = labels)

    assert s['0'].name == '0'
    assert s['0'].type == 'title'
    assert s['1'].name == '1'
    assert s['1'].type == 'rich_text'



    # More unit tests

    s = Schema(objects = [Title("User"), Number("Age"), Select("Favorite Color", options = ["Red", "Blue", "Green"])])

    assert s['User'].name == 'User'
    assert s['User'].type == 'title'
    assert s['Age'].name == 'Age'
    assert s['Age'].type == 'number'
    assert s['Favorite Color'].name == 'Favorite Color'
    assert s['Favorite Color'].type == 'select'

    s = None
    # Check update type
    s = Schema(objects = [Title("User"), Number("Age"), Select("Favorite Color", options = ["Red", "Blue", "Green"])])

    s.update_type('Favorite Color', 'multi_select')
    assert s['Favorite Color'].type == 'multi_select'

    # Check update options
    prev = s['Favorite Color'].options
    s.update_type('Favorite Color', 'select', options = ["Red", "Blue", "Purple", "Yellow"])
    assert prev != s['Favorite Color'].options

    # Check update options
    prev = s['Favorite Color'].options
    s.update_type(
        'Favorite Color',
        Select('Favorite Color', options = ["Red", "Blue", "Green", "Purple"])
    )
    assert prev != s['Favorite Color'].options    


def create_equality():
    # Check if all ways to create schema provide same compile result

    # Using labels and types
    types = ['title', 'rich_text', 'number', 'select', 'multi_select', 'date']
    labels = [str(i) for i in range(len(types))]
    s1 = Schema(labels = labels, types = types)

    # Using labels and property objects
    s2 = Schema(objects = [Title("0"), RichText("1"), Number("2"), Select("3"), MultiSelect("4"), Date("5")])

    # Create DatabaseRow using each schema
    data = {"0": "User", "1": "Hello", "2": 10, "3": "Red", "4": ["Red", "Blue"], "5": "2020-01-01"}
    r1 = DatabaseRow(data=data, schema=s1)
    r2 = DatabaseRow(data=data, schema=s2)

    # Check if both rows have the same notion_properties
    assert r1.notion_properties == r2.notion_properties
    print(r1.notion_properties)




    
schema_tests()
create_equality()