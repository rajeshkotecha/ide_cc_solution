# ide_cc_solution
Insight Data Engineering Code Challenge Solution

The main data structure used to generate the desired output is dictionary. 

# Median Value by Zip: 
Dictionary Key: recepient ID + zip_code

Dictionary Value: a list consisting of three values [transaction_count, total_amt, [a list consisting of donation amounts]]

# Median Value by Date: 
Dictionary Key: recepient ID + transaction_date in the format YYYYMMDD

Dictionary Value: a list consisting of four values [transaction_count, total_amt, [a list consisting of donation amounts], transaction_date in the format MMDDYYYY]

To calculate median sorting of all amount values for a given key is required. To make the program efficient on large volume of data the amount list is always kept sorted as new amount value is received into the list from input stream. The new amount value is inserted in the list in such a way that the amount list remains sorted all the time for all key values. 

The date field in dictionary key is stored in the format YYYYMMDD to enable sorting of dates in chronological order. In the dictionary value the same field is stored in format MMDDYYYY for writing to output file purpose.







