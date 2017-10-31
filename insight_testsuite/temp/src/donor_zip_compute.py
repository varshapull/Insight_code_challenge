import time
import re
import csv
import sys
from datetime import datetime
import operator

from helper_func import write_output,calculate_median


#Calculate Median values by recipient per zipcode(streaming)

#Helper function to create the streaming record

def create_record(pre_line,recipient_zip_info):

    CME_ID = pre_line[0]
    Zipcode = pre_line[10][:5]
    R_median = calculate_median(recipient_zip_info[pre_line[0]][pre_line[10][:5]])
    Total_txns = len(recipient_zip_info[pre_line[0]][pre_line[10][:5]])
    Total_amt = sum(recipient_zip_info[pre_line[0]][pre_line[10][:5]])

    return [CME_ID,Zipcode,R_median,Total_txns,Total_amt]



def calculate_recp_info(pre_line,recipient_zip_info):


    if pre_line[0] not in recipient_zip_info:

        recipient_zip_info[pre_line[0]] = {pre_line[10][:5]:[pre_line[14]]}

        Total_txns = len(recipient_zip_info[pre_line[0]][pre_line[10][:5]])

        rzip = [pre_line[0],pre_line[10][:5],pre_line[14],Total_txns,pre_line[14]]

        #recipient_info.append(rzip)
        return rzip


    else:

        if pre_line[0] in recipient_zip_info:

            if pre_line[10][:5] in recipient_zip_info[pre_line[0]]:



                recipient_zip_info[pre_line[0]][pre_line[10][:5]].append(pre_line[14])

                rzip = create_record(pre_line,recipient_zip_info)
                return rzip

            else:

                recipient_zip_info[pre_line[0]].update({pre_line[10][:5]:[pre_line[14]]})
                rzip = create_record(pre_line,recipient_zip_info)
                return rzip


'''
Create dictionary holding "CME_ID" : "Zipcode" : [transaction_amts]

'''

def recipient_zipcode_func(filename):

    #List to hold dictionaries containing contribution information
    recipient_info = []

    recipient_zip_info = {}

    with open(filename) as f:
        for line in f:
            #Cast numeric type to int
            pre_line = line.split('|')
            pre_line = [ x if x == pre_line[10] else int(x) if re.match('^[-+]?[0-9]+$',x) else x for x in pre_line]
                 #Check valid zipcode
            if len(pre_line[10]) < 5 or len(pre_line[10]) > 9:
                continue


            elif pre_line[15] != '':
                continue

            else:

                if pre_line[0] != '' and pre_line[10] != '' and pre_line[14] != '':

                    recipient_record = calculate_recp_info(pre_line,recipient_zip_info)
                    recipient_info.append(recipient_record)



    return recipient_info

