import csv
from enum import Enum
from io import StringIO

import requests


class BaseEnum(Enum):
    pass

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


def get_exchange_mic_to_suffix_dict():
    """
    Return a dictionary of MIC codes mapped to exchange codes as ticker suffixes.
    """
    # URL of the read-only Excel sheet
    url = 'https://docs.google.com/spreadsheets/d/1I3pBxjfXB056-g_JYf_6o3Rns3BV2kMGG1nCatb91ls/export?format=csv'
    
    try:
        response = requests.get(url)
        response.raise_for_status()    
        
        # Ensure we received a response in the expected format
        if not response.text.strip():
            return {}
    except requests.RequestException:
        return {}  # Return an empty dictionary in case of an error
        
    csv_reader = csv.reader(StringIO(response.text))
    header = next(csv_reader)
    code_index = header.index('code')
    mic_index = header.index('mic')
    
    # Use dictionary comprehension for concise code
    result_dict = {
        mic.strip(): row[code_index]
        for row in csv_reader
        for mic in row[mic_index].split(',')
    }
    
    return result_dict