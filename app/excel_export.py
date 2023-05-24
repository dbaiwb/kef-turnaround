# excel_export.py
import pandas as pd
import xlsxwriter
import datetime
from typing import List, Dict


def export_to_excel(data: List[Dict[str, str]]) -> None:
    """
    Export data to an Excel file with specified formatting.
    Args:
        data (list of lists): The data to be exported.
    Returns:
        None
    """
    if not isinstance(data, list):
        raise TypeError("Expected 'data' to be a list of dictionaries.")

    try:
        # Define the column order for the Excel sheet
        column_order = ['Priority', 'Flight No.\nFlug', 'A/C', 'Arr.', 'From', 'Dep.', 'To',
                        'Gate', 'Pax off', 'Cargo off', 'Mail off', 'Pax on',
                        'Booked\nCargo/Mail', 'Lead Agents', 'Radio', ' ',
                        'Specified & Comments:']

        # Create a pandas DataFrame from the data
        df = pd.DataFrame(data, columns=column_order)

        # Get the current date and time
        date = datetime.datetime.now().strftime('%d.%m.%y')
        time_now = datetime.datetime.now().strftime('%H:%M')

        # Create an Excel writer and workbook
        writer = pd.ExcelWriter(f'traffic {date}.xlsx', engine='xlsxwriter')
        workbook = writer.book

        # Add a worksheet for the data
        worksheet = workbook.add_worksheet('Traffic')

        # Write the DataFrame to the worksheet
        df.to_excel(writer, sheet_name='Traffic',
                    startrow=2, index=False, header=False)

        # Define formatting objects
        header_format = create_header_format(workbook)
        rows_format = create_rows_format(workbook)
        border_format = create_border_format(workbook)

        # Format the headers
        format_header(worksheet, column_order)

        # Apply conditional formatting to highlight specific rows
        format_rows(worksheet, ['A3:A39', 'C3:C39',
                    'H3:H39', 'L3:L39', 'M3:M39'], rows_format)

        # Apply conditional formatting for borders
        format_border(worksheet, 'A1:R40', border_format)

        # Write additional information
        write_info(worksheet, date, time_now, header_format)

        # Close the Excel writer
        writer.close()

    except Exception as e:
        print(f"An error occurred while exporting to Excel: {str(e)}")


def create_header_format(workbook):
    """
    Create and return the format for the headers.
    Args:
        workbook (xlsxwriter.workbook.Workbook): The workbook object.
    Returns:
        xlsxwriter.format.Format: The format for the headers.
    """
    return workbook.add_format({'bg_color': '#D3D3D3'})


def create_rows_format(workbook):
    """
    Create and return the format for the rows.
    Args:
        workbook (xlsxwriter.workbook.Workbook): The workbook object.
    Returns:
        xlsxwriter.format.Format: The format for the rows.
    """
    return workbook.add_format({'bg_color': '#808080'})


def create_border_format(workbook):
    """
    Create and return the format for the borders.
    Args:
        workbook (xlsxwriter.workbook.Workbook): The workbook object.
    Returns:
        xlsxwriter.format.Format: The format for the borders.
    """
    return workbook.add_format({'border': 1, 'border_color': 'black'})


def format_header(worksheet, column_order):
    """
    Format the headers of the worksheet.
    Args:
        worksheet (xlsxwriter.worksheet.Worksheet): The worksheet object.
        column_order (list): The column order for the headers.
        header_format (xlsxwriter.format.Format): The format for the headers.
    Returns:
        None
    """
    for col_idx, header in enumerate(column_order):
        cell = xlsxwriter.utility.xl_col_to_name(col_idx) + '2'
        worksheet.write(cell, header)
        text_length = len(str(header))
        column_width = max(10, text_length)
        worksheet.set_column(col_idx, col_idx, column_width)


def format_rows(worksheet, row_ranges, rows_format):
    """
    Apply conditional formatting to highlight specific rows.
    Args:
        worksheet (xlsxwriter.worksheet.Worksheet): The worksheet object.
        row_ranges (list): List of row ranges to apply formatting to.
        rows_format (xlsxwriter.format.Format): The format for the rows.
    Returns:
        None
    """
    for row_range in row_ranges:
        worksheet.conditional_format(
            row_range, {'type': 'no_blanks', 'format': rows_format})


def format_border(worksheet, frame_range, border_format):
    """
    Apply conditional formatting for borders.
    Args:
        worksheet (xlsxwriter.worksheet.Worksheet): The worksheet object.
        frame_range (str): The range to apply formatting to.
        border_format (xlsxwriter.format.Format): The format for the borders.
    Returns:
        None
    """
    worksheet.conditional_format(
        frame_range, {'type': 'no_blanks', 'format': border_format})


def write_info(worksheet, date, time_now, header_format):
    """
    Write additional information to the worksheet.
    Args:
        worksheet (xlsxwriter.worksheet.Worksheet): The worksheet object.
        date (str): The current date.
        time_now (str): The current time.
        header_format (xlsxwriter.format.Format): The format for the headers.
    Returns:
        None
    """
    worksheet.merge_range('A1:C1', 'Date:', header_format)
    worksheet.merge_range('D1:G1', date)
    worksheet.merge_range('O1:R1', f'Gate Confirmed: {time_now}')
    worksheet.merge_range('A40:B40', 'Confirmed by:')
    worksheet.merge_range('C40:G40', ' ')
