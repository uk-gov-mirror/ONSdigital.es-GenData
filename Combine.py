#!/usr/bin/python

import pandas as pd


def main():
    land = "fixtures/out.csv"
    marine = "fixtures/marine_out.csv"

    land_df = pd.read_csv(land)
    marine_df = pd.read_csv(marine)

    combined = pd.concat([land_df, marine_df], axis=0)
    # print(combined)

    with open("fixtures/land_marine_merged.csv", "w") as merged:
        combined.to_csv(merged, header=False, index=False)


main()
