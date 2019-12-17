import getopt
import json
import random
import sys

import pandas as pd


def main(argv):

    survey_config_file_path = 'fixtures/configs/sample_survey.json'
    region_list_file_path = 'fixtures/region_list.csv'
    enterprise_list_file_path = 'fixtures/enterprise_list_1.csv'
    output_file_path = 'fixtures/outputs/sample_out'
    ruref = 10000000000
    split = True

    try:
        opts, args = getopt.getopt(argv, "hs:r:e:o:i:p", ["survey_file=",
                                                          "region_file=",
                                                          "enterprise_file=",
                                                          "output_file=",
                                                          "starting_id=",
                                                          "period_split="
                                                          ])
    except getopt.GetoptError:
        print('DataGen.py -s <survey_file> -r <region_file> -e <enterprise_file> ' +
              '-o <output_file> -i <starting_id> -p <period_split>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('DataGen.py -s <survey_file> -r <region_file> -e <enterprise_file> ' +
                  '-o <output_file> -i <starting_id> -p <period_split>')
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

    with open(survey_config_file_path, "r") as survey_config_file:
        survey_config = json.load(survey_config_file)

    regions = pd.read_csv(region_list_file_path)
    enterprises = pd.read_csv(enterprise_list_file_path)

    output_df = pd.DataFrame(columns=survey_config['data_frame_columns'])
    column_order = output_df.columns

    # Generate the required enterprises.
    for enterprise_index in range(0, min(survey_config['number_of_enterprises'],
                                         len(enterprises.index))):
        # Pick enterprise name and id from list file.
        enterprise_name = enterprises.iloc[enterprise_index, 0]
        enterprise_ref = enterprises.iloc[enterprise_index, 1]

        # Decide on a number of subsidiaries the enterprise has.
        number_of_subsidiaries = random.randrange(survey_config['min_subsidiaries'],
                                                  survey_config['max_subsidiaries'])

        # For each subsidiary.
        for subsidiary_index in range(0, number_of_subsidiaries):
            ruref += 1

            # Pick a region from list file.
            subsidiary_region = regions.iloc[random.randrange(0, len(regions.index)), 0]

            # For each period.
            for period in survey_config['periods']:
                # Add new row to the output.
                response_df = pd.DataFrame({
                    "period": period,
                    "responder_id": ruref,
                    "enterprise_ref": enterprise_ref,
                    "enterprise_name": enterprise_name,
                    "gor_code": subsidiary_region
                }, index=[0])

                # Decide if non-respondent.
                if random.random() > survey_config['response_rate']:
                    response_df['response_type'] = 1

                    for value in survey_config['values']:
                        response_df[value['column_name']] = value['default']

                    # Calculate all sum columns.
                    for sum_column in survey_config['sum_columns']:
                        response_df[sum_column['column_name']] = 0
                else:
                    response_df['response_type'] = 2

                    # For each value in config.
                    for value in survey_config['values']:
                        # If value should be 0.
                        new_value = value['default']

                        # Should value be a valid response.
                        if random.random() <= value['probability_of_data']:
                            # Generate a random value from a range in config.
                            if 'max' in value:
                                new_value = random.randrange(value['min'], value['max'])
                            # Generate a random value from a range and
                            # the sum of specified columns.
                            elif 'max_from' in value:
                                max_value = 0
                                for aggregated_column in value['max_from']:
                                    max_value += response_df.iloc[0][aggregated_column]

                                if max_value > value['min']:
                                    new_value = random.randrange(value['min'], max_value)

                        # Save the value generated above in the current response.
                        response_df[value['column_name']] = new_value

                    # Calculate all sum columns.
                    for sum_column in survey_config['sum_columns']:
                        new_sum = 0
                        for data_column in sum_column['data']:
                            if sum_column['data'][data_column] == "+":
                                new_sum += response_df.iloc[0][data_column]
                            elif sum_column['data'][data_column] == "-":
                                new_sum -= response_df.iloc[0][data_column]
                        response_df[sum_column['column_name']] = new_sum

                # Add this response to output DataFrame.
                output_df = output_df.append(response_df, ignore_index=True)

    output_df = output_df.ix[:, column_order]
    output_df.to_csv(output_file_path + "_all.csv", header=True, index=False)
    output_df.to_json(output_file_path + "_all.json", orient="records")

    # Display last ruref.
    print("------------------------------------------------------")
    print("Final RU Reference: " + str(ruref))
    print("------------------------------------------------------")

    # Split into current and previous period files.
    if split is True:
        previous_df = output_df[output_df['period'] == survey_config["periods"][0]]
        current_df = output_df[output_df['period'] == survey_config["periods"][1]]

        previous_df.to_csv(output_file_path + "_previous.csv", header=True, index=False)
        previous_df.to_json(output_file_path + "_previous.json", orient="records")

        current_df.to_csv(output_file_path + "_current.csv", header=True, index=False)
        current_df.to_json(output_file_path + "_current.json", orient="records")


if __name__ == "__main__":
    main(sys.argv[1:])
