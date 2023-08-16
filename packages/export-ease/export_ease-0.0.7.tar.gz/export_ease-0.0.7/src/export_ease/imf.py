import os
import datetime
import json
import pandas
import requests
import datetime
from flatten_json import flatten

class IMF:
   
    root = "http://dataservices.imf.org/REST/SDMX_JSON.svc/"
    cwd = os.getcwd()
    parent = os.path.dirname(cwd)
    directory = os.path.join(parent, "data")
    json_path = os.path.join(directory, "my.json")

    # dictionary to store country names as keys and corresponding country codes as values
    country_dict = {} 

    def __init__(self):
        pass

    # function to write countries and their corresponding codes to a csv file
    @classmethod
    def get_countries(cls):
        df = pandas.DataFrame.from_dict(IMF.country_dict, orient = "index")
        file_path = os.path.join(IMF.directory, "imf_country_codes.csv")
        df.to_csv(file_path)

    # function to add key-value pairs to country_dict, where keys = country names & values = country codes
    @classmethod
    def make_country_dict(cls):
        country_key = 'DataStructure/DOT'
        dimensions = requests.get(f'{IMF.root}{country_key}').json()\
            ['Structure']['KeyFamilies']['KeyFamily']['Components']['Dimension']
        country_key = f"CodeList/{dimensions[1]['@codelist']}"
        country_list = requests.get(f'{IMF.root}{country_key}').json()['Structure']['CodeLists']['CodeList']['Code']
        for country in country_list:
            key = country['Description']['#text']
            value = country['@value']
            IMF.country_dict[key] = value
        if not os.path.exists(os.path.join(IMF.directory, "imf_country_codes.csv")):
            IMF.get_countries()

    # function to clean up data and write to a csv file
    @classmethod
    def flatten_and_write(cls, data, csv_path):
        json_obj = json.dumps(data, indent = 1)
        with open(IMF.json_path, "w") as output_file:
            output_file.write(json_obj)
        with open(IMF.json_path, "r") as input_file:
            data = json.load(input_file)
        df = pandas.DataFrame([flatten(country) for country in data])
        df.to_csv(csv_path)
        os.remove(IMF.json_path)

    # function to write export data to a csv file for a country to all its partners, starting at year designated by start
    @classmethod
    def get_reporter_exports(cls, rep, freq, start):
        IMF.make_country_dict()
        if (freq == "B"):
            IMF.get_reporter_exports(rep, "A", start)
            IMF.get_reporter_exports(rep, "M", start)
        else:
            reporter = IMF.country_dict[rep]
            csv_name = f'imf_{reporter}_all_exports_{start}{freq}.csv'
            year = int(datetime.date.today().year) - 3
            if int(start) > year and freq == "A":
                start = str(year)
            csv_path = os.path.join(IMF.directory, csv_name)
            key = f'CompactData/DOT/{freq}.{reporter}.TXG_FOB_USD..?startPeriod={start}'
            data = requests.get(f'{IMF.root}{key}').json()['CompactData']['DataSet']['Series']
            print(f'Writing {csv_name}....')
            IMF.flatten_and_write(data, csv_path)

    # function to get each country's total exports for a given year (returns data for specified year only)
    @classmethod
    def get_total_exports(cls, freq, year):
        if freq == "B":
            IMF.get_total_exports("A", year)
            IMF.get_total_exports("M", year)
        else:
            csv_name = f'imf_total_exports_{year}{freq}.csv'
            csv_path = os.path.join(IMF.directory, csv_name)
            key = f'CompactData/DOT/{freq}..TXG_FOB_USD.W00.?startPeriod={year}'
            data = requests.get(f'{IMF.root}{key}').json()['CompactData']['DataSet']['Series']
            print(f'Writing {csv_name}....')
            IMF.flatten_and_write(data, csv_path)
