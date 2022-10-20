from typing import List, Dict, Tuple, Optional, Any, TypeVar, TYPE_CHECKING
import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse

from .Schema import Schema


class Connector:
    """
    Notion API Client

    This allows interacting with the Notion API. You can use this to create databases, add rows to databases, and query databases.
    For any other API calls that are not implemented, you can use the `request` method.

    For more, see reference at: https://developers.notion.com/reference/intro

    All the methods in this class allow you to pass in additional arguments to the request body. These arguments will override the arguments that are passed in as parameters to the method if they use the same keys.

    Args:
        api_key (str): The API key
        **kwargs: Additional arguments to pass to the requests session


    Example:
        >>> import notion
        >>> client = notion.Connector("API_KEY")
        >>> client.query_db("DATABASE_ID")


    """

    def __init__(self, api_key, **kwargs) -> None:
        """Initializes the connector"""
        self.__API_KEY = api_key
        self.__session = requests.Session(**kwargs)
        self.__session.headers.update({"Authorization": f"Bearer {self.__API_KEY}"})
        self.__session.headers.update({"Notion-Version": "2022-02-22"})
        self.__session.headers.update({"Content-Type": "application/json"})

        # Retry 3 times
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
        self.__session.mount("https://", HTTPAdapter(max_retries=retries))

    # Database
    # ---------------------
    # POST databases/{database_id}/query

    def query_db(
        self,
        db_id: str,
        filter: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        **kwargs,
    ) -> Dict:
        """
        Query a database as per the notion API specifcation.
        Note: Corresponds to the POST /databases/{database_id}/query endpoint.

        Args:
            db_id (str): The database id
            filter (Optional[Dict]): The filter to apply to the query (see notion API docs)
            sorts (Optional[List[Dict]]): The sorts to apply to the query (see notion API docs)
            **kwargs: Additional arguments to pass to the POST request body (These may override the filter and sorts arguments if they use the same keys)

        Returns:
            Dict: The response from the API

        """

        data = {}
        if filter:
            data["filter"] = filter
        if sorts:
            data["sorts"] = sorts

        data.update(kwargs)

        response = self.__session.post(
            f"https://api.notion.com/v1/databases/{db_id}/query", json=data
        )

        return response.json()

    # POST /databases/{database_id}/
    def create_db(
        self, schema: "Schema", parent: str, title: str, cover_url: str = None, **kwargs
    ) -> Dict:
        """
        Creates a database as per the notion API specification.
        Uses a schema object to create the columns and properties of the database.
        To add rows to the database use the `add_row_to_db` method after creating the database.

        Note: Corresponds to the POST /databases/{database_id}/ endpoint.

        Args:
            schema (Schema): The schema of the database
            parent (str): The parent ID of the database
            title (str): The title of the database
            cover_url (Optional[str]): The cover url of the database
            **kwargs: Additional arguments to pass to the POST request body (These may override the schema, parent, title, and cover_url arguments if using the same keys)

        Returns:
            Dict: The response from the API
        """

        json = schema._to_notion()
        json["parent"] = {"page_id": parent}
        json["title"] = [{"text": {"content": title}}]
        if cover_url:
            json["cover"] = {"type": "external", "external": {"url": cover_url}}
        json.update(kwargs)
        response = self.__session.post("https://api.notion.com/v1/databases", json=json)

        return response.json()

    # PATCH /databases/{database_id}
    def update_db(self, db_id: str, schema: "Schema", title=None) -> Dict:
        """
        Updates a database schema as per the notion API specification.
        Uses a schema object to update the columns and properties of the database.

        Note: Corresponds to the PATCH /databases/{database_id} endpoint.

        Args:
            db_id (str): database ID
            schema (Schema): schema object to update
            title (str, optional): title to change. Defaults to None.
            **kwargs: Additional arguments to pass to the PATCH request body (These may override the schema, parent, title, and cover_url arguments if using the same keys)

        Returns:
            Dict: response from the API

        Example:
            >>> import notion
            >>> client = notion.Connector("API_KEY")
            >>> schema = notion.Schema(TITLE = notion.Title("Name"), AGE = notion.Number("Age"))
            >>> client.update_db("DATABASE_ID", schema)

        """
        if title:
            raise NotImplementedError("Title update not implemented")
        response = self.__session.patch(
            f"https://api.notion.com/v1/databases/{db_id}", json=schema._to_notion()
        )
        return response.json()

    # GET/databases
    def get_db_schema(self, db_id: str, json=False) -> "Schema":
        """Gets the schema of a database

        Note: Corresponds to the GET /databases/{database_id} endpoint.

        Args:
            db_id (str): Database ID
            json (bool, optional): Set to True to return the raw json instead of Schema obj. Defaults to False.

        Returns:
            Schema: The schema object of the database (or json if json is True)

        """
        response = self.__session.get(f"https://api.notion.com/v1/databases/{db_id}")
        if json:
            return response.json()
        return Schema.from_database(response.json())

    # Pages
    # ---------------------
    # POST /pages

    def add_row_to_db(self, db_id: str, row, **kwargs) -> Dict:
        """Adds a DatabaseRow object to a database

        Note: Corresponds to the POST /pages endpoint.

        Args:
            db_id (str): Database ID
            row (DatabaseRow|Dict|str): DatabaseRow object or JSON object based on API specification
            **kwargs: Additional arguments to pass to the POST

        Returns:
            Dict: response from the API
        """
        json = row.notion
        json["parent"] = {"database_id": db_id}
        json.update(kwargs)
        response = self.__session.post("https://api.notion.com/v1/pages", json=json)
        return response.json()

    def request(self, method, url, **kwargs):
        """Makes a custom request to the notion API

        Uses underlying requests.Session object to make a request to the notion API.
        See the requests documentation for more information.

        Args:
            method (str): type of request, eg. GET, POST, PATCH, etc.
            url (str): url to make the request to (must be a notion API url or extension)

        Returns:
            Dict: response
        """
        if not url.startswith("https://api.notion.com"):
            if url.startswith("/"):
                url = "https://api.notion.com" + url
            else:
                raise ValueError(
                    "url must be a notion API url that starts with https://api.notion.com or / . eg. '/databases/get'"
                )

        return self.__request(method, url, **kwargs)

    def __request(self, method, url, **kwargs):
        """Only for internal use. All requests will be routed through here. This is a final step and secuirty check before making a request."""
        if not url.startswith("https://api.notion.com"):
            raise ValueError(
                "Session received a request that was not a notion API request to " + url
            )
        return self.__session.request(method, url, **kwargs)
