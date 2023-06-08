# main.py
import argparse
import datetime
from excel_export import export_to_excel
from data_fetch import *
from data_processing import *
from data_merge import data_merge


def main(hours_threshold_before, hours_threshold_after):
    """
    Main function to fetch, process and export flight data.
    """
    # Fetch data from the specified URLs
    try:
        arrivals_response = fetch_data(
            "https://www.isavia.is/fids/arrivals.aspx?_=1684513438221")
        departures_response = fetch_data(
            'https://www.isavia.is/fids/departures.aspx?_=1684682369206')
    except Exception as e:
        print(f"Error occurred while fetching data: {str(e)}")
        return

    # Parse fetched data
    try:
        arrivals = parse_data(arrivals_response)
        departures = parse_data(departures_response)
    except Exception as e:
        print(f"Error occurred while parsing data: {str(e)}")
        return

    # Filter data
    try:
        arrivals = filter_data(arrivals)
        departures = filter_data(departures)
    except Exception as e:
        print(f"Error occurred while filtering data: {str(e)}")
        return

    # Determine cutoff times based on thresholds
    cutoff_time_before = datetime.datetime.now(
        datetime.timezone.utc) - datetime.timedelta(hours=hours_threshold_before)
    cutoff_time_after = datetime.datetime.now(
        datetime.timezone.utc) + datetime.timedelta(hours=hours_threshold_after)
    # Filter data by timestamp
    try:
        arrivals = filter_data_by_timestamp(
            arrivals, cutoff_time_before, cutoff_time_after)
        departures = filter_data_by_timestamp(
            departures, cutoff_time_before, cutoff_time_after)
    except Exception as e:
        print(f"Error occurred while filtering data by timestamp: {str(e)}")
        return

    # Format time in data
    try:
        format_time(arrivals)
        format_time(departures)
    except Exception as e:
        print(f"Error occurred while formatting time: {str(e)}")
        return

    # Format data
    try:
        format_data(arrivals, 0)
        format_data(departures, 1)
    except Exception as e:
        print(f"Error occurred while formatting data: {str(e)}")
        return

    # Merge departures and arrivals data
    try:
        merged_list = data_merge(departures, arrivals)
    except Exception as e:
        print(f"Error occurred while merging data: {str(e)}")
        return

    # Export data to Excel
    try:
        export_to_excel(merged_list)
        print("Data exported successfully.")
    except Exception as e:
        print(f"Error occurred while exporting data: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--bf', type=int, required=True,
                        help='Specify time in hours before now')
    parser.add_argument('--af', type=int, required=True,
                        help='Specify time in hours after now')

    args = parser.parse_args()

    main(args.bf, args.af)
