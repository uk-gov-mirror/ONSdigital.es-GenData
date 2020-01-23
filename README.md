# DataGen.py

This script allows the user to quickly generate a data response file for the BMI surveys. It generates this synthetic data based on input configuration and lists which can be specified in command-line arguments (listed below). 

## Usage
To execute cd into the directory for this repo and execute:

    DataGen.py -s <survey_file> -r <region_file> -e <enterprise_file> -o <output_file> -i <starting_id> -p <period_split>

All arguments are optional as the default values are set to point at files within the repo. 

Outputs the last ruref to the console for continuation, e.g. for creating land and marine data, which is to be passed in as an argument as detailed below.

## Arguments:
### -s / survey_file
Path to the file which contains the configuration for the survey you want to generate. To make your own, look at the section about file structures below.

Default: `fixtures/configs/sample_survey.json`

### -r / region_file
Path to the file which contains a comma and line separated list of region codes. To make your own, look at the section about file structures below.

Default: `fixtures/region_list.csv`

### -e / enterprise_file
Path to the file which contains a comma and line separated list of enterprise names and ids. To make your own, look at the section about file structures below.

Default: `fixtures/enterprise_list.csv`

### -o / output_file
Path to target output file doesn't have to exist yet as this script will create (and overwrite) it. (Should exclude file type.)

Default: `fixtures/outputs/sample_out`

### -i / starting_id
The number from which the numbering of respondents should start above (the first id will be 1 higher than the number you provide). The value must be a whole number, containing only digits 0-9 and it must not start with a '0'.

Default: `10000000000`

### -p / period_split
Boolean value to determine if the output is to be split into two separate files;
* current period
* previous period

to be saved in the fixtures/outputs directory.
Default: `True`

## Requirements

    Python 3.7

with libraries:

    pandas
    getopt
    json
    random
    sys

# Files
## Survey Config File:
Is a json file with the following content required

    "data_frame_columns": [
        "period",
        "responder_id",
        "response_type",
        "region",
        "enterprise_reference",
        "enterprise_name",
        "data_0",
        "data_1",
        "data_2",
        "data_3",
        "sum_1",
        "sum_2" ]

The first 6 columns are required, you can have any number of `data_###` and `sum_###` columns you want as documented below.

### period

    "periods": [201812, 201903]

This list of two periods will determine how many periods each respondent will reply to, note that each enterprise will have between 1 and 5 respondents, each replaying for ALL periods. 

### number of enterprises

    "number_of_enterprises": 10,
    "min_subsidiaries":1,
    "max_subsidiaries":5

This is the number of unique enterprises with names to generate, not that if you require more than 30 you will need to supply your own enterpriseList.csv file as the default only has 30 entries. The software will automatically cap at this number. Names are assigned sequentially.

You may also specify the min/max number of responders that each enterprise may have.

NOTE: The code chooses a random number between the minimum and the maximum.

### response rate

    "response_rate": 0.5

This will determine how many of the responses (individual per respondent and period) will be filled with synthetic data. Any data that is labelled as a non-response will use the 'default' value (explained below).

### value columns

    "values":[ {"column_name": "data_###", "probability_of_data": 0.5, "default": 0, "min": 1, "max": 100}, ...]
The list of value columns to generate. Each is a dictionary with the following properties:

| Key            | Expected value                                                                                                              |
|----------------|-----------------------------------------------------------------------------------------------------------------------------|
| `column_name`         | Must match one of the `data_###` items from the `data_frame_columns` list above (String)                                    |
| `probability_of_data` | How likely is it that this field has a response, if it doesn't it will be populated with the value of `default` (Float)     |
| `default`             | Value used for empty responses (either because the whole response or just this value is under the response threshold) (any) |
| `min`                 | The lowest value to use for those responses, inclusive (Int)                                                                |
| `max` *1**            | The highest value to use for those responses, exclusive (Int)                                                               |
| `max_from` *1**       | A list of strings mapping to the columns declared earlier. For example: `["data_0", "data_1", ...]`. The script will add the value of the columns provided *2** and set it as the max. If that value is less then the `min` value, this row will be populated by the `default` value instead.

*1** *Use the `max` column **or** the `max_from` column, not both.*

*2** *The columns to consider must be listed **before** the one with a `max_from` field*

NOTE: If you want every row to have the default value you should set the `probability_of_data` to `0` to specify that no data will be calculated.

### sum columns

    "sum_columns": [
        {   
            "column_name": "sum_1",
            "data": {
                "data_0": "+",
                "data_1": "-"
            }
        },
        ...
    ]

This is a list of sum columns you want to generate. The values provided in `column_name` and in the `data` list must match the values listed in `data_frame_columns`.

| Key | Expected value |
| --- | -------------- |
| `column_name` | Name of the sum column, must be one of the names listed in `data_frame_columns`. |
| `data`        | Dict of column names that will be included to create the sum and whether they should be added or subtracted. These names must be listed in the `data_frame_colums` list. |

## Region List File
This must be a csv file listing region codes, usually just 2 letters. Each region is given its own line like this:

    AA,
    BB,
    ...,
    ZZ

Longer codes are allowed by this script but may not be compatible with the code run of the sample file produces.
Note that there is no header for this table.

## Enterprise List File
This must be a csv file listing enterprise names and 10 digit enterprise ids. Each of those pairs is on its own row like this:

    enterprise_name, enterprise_reference
    Apples with Alice, 1000000001
    Bannans by Bob, 1000000002
    ...
    Zucchinis from Zack, 9999999999

Enterprise names have only been tested to contain letters a-z, A-Z and spaces, but other characters may work too. The id has to be numeric made of 10 digits (0-9) and can not start with a '0'.

## Output File
This will be produced by the script. Please specify a file name and location (excluding file type. e.g. 'fixtures/outputs/sand_gravel') that the script can write to. 

**Warning:** this script **will overwrite** the file you specify, if making multiple files make sure to change this argument or make a copy of this file in a safe location between executions.
<hr>

# LookupGen.py
This script allows the user to quickly generate a data loopup file for the BMI Sand And Gravel survey.
## Usage
To execute cd into the directory for this repo and execute:

    LookupGen.py -i <input_file> -r <region_file> -c <county_file>

## Arguments:
### -i / input_file
Path to the file which contains the input data for the survey you want to generate.
Default: `fixtures/outputs/sample_out_all.csv`

### -r / region_file
Path to the file which contains a comma and line separated list of region codes. To make your own, look at the section about file structures below.

Default: `fixtures/region_list.csv`

### -c / county
Path to the file which contains a lookup of gor_codes mapped to regions.
Default: `fixtures/county_lookup.json`

## Requirements

    Python 3.7

with libraries:

    pandas
    getopt
    json
    random
    sys

# Combine.py
This script allows the user to quickly generate a data loopup file for the BMI Sand And Gravel survey.
## Usage
To execute cd into the directory for this repo and execute:

    Combine.py -m <marine_file> -l <land_file> -o <out_file>

## Arguments:
### -m / marine_file
Default: `fixtures/outputs/sample_out_current.csv`

### -l / land_file
Default: `fixtures/outputs/sample_out_previous.csv`

### -o / out_file
Default: `fixtures/outputs/sample_merged.csv`

## Requirements

    Python 3.7

with libraries:

    pandas
    getopt
    sys
