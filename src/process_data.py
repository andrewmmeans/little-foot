from bs4 import BeautifulSoup
import pandas as pd
from numpy import vectorize


def build_header(str_lst):
    """
    Parameters
    ----------
    str_list: list(str)
        A list of strings

    Returns
    -------
    result : dict
        A dictionary with key, value pairs from processing the header
    """
    result = {}

    # array for geographical information 
    # Example : (Geographical Index > United States > Alaska > Anchorage County > Report # 13038)
    # geographic = [Geographical Index, United States, Alaska, Anchorage County, Report # 13038]
    geographic = [x.strip() for x in str_lst[0].split('>')]
    geo_dict = {
        'region': None,
        'state': None,
        'detail': None,
        'report': None,
        'report_class': None
    }
    if len(geographic) > 4:
        geo_dict['region'] = geographic[1]
        geo_dict['state'] = geographic[2]
        geo_dict['detail'] = geographic[3]
        report = geographic[4]
        geo_dict['report'] = report.split(' ')[-1]
        geo_dict['report_class'] = str_lst[2]
    return geo_dict


def build_details(str_lst):
    """
    Parameters
    ----------
    str_list: list(str)
        A list of strings

    Returns
    -------
    result : dict
        A dictionary with key, value pairs from processing the details section
    """
    # empty list to store return key value pairs
    result = {}
    
    valid_columns = ['YEAR', 'SEASON', 'MONTH', 'STATE', 'COUNTY', 'LOCATION DETAILS',
       'NEAREST TOWN', 'NEAREST ROAD', 'OBSERVED', 'ALSO NOTICED',
       'OTHER WITNESSES', 'OTHER STORIES', 'TIME AND CONDITIONS',
       'ENVIRONMENT', 'DATE', 'extra']
    
    # flag to alter the way we build keys
    process_diff = False
    
    # empty array to store extra information if process_diff flag is True
    extra = []
    for i, x in enumerate(str_lst):
        # splits each line into a key, value string pair
        first, *second = x.split(':')
        
        if not first.isupper() and first not in valid_columns:    
            # checks if key isn't CAPS, if not we process the rest of the html differently
            process_diff = True
            
        if not process_diff:
            # we join the second part in case there exists a colon ":" inside the raw text
            result[first] = (' '.join(second)).strip()
            
        else:
            # append each extra line to a general array
            extra.append(x)
    
    # combine all extra values into a single long string
    result['extra'] = ' '.join(extra)
    remove_keys = []
    # find all keys that don't match schema
    for key in result.keys():
        if key not in valid_columns:
            remove_keys.append(key)
    # remove keys from result
    for key in remove_keys:
        result.pop(key)
    return result


def process_one(row):
    soup = BeautifulSoup(row, features='html.parser')
    details = build_details([x.text for x in soup.find_all('p')])
    header = build_header([x.text for x in soup.find_all('span')[0:5]])
    joined = {}
    try:
        joined.update(details)
        joined.update(header)
    except ValueError as e:
        pass
    return joined

if __name__ == '__main__':
    dataset = 'data/bigfoot_data.json'

    # load the raw data
    with open(dataset) as f:
        raw_df = pd.read_json(f, lines=True)

    processed = []

    for i, row in enumerate(raw_df.html):
        try:
            processed.append(process_one(row))
        except Exception as e:
            print(f'row: {i}', e)
    df = pd.DataFrame(processed)
    df.to_pickle('data/processed_df.pkl')

