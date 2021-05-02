"""
Query the DoneDeal API and store the results in a CSV file for later use
"""

import requests
import json
import pandas as pd
import logging
from DoneDeal_Ad import DoneDealAd

# API URL
DONEDEAL_API_URL = "https://www.donedeal.ie/search/api/v4/find/"


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Configurable API inputs
json_input = {
    "adType": "forsale",
    "area": ["Leinster"],
    "max": 30,
    "mileageType": "Kilometres",
    "priceType": "Euro",
    "section": "cars",
    "sort": "relevance desc",
    "start": 0,
    "source": "simi",
    "viewType": "list",
    "words": ""
}

resp_len = 30
buffer_list = []
df = None

# if respone length drops below 30 we must be on the last page
while resp_len == 30:
    resp_dict = requests.post(url=DONEDEAL_API_URL, json=json_input, headers=headers).json()
    resp_json = json.dumps(resp_dict, indent=4)

    # test_file = "/Users/jcurtis/DoneDeal_Scrapper/test.json"
    # Log json response to a file
    # f = open(test_file, 'w')
    # f.write(resp_json)

    ads_list = resp_dict.get('ads', None)

    # If there are no more ads, break the loop
    # Log the response so we can take a look at it
    if ads_list is None:
        test_file = "/Users/jcurtis/DoneDeal_Scrapper/test.json"
        # Log json response to a file
        f = open(test_file, 'w')
        f.write(resp_json)
        break

    logging.debug(f"Response: {ads_list}")
    print(f"Length of response: {len(ads_list)}")

    for ad in ads_list:
        # Parse ad dict and set attrs
        ParsedAd = DoneDealAd(ad)
        # attrs_dict = [{attr: ParsedAd.__dict__ .get(attr)} for attr in ParsedAd.__dict__ if attr not in ["raw_ad"]]
        attrs_dict = ParsedAd.__dict__
        # Dict of all attrs except for the raw ad json which we don't need
        attrs_dict.pop("raw_ad")
        buffer_list.append(attrs_dict)

    # Add values to a python dataframe
    if df is None:
        df = pd.DataFrame(buffer_list)
    else:
        df1 = pd.DataFrame(buffer_list)
        df = pd.concat([df, df1])
    resp_len = len(resp_dict['ads'])

    # bump starting point forward a page worths of ads
    json_input['start'] += 29


print(df.head())
print(len(df))
df.to_csv("/Users/jcurtis/DoneDeal_Scrapper/output.csv")
