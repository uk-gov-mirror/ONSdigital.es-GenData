import getopt
import sys

import pandas as pd


def main(argv):

    marine_file_name = 'fixtures/outputs/sample_out_current.csv'
    land_file_name = 'fixtures/outputs/sample_out_previous.csv'
    out_file_name = 'fixtures/outputs/sample_merged.csv'

    try:
        opts, args = getopt.getopt(argv, "hm:l:o", ["marine_file=",
                                                    "land_file=",
                                                    "out_file=",
                                                    ])
    except getopt.GetoptError:
        print('Combine.py -i <input_file> -r <region_file> -c <county_file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Combine.py -m <marine_file> -l <land_file> -o <out_file>')
            sys.exit()
        elif opt in ("-m", "--marine_file"):
            marine_file_name = arg
        elif opt in ("-l", "--land_file"):
            land_file_name = arg
        elif opt in ("-o", "--out_file"):
            out_file_name = arg
    land_df = pd.read_csv(land_file_name)
    marine_df = pd.read_csv(marine_file_name)

    combined = pd.concat([land_df, marine_df], axis=0)

    with open(out_file_name, "w") as merged:
        combined.to_csv(merged, header=True, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
