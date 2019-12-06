#!/usr/bin/python

import getopt
import json
import random
import sys

import pandas as pd


def main(argv):

    survey_config_file_path = 'fixtures/SynthData/SandAndGravelLand.json'
    region_list_file_path = 'fixtures/region_list.csv'
    enterprise_list_file_path = 'fixtures/enterprise_list.csv'
    previous_file_path = 'fixtures/previous_out.json'
    current_file_path = 'fixtures/current_out.json'
    output_file_path = 'fixtures/out.csv'
    ruref = 10000000000
    split = True

    try:
        opts, args = getopt.getopt(argv, "hs:r:e:o:i:p:", ["survey_file=", "region_file=",
                                                           "enterprise_file=",
                                                           "output_file=",
                                                           "starting_id=",
                                                           "period_split=",
                                                           "current_file_path=",
                                                           "previous_file_path="
                                                           ])
    except getopt.GetoptError:
        print('DataGen.py -s <survey_file> -r <region_file> -e <enterprise_file> ' +
              '-o <output_file> -i <starting_id> -p <period_split> ' +
              '-pr <previous_file_path> -cr <current_file_path>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('DataGen.py -s <survey_file> -r <region_file> -e <enterprise_file> ' +
                  '-o <output_file> -i <starting_id> -p <period_split> ' +
                  '-pr <previous_file_path> -cr <current_file_path>')
            sys.exit()
        elif opt in ("-s", "--survey_file"):
            survey_config_file_path = arg
        elif opt in ("-r", "--region_file"):
            region_list_file_path = arg
        elif opt in ("-e", "--enterprise_file"):
            enterprise_list_file_path = arg
        elif opt in ("-o", "--output_file"):
            output_file_path = arg
        elif opt in ("-i", "--starting_id"):
            ruref = int(arg)
        elif opt in ("-p", "--period_split"):
            split = arg
        elif opt in ("-pr", "--previous_file_path"):
            previous_file_path = arg
        elif opt in ("-cr", "--current_file_path"):
            current_file_path = arg

    with open(survey_config_file_path, "r") as survey_config_file:
        survey_config = json.load(survey_config_file)

    regions = pd.read_csv(region_list_file_path)
    enterprises = pd.read_csv(enterprise_list_file_path, )

    output_df = pd.DataFrame(columns=survey_config['data_frame_columns'])
    column_order = output_df.columns

    # generate the required enterprises
    for enterprise_index in range(0, min(survey_config['number_of_enterprises'],
                                         len(enterprises.index))):
        # pick enterprise name and id from list file
        enterprise_name = enterprises.iloc[enterprise_index, 0]
        enterprise_ref = enterprises.iloc[enterprise_index, 1]

        # decide on a number of subsidiaries the enterprise has
        number_of_subsidiaries = random.randrange(1, 5)

        # for each subsidiary
        for subsidiary_index in range(0, number_of_subsidiaries):
            # generate a ruref
            ruref += 1

            # pick a region from list file
            subsidiary_region = regions.iloc[random.randrange(0, len(regions.index)), 0]

            # for each period
            for period in survey_config['periods']:
                # add new row to the output
                response_df = pd.DataFrame({
                    "period": period,
                    "responder_id": ruref,
                    "enterprise_ref": enterprise_ref,
                    "name": enterprise_name,
                    "gor_code": subsidiary_region
                }, index=[0])

                # decide if non-respondent
                if random.random() > survey_config['response_rate']:
                    response_df['response_type'] = 1

                    for value in survey_config['values']:
                        response_df[value['column_name']] = value['default']

                    # calculate all sum columns
                    for sum_column in survey_config['sum_columns']:
                        response_df[sum_column['column_name']] = 0
                else:
                    response_df['response_type'] = 2

                    # for each value in config
                    for value in survey_config['values']:
                        # if value should be 0
                        new_value = value['default']

                        # should value be a valid response
                        if random.random() <= value['probability_of_data']:
                            # generate a rand value from range in config
                            if 'max' in value:
                                new_value = random.randrange(value['min'], value['max'])
                            # generate a rang value from a range and
                            # the sum of specified columns
                            elif 'max_from' in value:
                                max_value = 0
                                for aggregated_column in value['max_from']:
                                    max_value += response_df.iloc[0][aggregated_column]

                                if max_value > value['min']:
                                    new_value = random.randrange(value['min'], max_value)

                        # save the value generaed above in the current response
                        response_df[value['column_name']] = new_value

                    # calculate all sum columns
                    for sum_column in survey_config['sum_columns']:
                        new_sum = 0
                        for data_column in sum_column['data']:
                            if sum_column['data'][data_column] == "+":
                                new_sum += response_df.iloc[0][data_column]
                            elif sum_column['data'][data_column] == "-":
                                new_sum -= response_df.iloc[0][data_column]
                        response_df[sum_column['column_name']] = new_sum

                # add this response to output data frame
                output_df = output_df.append(response_df, ignore_index=True)

    # save to csv
    output_df = output_df.ix[:, column_order]
    output_df.to_csv(output_file_path, header=True, index=False)

    # display last ruref
    print("------------------------------------------------------")
    print("Starting ruref for land/marine: " + str(ruref))
    print("------------------------------------------------------")

    # split into current and previous period files
    # unless split=False
    if split is True:
        previous_df = output_df[output_df['period'] == survey_config["periods"][0]]
        current_df = output_df[output_df['period'] == survey_config["periods"][1]]

        previous_df.to_json(previous_file_path, orient="records")
        current_df.to_json(current_file_path, orient="records")


if __name__ == "__main__":
    main(sys.argv[1:])
