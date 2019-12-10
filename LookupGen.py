#!/usr/bin/python

import getopt
import json
import random
import sys

import pandas as pd


def main(argv):

    input_file_name = 'fixtures/outputs/sample_out_all'
    region_file_name = 'fixtures/region_lookup.csv'
    county_file_name = 'fixtures/county_lookup.json'

    try:
        opts, args = getopt.getopt(argv, "hi:r:c", ["input_file=",
                                                    "region_file=",
                                                    "county_file=",
                                                    ])
    except getopt.GetoptError:
        print('DataGen.py -i <input_file> -r <region_file> -c <county_file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('DataGen.py -s <survey_file> -r <region_file> -e <enterprise_file> ' +
                  '-o <output_file> -i <starting_id> -p <period_split>')
            sys.exit()
        elif opt in ("-i", "--input_file"):
            input_file_name = arg
        elif opt in ("-r", "--region_file"):
            region_file_name = arg
        elif opt in ("-c", "--county_file"):
            county_file_name = arg

    input_df = pd.read_csv(input_file_name + '.csv')
    region_df = pd.read_csv(region_file_name)

    with open(county_file_name, "r") as county_file:
        county_json = json.load(county_file)
    county_df = pd.DataFrame(county_json)

    id_column = input_df[['responder_id', 'gor_code', 'land_or_marine']].drop_duplicates()
    prepared_df = pd.merge(id_column, region_df[['region', 'gor_code']],
                           on='gor_code', how="left")

    prepared_df['county'] = prepared_df.apply(lambda x: get_county(x, county_df), axis=1)

    final_df = prepared_df[['responder_id', 'county']]
    final_df.to_csv(input_file_name + "_lookup.csv", header=True, index=False)
    final_df.to_json(input_file_name + "_lookup.json", orient="records")
    print('----------')
    print(' Complete')
    print('----------')


def get_county(row, county_df):

    if row['land_or_marine'] == 'L':
        toggle = 'n'
    elif row['land_or_marine'] == 'M':
        toggle = 'y'

    county_list = county_df['county'][(county_df['region'] == row['region']) & (county_df['marine'] == toggle)].tolist()

    return random.choice(county_list)


if __name__ == "__main__":
    main(sys.argv[1:])
