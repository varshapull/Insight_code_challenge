#Import required libraries

import csv

#Function to calculate median for list of numbers

def calculate_median(num_list):

    sorted_list = sorted(num_list)

    n = len(num_list)
    if n < 1:
            return None
    if n % 2 == 1:
        #Round down if less than 0.5 else round up
            return int(round(sorted_list[n//2]))
    else:
            return int(round(sum(sorted_list[n//2-1:n//2+1])/2.0))

#Helper function to write generated results to output text files
# 1. medianvals_by_zip.txt
# 2. medianvals_by_date.txt

def write_output(data,output_file_name):
       with open(output_file_name,"w") as f:
        wr = csv.writer(f,delimiter='|') #Use '|' as delimiter
        wr.writerows(data)