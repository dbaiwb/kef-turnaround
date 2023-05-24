# data_fetch.py
import requests
from typing import Optional, Dict, Any, Union
from requests.models import Response


def fetch_data(url: str, headers: Optional[Dict[str, str]] = None) -> Union[Response, None]:
    """
    Fetches data from the given URL.
    Args:
        url (str): The URL to fetch the data from.
        headers (dict, optional): Headers to include in the request. Defaults to None.
    Returns:
        requests.Response: The response object containing the fetched data or None in case of failure.
    """
    if not isinstance(url, str):
        raise TypeError("Expected 'url' to be a string.")

    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-successful status codes
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {str(e)}")
        return None


def parse_data(response: Response) -> Union[Dict[str, Any], None]:
    """
    Parses the response and returns the JSON data.
    Args:
        response (requests.Response): The response object to parse.
    Returns:
        dict: The parsed JSON data or None in case of failure.
    """
    if not isinstance(response, Response):
        raise TypeError(
            "Expected 'response' to be a 'requests.Response' object.")

    try:
        return response.json()
    except ValueError as e:
        print(f"An error occurred while parsing data: {str(e)}")
        return None
