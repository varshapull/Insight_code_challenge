# Insight Coding Challenge : Finding political donors

## Goal

Generate two output files containing :

1. medianvals_by_zip.txt


This text file contains recipient id, zipcode , recipient running median of contributions received, total number of transactions and total amount by recipient from the contributor's zip code streamed in so far.


2. medianvals_by_date.txt

- This text file contains recipient id, zipcode, median of contributions received by recipient , total number of transactions and total amount received on that date.

---

## Approach

### Problem 1 : Rolling Median Values by Zip code for each recipient

Each row in the input file was streamed in a sequential manner.

- Preprocessing of each row consisted of :

1. Splitting on '|' delimiter
2. Convert numeric strings such as Transaction amt to numeric type
3. Each zip code was validated for length and missing values
4. Each transaction amount and CMTE_ID was checked for missing values and skipped if not present/valid

- A nested dictionary was created to store CMTE_ID and corresponding zipcode and transaction amount.
- The top level key being CMTE_ID and inner dictionary containing zipcode as key and transaction amount as value.
- This dictionary was used to keep track of new data in terms of zipcode or transaction amount  being added to a particular recipient (CMTE_ID).
- Based on this dictionary , the median , total # of transaction and total donation amount was calculated.
- This data was written to a text file.

### Problem 2: Median contribution by date for each recipient

All data was preprocessed and stored as a nested dictionary.

- Preprocessing of each row consisted of :

1. Splitting on '|' delimiter
2. Convert numeric strings such as Transaction amt to numeric type
3. Convert date string to date type and check for date validity
4. Each transaction amount and CMTE_ID was checked for missing values and skipped if not present/valid

- Once all the data had been preprocessed, a nested dictionary was constructed to to store CMTE_ID and corresponding date and transaction amount.
- The top level key being CMTE_ID and inner dictionary containing date as key and transaction amount as value.
- Based on this dictionary , the median , total # of transaction and total donation amount was calculated.
- The final output was written to a text file

## Notes on Code organization

The main file named "find_political_donors.py" is run using the shell script run.sh to execute the script. However, 3 additional files containing helper functions are imported in "find_political_donors.py"

These files are :
1. helper_func.py
2. donor_date_compute.py
3. donor_zip_compute.py

The main python script and all helper function scripts are present in the src folder.

