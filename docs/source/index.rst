Notion-DB
=============
Notion-DB is a powerful object-oriented client for the Notion API that
allows you to easily access and work with notion Databases.
Learn how to use it and create your own Notion integrations in minutes!


.. toctree::
   :maxdepth: 5

   notiondb
   readme

Installation
------------
Install the package using pip:
    pip install notion-toolkit


Usage
-----
Import notiondb and create a client object:
    from notiondb import Connector
    con = Connector("YOUR_API_KEY")

To add a row to an existing database, use the Row and Schema objects:
    >>> from notiondb import Row, Schema
    >>> schema = con.get_db_schema("YOUR_DATABASE_ID")
    >>> schema
    SchemaObject: {'Name': {'type': 'title'}, 'Age': {'type': 'number'}}
    >>> row = Row(data = {"Name": "John", "Age": 20}, schema)
    >>> con.add_row_to_db("YOUR_DATABASE_ID", row)
    

License
-------
This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.
