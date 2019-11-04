#!/usr/bin/python

import sys
import json
import random
import pandas as pd

def main():

    with open("resources/sampleSurvey.json", "r") as survey_config_file:
        survey_config = json.load(survey_config_file)

    regions = pd.read_csv("resources/regionList.csv")
    enterprises = pd.read_csv("resources/enterpriseList.csv", )

    sub_ref = 10000000000
    
    output_df = pd.DataFrame(columns=survey_config['data_frame_columns'])
    column_order = output_df.columns

    # generate the required entrprises
    for ent_idx in range(0, min(survey_config['number_of_enterprises'], len(enterprises.index))):
        # pick enterprise name and id from list file
        ent_name = enterprises.iloc[ent_idx, 0]
        ent_ref = enterprises.iloc[ent_idx, 1]
        #print(ent_idx, ent_name)
        
        # decide on a number of subsidiaries the enterprise has
        number_of_subsidiaries = random.randrange(1,5)
        
        # for each subsidiary 
        for sub_idx in range(0, number_of_subsidiaries):
            # generate a ruref
            sub_ref += 1
            
            # pick a region from list file
            sub_region = regions.iloc[random.randrange(0, len(regions.index)), 0]
            #print (sub_ref, sub_region)

            # for each period
            for period in survey_config['periods']:
                # add new row to the output
                response_df = pd.DataFrame({
                    "period": period,
                    "ruref": sub_ref,
                    "ent_ref": ent_ref,
                    "ent_name": ent_name
                }, index=[0])

                # decide if non-respondent
                if(random.random() > survey_config['response_rate']):
                    response_df['response_type'] = 1

                    for value in survey_config['values']:
                        response_df[value['col_name']] = value['default']

                    response_df['sum'] = 0
                    #print(response_df)
                else:
                    response_df['response_type'] = 2
                    response_sum = 0
                    
                    # for each value in config
                    for value in survey_config['values']:
                        # if value should be 0
                        new_value = value['default']

                        # should value be a valid response
                        if (random.random() <= value['prob_of_data']):
                            # generate a rand value from range in config
                            new_value= random.randrange(value['min'], value['max'])
                        
                        # assign response value
                        response_df[value['col_name']] = new_value

                        # add to sum column
                        response_sum += new_value

                    response_df['sum'] = response_sum
                
                # add this response to output data frame
                output_df = output_df.append(response_df, ignore_index=True)
            
    # save to csv
    output_df = output_df.ix[:, column_order]
    output_df.to_csv("resources/out.csv", header=False)

if __name__ == "__main__":
    main()
