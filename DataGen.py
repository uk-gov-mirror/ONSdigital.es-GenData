#!/usr/bin/python

import sys

no_of_enterprises = 10

def main():
    # generate the required entrprises
    for ent in range(0, no_of_enterprises):
        ## pick enterprise name and id from dictionary file
        
        ## decide on a number of subsidiaries the enterprise has
        ## for each subsidiary 
            ## generate a ruref
            ## decide if non-respondent
            ## pick a region from dictionary file
            ## for each period
                ## satart with sum = 0
                ## for each value in config
                    ## if value should be 0
                        ## set to 0
                    ## if value should be a response
                        ## generate a rand value from range in config
                        ## add to sum column
                ## save all data for this period to csv

if __name__ == "__main__":
    main()
