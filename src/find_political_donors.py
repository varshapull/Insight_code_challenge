
#Import required libraries

import time
import re
import csv
import sys
from datetime import datetime
import operator

#Import helper functions from helper_func.py donor_date_compute.py & donor_zip_compute.py
from helper_func import write_output,calculate_median
from donor_date_compute import pre_process_func, compute_recp_stats
from donor_zip_compute import recipient_zipcode_func


#Main function to generate medianvals_by_zip.txt and medianvals_by_date.txt

def main():

    # Generate medianvals_by_zip file
    medianval_by_zip = recipient_zipcode_func(sys.argv[1]) #returns donor contribution to recipient by zipcode
    write_output(medianval_by_zip,sys.argv[2]) #write output file medianvals_by_zip.txt

    #Generate medianvals_by_date file
    clean_data = pre_process_func(sys.argv[1]) #Preprocesses data
    medianval_by_date = compute_recp_stats(clean_data) #returns donor contribution to recipient by date
    write_output(medianval_by_date,sys.argv[3]) #write output to file : medianvals_by_date.txt

#Execute main function

if __name__ == '__main__':
    main()







