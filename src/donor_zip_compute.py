
'''
This file contains Helper functions with compute median and total transaction amount
donated to recipient per zipcode

The rows from the file are streamed sequentially.


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


#Calculate Median values by recipient per zipcode (stream records one by one)

#Helper function to create the record to store streaming data

#Function takes a record which is preprocessed (pre_line) & a dictionary to create record for each streaming record
def create_record(pre_line,recipient_zip_info):

    CMTE_ID = pre_line[0] #CMTE_ID/ Recipient id
    Zipcode = pre_line[10][:5] #zipcode of donor
    R_median = calculate_median(recipient_zip_info[pre_line[0]][pre_line[10][:5]]) #rolling median computed till current record
    Total_txns = len(recipient_zip_info[pre_line[0]][pre_line[10][:5]]) #total number of transactions per zip code for recipient
    Total_amt = sum(recipient_zip_info[pre_line[0]][pre_line[10][:5]]) #total amount donated per zip code for recipient

    return [CMTE_ID,Zipcode,R_median,Total_txns,Total_amt] #returns a list

'''
#Function to create a dictionary holding all the data streamed so far
#Input parameters : pre_line (preprocessed line) & dictionary holding all data streamed so far (recipient_zip_info)
#Output :

This results in a nested dictionary with the structure:

 {CMTE_ID1 :
            { Zipcode1:[Transaction_amt]} , {Zipcode2:[Transaction_amt]},
  CMTE_ID2 :
            {Zipcode1 : [Transaction_amt]}

 }

#This function is called from within recipient_zipcode_func to generate output file.

'''

def create_recp_info(pre_line,recipient_zip_info):

    '''Condition 1: Check if recipient not present in recipient_zip_info. If not present,
    add the recipient as key and create another dictionary (as it's value) with zipcode as key and transaction amt as its value.recipient
    '''

    if pre_line[0] not in recipient_zip_info:

        recipient_zip_info[pre_line[0]] = {pre_line[10][:5]:[pre_line[14]]}

        Total_txns = len(recipient_zip_info[pre_line[0]][pre_line[10][:5]])

        rzip = [pre_line[0],pre_line[10][:5],pre_line[14],Total_txns,pre_line[14]]

        return rzip #Return cmte_id,zipcode, median, total_transactions and total_transaction_amt

        '''
        Condition 2: If CMTE_ID already exists as key, and if Zipcode exists as well, if the record
        belongs to the zipcode, append the transaction amount to the existing list of amount and increment total # transactions

        '''

    else:

        if pre_line[0] in recipient_zip_info:

            if pre_line[10][:5] in recipient_zip_info[pre_line[0]]:

                recipient_zip_info[pre_line[0]][pre_line[10][:5]].append(pre_line[14]) #Append trxn to existing list

                rzip = create_record(pre_line,recipient_zip_info)
                return rzip #return record

                '''
                Condition 3: If CMTE_ID already exists but zipcode does not , create a new dictionary as its value with new ZIpcode as key and corresponding
                transaction amt as value.

                '''

            else:
                #Updating CMTE_ID with new zipcode dictionary as it's value.
                recipient_zip_info[pre_line[0]].update({pre_line[10][:5]:[pre_line[14]]})
                rzip = create_record(pre_line,recipient_zip_info)
                return rzip #return record

'''
#Function which reads input file, checks for input considerations and outputs required data
#Input : Function takes filename as argument
#Output : Outputs a list of lists consisting of our streamed records
with CMTE_ID, Zipcode, Rolling median, Total # txns and Total amount donated per recipient by zipcode

'''

def recipient_zipcode_func(filename):

    #List to hold lists containing donor contribution information
    recipient_info = []

    #Dictionary to hold all data streamed so far for donor information
    recipient_zip_info = {}

    with open(filename) as f:
        for line in f: #Iterating through each line (simulating streaming sequentially)
            #Split each row by '|'
            pre_line = line.split('|')
            #Put preprocessing logic into place
            #Check if strings are numeric and convert int if true
            pre_line = [ x if x == pre_line[10] else int(x) if re.match('^[-+]?[0-9]+$',x) else x for x in pre_line]

            #Check valid zipcode in terms of characters
            if len(pre_line[10]) < 5 or len(pre_line[10]) > 9:
                continue

            #Check if OTHER_ID is not empty - if it is not empty or null  go to next row
            elif pre_line[15] != '':
                continue

            else:
            #Checks to validate CMTE_ID , Zipcode and transaction amount

                if pre_line[0] != '' and pre_line[10] != '' and pre_line[14] != '':

                    recipient_record = create_recp_info(pre_line,recipient_zip_info) #Creates list holding data
                    recipient_info.append(recipient_record) #Add record



    return recipient_info

