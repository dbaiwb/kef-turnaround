# data_merge.py
from typing import List, Dict, Any


def data_merge(departures: List[Dict[str, Any]], arrivals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Merge two lists of flight data (departures and arrivals) based on 'Gate' and 'A/C'.
    Args:
        departures (list): A list of dictionaries, where each dictionary contains flight departure data.
        arrivals (list): A list of dictionaries, where each dictionary contains flight arrival data.
    Returns:
        merged_list (list): A list of dictionaries, where each dictionary contains merged flight data.
    """

    # Initialize an empty list for the merged data
    merged_list = []

    # Initialize an empty list for keeping track of merged IDs
    merged_ids = []

    # Initialize a variable for flight priority
    i = 1

    # Loop through all departures
    for departure in departures:
        # Loop through all arrivals
        for arrival in arrivals:
            # If the 'Gate' and 'A/C' values match...
            if (departure['Gate'] == arrival['Gate']) and (departure['A/C'] == arrival['A/C']):
                # Merge the departure and arrival dictionaries
                merged_dict = {**departure, **arrival}
                # Combine the flight numbers
                merged_dict['Flight No.\nFlug'] = arrival['Flight No.\nFlug'] + \
                    '-' + departure['Flight No.\nFlug']
                # Assign the flight a priority
                merged_dict['Priority'] = i
                i += 1

                # Append the merged dictionary to the merged list
                merged_list.append(merged_dict)
                # Remember the Gate number of the merged flight
                merged_ids.append(arrival['Gate'])
                break
        # If no matching arrival was found...
        else:
            # Update the flight number of the departure
            departure['Flight No.\nFlug'] = '-' + departure['Flight No.\nFlug']
            # Add the departure to the merged list
            merged_list.append(departure)

    # Loop through all arrivals one more time
    for arrival in arrivals:
        # If an arrival was not already merged...
        if arrival['Gate'] not in merged_ids:
            # Update the flight number of the arrival
            arrival['Flight No.\nFlug'] = '-' + arrival['Flight No.\nFlug']
            # Add the arrival to the merged list
            merged_list.append(arrival)

    # Return the merged list
    return merged_list
