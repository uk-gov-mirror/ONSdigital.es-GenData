#!/usr/bin/python

import getopt
import json
import random
import sys

import pandas as pd


def main(argv):

    survey_config_file_path = 'resources/sampleSurvey.json'
    region_list_file_path = 'resources/regionList.csv'
    enterprise_list_file_path = 'resources/enterpriseList.csv'
    output_file_path = 'resources/out.csv'
    sub_ref = 10000000000

    try:
        opts, args = getopt.getopt(argv, "hs:r:e:o:id:", ["survey_file=", "region_file=",
                                                          "enterprise_file=",
                                                          "output_file=", "starting_id="])
    except getopt.GetoptError:
        print('DataGen.py -s <survey_file> -r <region_file> -e <enterprise_file> ' +
              '-o <output_file> -id <starting_id>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('DataGen.py -s <survey_file> -r <region_file> -e <enterprise_file> ' +
                  '-o <output_file> -id <starting_id>')
            sys.exit()
        elif opt in ("-s", "--survey_file"):
            survey_config_file_path = arg
        elif opt in ("-r", "--region_file"):
            region_list_file_path = arg
        elif opt in ("-e", "--enterprise_file"):
            enterprise_list_file_path = arg
        elif opt in ("-o", "--output_file"):
            output_file_path = arg
        elif opt in ("-id", "--starting_id"):
            sub_ref = arg

    with open(survey_config_file_path, "r") as survey_config_file:
        survey_config = json.load(survey_config_file)

    regions = pd.read_csv(region_list_file_path)
    enterprises = pd.read_csv(enterprise_list_file_path, )

    output_df = pd.DataFrame(columns=survey_config['data_frame_columns'])
    column_order = output_df.columns

    # generate the required enterprises
    for ent_idx in range(0, min(survey_config['number_of_enterprises'],
                                len(enterprises.index))):
        # pick enterprise name and id from list file
        ent_name = enterprises.iloc[ent_idx, 0]
        ent_ref = enterprises.iloc[ent_idx, 1]

        # decide on a number of subsidiaries the enterprise has
        number_of_subsidiaries = random.randrange(1, 5)

        # for each subsidiary
        for sub_idx in range(0, number_of_subsidiaries):
            # generate a ruref
            sub_ref += 1

            # pick a region from list file
            sub_region = regions.iloc[random.randrange(0, len(regions.index)), 0]

            # for each period
            for period in survey_config['periods']:
                # add new row to the output
                response_df = pd.DataFrame({
                    "period": period,
                    "ruref": sub_ref,
                    "ent_ref": ent_ref,
                    "ent_name": ent_name,
                    "region": sub_region
                }, index=[0])

                # decide if non-respondent
                if random.random() > survey_config['response_rate']:
                    response_df['response_type'] = 1

                    for value in survey_config['values']:
                        response_df[value['col_name']] = value['default']

                    # calculate all sum columns
                    for sum_col in survey_config['sum_columns']:
                        response_df[sum_col['col_name']] = 0
                else:
                    response_df['response_type'] = 2
                    response_sum = 0

                    # for each value in config
                    for value in survey_config['values']:
                        # if value should be 0
                        new_value = value['default']

                        # should value be a valid response
                        if random.random() <= value['prob_of_data']:
                            # generate a rand value from range in config
                            if 'max' in value:
                                new_value = random.randrange(value['min'], value['max'])
                            # generate a rang value from a range and
                            # the sum of specified columns
                            elif 'max_from' in value:
                                max_value = 0
                                for agg_col in value['max_from']:
                                    max_value += response_df.iloc[0][agg_col]

                                if max_value > value['min']:
                                    new_value = random.randrange(value['min'], max_value)

                        # assign response value
                        response_df[value['col_name']] = new_value

                        # add to sum column
                        response_sum += new_value

                    # calculate all sum columns
                    for sum_col in survey_config['sum_columns']:
                        new_sum = 0
                        for data_col in sum_col['data']:
                            if sum_col['data'][data_col] == "+":
                                new_sum += response_df.iloc[0][data_col]
                            elif sum_col['data'][data_col] == "-":
                                new_sum -= response_df.iloc[0][data_col]
                        response_df[sum_col['col_name']] = new_sum

                # add this response to output data frame
                output_df = output_df.append(response_df, ignore_index=True)

    # save to csv
    output_df = output_df.ix[:, column_order]
    output_df.to_csv(output_file_path, header=False, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
