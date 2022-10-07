from typing import List, Dict, Tuple, Optional, Any, TypeVar, TYPE_CHECKING
import requests

if TYPE_CHECKING:
    from .Schema import Schema

class Connector:
    """
        Notion API Client
        See reference at: https://developers.notion.com/reference/intro

        For use with Object Oriented Notion API Wrapper

        Example:
        import notion
        client = notion.Connector("API_KEY")
        client.query_db("DATABASE_ID")

    """
    def __init__(self, api_key) -> None:
        """
            Initializes Notion API Client. 
            :param api_key: The API key
        """
        self.API_KEY = api_key
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.API_KEY}"})
        self.session.headers.update({"Notion-Version": "2022-02-22"})
        self.session.headers.update({"Content-Type": "application/json"})
        
    # Database
    # ---------------------
    # POST databases/{database_id}/query

    def query_db(self, db_id: str, filter: Optional[Dict] = None, sorts: Optional[List[Dict]] = None) -> Dict:
        """
            Query a database.
            :param db_id: The database id
            :param filter: A filter object
            :param sorts: A list of sort objects
        """
    
        data = {}
        if filter:
            data["filter"] = filter
        if sorts:
            data["sorts"] = sorts
        response = self.session.post(f"https://api.notion.com/v1/databases/{db_id}/query", json = data)
        return response.json()
    
    # POST /databases/{database_id}/
    def create_db(self, schema: "Schema", parent: str, title:str, cover_url:str = None) -> Dict:
        """
            Create a new database.
            :param schema: The schema of the database
            :param parent: The parent page id
            :param title: The title of the database
            :param cover_url: Optional, The cover image url
        
        """
        json = schema.to_notion()
        json["parent"] = {"page_id": parent}
        json["title"] = [{"text": {"content": title}}]
        if cover_url:
            json["cover"] = {"type": "external", "external": {"url": cover_url}}
        
        response = self.session.post("https://api.notion.com/v1/databases", json = json)

        return response.json()

    # PATCH /databases/{database_id}
    def update_db(self, db_id: str, schema: "Schema", title = None) -> Dict:
        """
            Update the schema of a database.
            :param db_id: The database id
            :param schema: The new schema
        """
        if title: raise NotImplementedError("Title update not implemented")
        response = self.session.patch(f"https://api.notion.com/v1/databases/{db_id}", json = schema.to_notion())
        return response.json()
    

    # GET/databases
    def get_db_schema(self, db_id: str) -> Dict:
        """
            Get the schema of a database.
            :param db_id: The database id
        """
        response = self.session.get(f"https://api.notion.com/v1/databases/{db_id}")
        return response.json()
    

    # Pages
    # ---------------------
    # POST /pages

    def add_row_to_db(self, db_id: str, row) -> Dict:
        """
            Add a row to a database.
            :param db_id: The database id
            :param row: The row to add
        """
        json = row.to_notion()
        json["parent"] = {"database_id": db_id}
        response = self.session.post("https://api.notion.com/v1/pages", json = json)
        return response.json()

