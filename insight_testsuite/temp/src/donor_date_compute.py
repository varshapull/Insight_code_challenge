import time
import re
import csv
import sys
from datetime import datetime
import operator

from helper_func import write_output,calculate_median
#Calculate median values for recipient per date

#Helper function to create dictionary to hold each recipient's date data

def date_contrib_func(row,date_contribution_data_dict):
    #date_contribution_data = []

    if row[0] not in date_contribution_data_dict:
        date_contribution_data_dict[row[0]] = {row[13]:[row[14]]}

    else:

        if row[0] in date_contribution_data_dict:
            if row[13] in date_contribution_data_dict[row[0]]:

                date_contribution_data_dict[row[0]][row[13]].append(row[14])
            else:

                date_contribution_data_dict[row[0]].update({row[13]:[row[14]]})

    return date_contribution_data_dict


# Function to preprocess the file and validate the rows to incorporate input considerations

"""
- Input considerations for median values for date:
    1. Check CMTE_ID is empty or NULL
    2.

"""


def pre_process_func(filename):

    date_contri_dict = {}


    with open(filename) as f:

        for line in f:
            pre_line = line.split('|')

            try:
                pre_line = [ datetime.strptime(x,"%m%d%Y").date() if x == pre_line[13] else int(x) if re.match('^[-+]?[0-9]+$',x) else x for x in pre_line]
                pre_line[13].strftime('%m%d%Y')  #Check valid date

            except ValueError:
                continue


            if pre_line[15] != '':
                continue

            else:

                if pre_line[0] != '' and pre_line[13] != '' and pre_line[14] != '':
                    #if pre_line[15] in ('','NULL'): #Check valid date
                    date_contribution_data_ = date_contrib_func(pre_line,date_contri_dict)



    return date_contribution_data_



#Compute stats for each recipient by date

def compute_recp_stats(date_dictionary):

    date_stats =[]


    for key, value in date_dictionary.iteritems():
        for k,v in value.iteritems():

            total = reduce(lambda x,y: x+y,v) #Compute total amt for each recipient on given date
            median = calculate_median(v) #Calculate median amt for each recipient on given date
            total_txns = len(v) #Compute total transaction for each recipient on given date
            contribution_date = k.strftime("%m%d%Y")  #Format datetime type to string
            date_stats.append([key,contribution_date,median,total_txns,total])

    #Sort recipient data according to CMTE_ID and Date
    date_stats = sorted(date_stats, key=operator.itemgetter(0,1))


    return date_stats