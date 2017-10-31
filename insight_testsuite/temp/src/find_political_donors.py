
#Load required libraries

import time
import re
import csv
import sys
from datetime import datetime
import operator


from helper_func import write_output,calculate_median
from donor_date_compute import pre_process_func, compute_recp_stats
from donor_zip_compute import recipient_zipcode_func


#Main function to generate medianvals_by_zip.txt and medianvals_by_date.txt

def main():

    #Call to generate medianval_by_zip file
    medianval_by_zip = recipient_zipcode_func(sys.argv[1])
    write_output(medianval_by_zip,sys.argv[2])

    #Call to generate medianval_by_date file
    clean_data = pre_process_func(sys.argv[1])
    medianval_by_date = compute_recp_stats(clean_data)
    write_output(medianval_by_date,sys.argv[3])

#Execute main function

if __name__ == '__main__':
    main()






# print (end-start)
# #print recipient_zip_info

# print "--------"


# print "-------"


# #Write list of dictionaries to tsv file

# with open(sys.argv[2],"w") as f:
#     wr = csv.writer(f,delimiter='|')
#     wr.writerows(output)





