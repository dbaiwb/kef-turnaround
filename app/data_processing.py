# data_processing.py
from typing import Dict, List, Optional, Union
import datetime

# Setting global variables
target_key: str = 'AirlineIATA'
target_values: List[str] = ['FI', 'SK', 'AY']
keys_to_keep: List[str] = ['No', 'OriginDestIATA',
                           'Scheduled', 'Stand', 'Aircraft']


def filter_data(data: Dict[str, Union[Dict[str, str], List[Dict[str, str]]]],
                key: Optional[str] = None,
                values: Optional[List[str]] = None) -> List[Dict[str, str]]:
    """
    Filters the input data according to provided key and values. 
    If key and values are not provided, uses the global target_key and target_values.
    Args:
        data: dict -- The data to be filtered.
        key: str -- The key to filter by. Defaults to None.
        values: list -- The values to filter by. Defaults to None.
    Returns:
    list -- The filtered data.
    """

    # Assigning default values
    key = key or target_key
    values = values or target_values

    # Error handling for data type
    if not isinstance(data, dict):
        raise TypeError("Expected 'data' to be a dictionary.")
    if not isinstance(key, str):
        raise TypeError("Expected 'key' to be a string.")
    if not isinstance(values, list):
        raise TypeError("Expected 'values' to be a list.")

    data = list(data.values())[:1]

    data = [
        item for sublist in data for item in sublist if isinstance(item, dict)]

    data = [item for item in data if item.get(key) in values]

    # Keeping only required keys in data
    data = [{k: d[k] for k in keys_to_keep if k in d} for d in data]

    return sorted(data, key=lambda x: x['Scheduled'])


def format_time(data: List[Dict[str, str]]) -> None:
    """
    Formats the 'Scheduled' time of data items into '%H:%M' format.
    Args:
    data: list -- The data to format the time.
    Returns:
    None
    """
    # Error handling for data type
    if not isinstance(data, list):
        raise TypeError("Expected 'data' to be a list.")

    for item in data:
        original_time = item.get('Scheduled', '')

        try:
            datetime_obj = datetime.datetime.fromisoformat(original_time)
        except ValueError:
            raise ValueError(
                f"Invalid date format in 'Scheduled': {original_time}")

        formatted_time = datetime_obj.strftime('%H:%M')
        item['Scheduled'] = formatted_time


def filter_data_by_timestamp(data: List[Dict[str, str]],
                             start_timestamp: datetime.datetime,
                             end_timestamp: datetime.datetime) -> List[Dict[str, str]]:
    """
    Filters the data by a range of timestamps.
    Args:
    data: list -- The data to be filtered.
    start_timestamp: datetime -- The starting timestamp.
    end_timestamp: datetime -- The ending timestamp.
    Returns:
    list -- The filtered data.
    """
    # Error handling for data type
    if not isinstance(data, list):
        raise TypeError("Expected 'data' to be a list.")
    if not isinstance(start_timestamp, datetime.datetime) or not isinstance(end_timestamp, datetime.datetime):
        raise TypeError(
            "Expected 'start_timestamp' and 'end_timestamp' to be datetime objects.")

    return [item for item in data if start_timestamp <= datetime.datetime.fromisoformat(item['Scheduled']) <= end_timestamp]


def format_data(data: List[Dict[str, str]],
                departure: Optional[int] = 0) -> None:
    """
    Formats the keys in the data items.
    Args:
    data: list -- The data to be formatted.
    departure: int -- If 0, item 'From' key is set. Else, item 'To' key is set. Defaults to 0.
    Returns:
    None
    """
    # Error handling for data type
    if not isinstance(data, list):
        raise TypeError("Expected 'data' to be a list.")
    if not isinstance(departure, int):
        raise TypeError("Expected 'departure' to be an integer.")

    for item in data:
        arr_dep = 'Arr.' if departure == 0 else 'Dep.'
        item[arr_dep] = item.pop('Scheduled', None)
        from_to = 'From' if departure == 0 else 'To'
        item[from_to] = item.pop('OriginDestIATA', None)
        item['Flight No.\nFlug'] = item.get('No', '')[-3:]
        item['Aircraft'] = item.get('Aircraft', '')[-3:]
        item['A/C'] = item.pop('Aircraft', None)
        item['Gate'] = item.pop('Stand', None)
        item['Booked Cargo/Mail'] = item.pop('Booked\nCargo/Mail', None)
