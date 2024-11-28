# test_word = "Hi, I'm a test sentence."

import requests
import csv

# def get_google_sheet_as_list(sheet_url):
#     """
#     Fetches the content of a public Google Sheet and returns the first column as a string list.
#
#     :param sheet_url: The public URL of the Google Sheet
#     :return: A list of strings from the first column
#     """
#     # Convert Google Sheet URL to its CSV export format
#     if "/edit" in sheet_url:
#         csv_url = sheet_url.replace("/edit", "/export?format=csv")
#     else:
#         raise ValueError("Invalid Google Sheet URL format.")

def get_google_sheet_as_dict(sheet_url):
    """
    Fetches the content of a public Google Sheet and returns a dictionary where
    the first column is the key (word) and the second column is the value (image URL).

    :param sheet_url: The public URL of the Google Sheet
    :return: A dictionary mapping words to their associated image URLs
    """
    # Convert Google Sheet URL to its CSV export format
    if "/edit" in sheet_url:
        csv_url = sheet_url.replace("/edit", "/export?format=csv")
    else:
        raise ValueError("Invalid Google Sheet URL format.")

    # Fetch the CSV data from the public URL
    response = requests.get(csv_url)
    response.raise_for_status()  # Raise an error for invalid responses

    # Parse the CSV data
    # data = []
    # csv_reader = csv.reader(response.text.splitlines())
    # for row in csv_reader:
    #     if row:  # Skip empty rows
    #         data.append(row[0])  # Append the first column of each row
    #
    # return data

    # Parse the CSV data
    data = {}
    csv_reader = csv.reader(response.text.splitlines())
    for row in csv_reader:
        if len(row) >= 2:  # Ensure there are at least two columns
            data[row[0]] = row[1]  # Use the first column as key and second as value

    return data    # Parse the CSV data


# Example usage
# sheet_url = "https://docs.google.com/spreadsheets/d/1fGC_FzOsUHDt9NsO1LKsIMmcpLq6hZEtohgnBl2kZto/edit"  # Replace with your public Google Sheet URL
# try:
#     word_list = get_google_sheet_as_list(sheet_url)
#     print(word_list)  # Prints the list of strings from the first column
# except Exception as e:
#     print(f"An error occurred: {e}")
#
#

# Example usage
sheet_url = "https://docs.google.com/spreadsheets/d/1fGC_FzOsUHDt9NsO1LKsIMmcpLq6hZEtohgnBl2kZto/edit"  # Replace with your public Google Sheet URL
try:
    word_image_dict = get_google_sheet_as_dict(sheet_url)
    print(word_image_dict)  # Prints the dictionary of words and image URLs
except Exception as e:
    print(f"An error occurred: {e}")
