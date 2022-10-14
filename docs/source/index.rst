Notion-Client
=============
NotionClient is a powerful object-oriented client for the Notion API. 
Learn how to use it and create your own Notion integrations in minutes!


.. toctree::
   :maxdepth: 5

   modules
   getting_started



Installation
------------
Install the package using pip:
```
pip install notion-client
```

Usage
-----
First, import the client:
```
from notion_client import Client
```

Then, create a client instance:
```
client = Client(auth="secret_...")
```

You can now use the client to interact with the Notion API. For example, to get a page:
```
page = client.get_database("https://www.notion.so/Notion-Python-SDK-Example-Page-1e0e1e1e1e1e4e5e8e9e9e9e9e9e9e9e")
```
