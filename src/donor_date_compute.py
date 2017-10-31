'''
This file contains Helper functions with compute median and total transaction amount
donated to recipient per date

'''

#Import required libraries

import time
import re
import csv
import sys
from datetime import datetime
import operator

#Import helper functions from helper_func.py

from helper_func import write_output,calculate_median

'''

#Helper function to create dictionary to hold each recipient's date data
##Function takes a record which is preprocessed (row) & a dictionary to create recipient record for each date

This results in a nested dictionary with the structure:

 {CMTE_ID1 :
            { date1:[Transaction_amt]} , {date2:[Transaction_amt]},
  CMTE_ID2 :
            {date1 : [Transaction_amt]}

 }

 '''

def date_contrib_func(row,date_contribution_data_dict):

    #Condition 1: Check if recipient (CMTE_ID) is present in date_contribution_data_dict

    if row[0] not in date_contribution_data_dict:
        date_contribution_data_dict[row[0]] = {row[13]:[row[14]]}

    else:
        #Condition 2: If CMTE_ID exists and date exists in dictionary, add it to the list of transaction amts
        if row[0] in date_contribution_data_dict:
            if row[13] in date_contribution_data_dict[row[0]]:

                date_contribution_data_dict[row[0]][row[13]].append(row[14])
            else:
            #Condition 3: If date not present, update dictionary with new date and corresponding transaction amt
                date_contribution_data_dict[row[0]].update({row[13]:[row[14]]})

    return date_contribution_data_dict #return nested dictionary with donation information for each recipient by date


#Function to preprocess each line of input file and check for valid dates, transactions amts
#OTHER_ID and CMTE_ID

def pre_process_func(filename):

    #Dictionary to hold all donor information
    date_contri_dict = {}


    with open(filename) as f:

        for line in f:
            pre_line = line.split('|')

            #Convert string to date format and account for date validity.
            #Check if strings are numeric and convert to int if true
            try:
                pre_line = [ datetime.strptime(x,"%m%d%Y").date() if x == pre_line[13] else int(x) if re.match('^[-+]?[0-9]+$',x) else x for x in pre_line]
                pre_line[13].strftime('%m%d%Y')  #Check valid date

            except ValueError: #IF exception caught, skip the row and go to next row
                continue

            #Check if OTHER_ID is not null or empty
            if pre_line[15] != '':
                continue

            else:
                #Check to validate CMTE_ID , date and transaction amount
                if pre_line[0] != '' and pre_line[13] != '' and pre_line[14] != '':
                   #Create list to hold donor information per recipient by date
                    date_contribution_data_ = date_contrib_func(pre_line,date_contri_dict)



    return date_contribution_data_



#Compute stats for each recipient by date

def compute_recp_stats(date_dictionary):

    #List of lists to hold each recipient information by date
    date_stats =[]

    #Iterate over date_dictionary and compute sum, median and total number of transactions
    for key, value in date_dictionary.iteritems():
        for k,v in value.iteritems():

            total = reduce(lambda x,y: x+y,v) #Compute total amt for each recipient on given date
            median = calculate_median(v) #Calculate median amt for each recipient on given date
            total_txns = len(v) #Compute total transaction for each recipient on given date
            contribution_date = k.strftime("%m%d%Y")  #Format datetime type to string
            #Append each row of information to list
            date_stats.append([key,contribution_date,median,total_txns,total])

    #Sort recipient data according to CMTE_ID and Date
    date_stats = sorted(date_stats, key=operator.itemgetter(0,1))


    return date_stats