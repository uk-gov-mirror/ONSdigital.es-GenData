# # es-GenData

This script allows the user to quickly generate a data response file for the BMI surveys. It generates this synthetic data based on input configuration and lists which can be specified in command-line arguments (listed below). 

# Usage
To execute cd into the directory for this repo and execute:

    DataGen.py -s <survey_file> -r <region_file> -e <enterprise_file> -o <output_file> -id <starting_id>

All options are optional as the default values are set to point at files within the repo. 

## Options:
### -s / survey_file
Path to the file which contains the configuration for the survey you want to generate. To make your own, look at the section about file structures below.
Default: `resources/sampleSurvey.json`

### -r / region_file
Path to the file which contains a comma and line separated list of region codes. To make your own, look at the section about file structures below.
Default: `resources/regionList.csv`

### -e / enterprise_file
Path to the file which contains a comma and line separated list of enterprise names and ids. To make your own, look at the section about file structures below.
Default: `resources/enterpriseList.csv`

### -o / output_file
Path to target output file doesn't have to exist yet as this script will create (and overwrite) it. Should be in a .csv extension.
Default: `resources/out.csv`

### -id / starting_id
The number from which the numbering of respondents should start above (the first id will be 1 higher than the number you provide). The value must be a whole number, containing only digits 0-9 and it must not start with a '0'.
Default: `10000000000`

## Requirements

    Python 3.7

with libraries:

    pandas
    getopt
    json
    random
    sys

# Files
## Survey config file:
Is a json file with the following content required

    "data_frame_columns": ["period", "ruref", ..., "sum" ]
This list must contain all the named fields, so not the `data_0`, `data_1` ... columns, in the order in which you want them to appear in the final output file.
The `data_###` columns must appear one for each data column you want to generate (more on this below).

    "periods": [201903, 201906]

This list of periods will determine how many periods each respondent will reply to, note that each enterprise will have between 1 and 5 respondents, each replaying for ALL periods. 

    "number_of_enterprises": 10

This is the number of unique enterprises with names to generate, not that if you require more than 30 you will need to supply your own enterpriseList.csv file as the default only has 30 entries. The software will automatically cap at this number. Names are assigned sequentially.

    "response_rate": 0.5

This will determine how many of the responses (individual per respondent and period) will be filled with synthetic data. Any data that is labelled as a non-response will use the 'default' value (explained below).

    "values":[ {"col_name": "data_###", "prob_of_data": 0.5, "default": 0, "min": 1, "max": 100}, ...]
The list of value columns to generate. Each is a dictionary with the following properties:

| Key            | Expected value                                                                                                              |
|----------------|-----------------------------------------------------------------------------------------------------------------------------|
| `col_name`     | Must match one of the `data_###` items from the `data_frame_columns` list above (String)                                    |
| `prob_of_data` | How likely is it that this field has a response, if it doesn't it will be populated with the value of `default` (Float)     |
| `default`      | Value used for empty responses (either because the whole response or just this value is under the response threshold) (any) |
| `min`          | The lowest value to use for those responses, inclusive (Int)                                                                |
| `max`          | the highest value to use for those responses, exclusive (Int)                                                               |

## Region List file
This must be a csv file listing region codes, usually just 2 letters. Each region is given it's own line like this:

    AA,
    BB,
    ...,
    ZZ
Longer codes are allowed by this script but may not be compatible with the code run of the sample file produces.
Note that there is no header for this table.
## Enterprise List file
This must be a csv file listing enterprise names and 10 digit enterprise ids. Each of those pairs is on it's own row like this:

    Alice Apples, 1000000001
    Bob Bannans, 1000000002
    ...
    Zack Zucchinis, 9999999999
Enterprise names have only been tested to contain letters a-zA-Z and spaces, but other characters may work too. The id has to be numeric made of 10 digits (0-9) and can not start with a '0'.
## Output file
This will be produced by the script. Please specify a file name and location that the script can write to. 
**Warning:** this script **will overwrite** the file you specify, if making multiple files make sure to change this argument or make a copy of this file in a safe location between executions.