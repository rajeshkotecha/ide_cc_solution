import math
import datetime
import sys


def validate_date (date_mmddyyyy):
    valid_date = None

    # Date is invalid if it does not contain exactly 8 characters
    if (len (date_mmddyyyy) != 8):
        valid_date = False
        return valid_date
   
    # Date is invalid if it contains a non-numeric character 
    try: 
        year = int (date_mmddyyyy [4:])
        month = int (date_mmddyyyy [:2])
        day = int (date_mmddyyyy [2:4])
    except ValueError:
        valid_date = False
        return valid_date
    
    # Date is invalid if either year, month or day is invalid
    try:
        create_date = datetime.datetime (year, month, day)
        valid_date = True
    except ValueError:
        valid_date = False

    return valid_date


def validate_zip (zip_code):
    valid_zip_code = None

    # If zip is null or contains less than 5 characters it is not valid. 
    if (len (zip_code) < 5):
        valid_zip_code = False
    else:
        valid_zip_code = True

    return valid_zip_code
   

def convert_date (date_mmddyyyy):
    # Converts date from MMDDYYYY format to YYYYMMDD for sorting purpose
    year = date_mmddyyyy [4:]
    month = date_mmddyyyy [:2]
    day = date_mmddyyyy [2:4]
    date_yyyymmdd = "".join ([year, month, day])
  
    return date_yyyymmdd


def insert_amt (amt, amts_list):
    # The input list amts_list is sorted. We need to insert amt at the right location
    # so that the list remains sorted. 

    num_of_amts = len (amts_list)

    amt_index = num_of_amts # Let us first assume that amt is higher than all 
                            # elements in the list so its location is at the end of list. 

    # Find the right location for amt in the list traversing from left to right
    for i in range (num_of_amts):
        if amts_list[i] >= amt:
            amt_index = i # This is the right location
            break

    amts_list.insert (amt_index, amt) # Insert amt at the location
    return None # Since the amts_list is mutable we do not need to return anything


def find_median (amts_list):
    num_of_amts = len (amts_list)

    # The input list is sorted

    # If the list contains odd number of members pick the middle one
    # If the list contains even number of members find middle two members and
    # calculate their mean

    if num_of_amts % 2 == 1:
        median = amts_list [num_of_amts // 2]

    else:
        pos_first_middle = (num_of_amts // 2) - 1
        pos_second_middle = (num_of_amts // 2) + 1 # Add 1 since we slice the list below
        median = sum (amts_list [pos_first_middle : pos_second_middle]) / 2.0


    # If median < 0.50 it should be dropped to zero. 
    # If median >= 0.50 it should be rounded to the next dollar amount. 

    if median < 0.5:
       median = 0
    else:
       median = math.ceil (median)

    return median


def write_output_by_date (fp_output_by_date, dict_by_date):
    for i in sorted (dict_by_date.keys ()):
        fp_output_by_date.write (i[:-8] + '|' + 
                                 dict_by_date [i][3] + '|' +
                                 repr (find_median (dict_by_date [i][2])) + '|' +
                                 repr (dict_by_date [i][0]) + '|' +
                                 repr (math.ceil (dict_by_date [i][1])) + '\n')

 
def find_political_donors (debug=False):

    if len (sys.argv) != 4:
       print ("Usage: python " + sys.argv [0] + " <input data file> " + 
              "<output data file by zip> <output data file by date>")
       return None

    input_file = sys.argv [1]
    output_file_by_zip = sys.argv [2]
    output_file_by_date = sys.argv [3]

    output_data_by_zip = open (output_file_by_zip, "w")
    output_data_by_date = open (output_file_by_date, "w")
    dict_by_zip = {}
    dict_by_date = {}

    input_data = open (input_file, 'r')
    for line in input_data:
        fields = line.split ('|')
        cmte_id = fields [0]
        zip_code = fields [10][:5] # Take first five characters from ZIP_CODE field
        transaction_dt = fields [13]
        transaction_amt = float (fields [14])
        other_id = fields [15]

        # If OTHER_ID is not null or CMTE_ID is null or TRANSACTION_AMT is null
        # ignore the input record
        if ((other_id) or (not cmte_id) or (not transaction_amt)):
            continue

        if validate_zip (zip_code): 
            zip_key = cmte_id + zip_code
            if (zip_key) in dict_by_zip:
                dict_by_zip [zip_key][0] = dict_by_zip [zip_key][0] + 1
                dict_by_zip [zip_key][1] = dict_by_zip [zip_key][1] + transaction_amt
                insert_amt (transaction_amt, dict_by_zip [zip_key][2])
            else:
                dict_by_zip [zip_key] = [1, transaction_amt, [transaction_amt]]
            output_data_by_zip.write (cmte_id + '|' + zip_code + '|' +
                                      repr (find_median (dict_by_zip [zip_key][2])) + '|' +
                                      repr (dict_by_zip [zip_key][0]) + '|' +
                                      repr (math.ceil (dict_by_zip [zip_key][1])) + '\n')

        if validate_date (transaction_dt):
            transaction_dt_yyyymmdd = convert_date (transaction_dt)
            date_key = cmte_id + transaction_dt_yyyymmdd
            if (date_key) in dict_by_date:
                dict_by_date [date_key][0] = dict_by_date [date_key][0] + 1
                dict_by_date [date_key][1] = dict_by_date [date_key][1] + transaction_amt
                insert_amt (transaction_amt, dict_by_date [date_key][2])
            else:
                dict_by_date [date_key] = [1, transaction_amt, [transaction_amt], 
                                           transaction_dt]
            
                                      

        if debug:
            print ("cmte_id: " + cmte_id)
            print ("zip_code: " + zip_code)
            print ("transaction_dt: " + transaction_dt)
            print ("transaction_amt: ", transaction_amt)
            print ("other_id: " + other_id)
            print ("valid date: ", validate_date (transaction_dt))
            print ("convert date: ", convert_date (transaction_dt))
            print ("valid zip code: ", validate_zip (zip_code), "\n")
    
    write_output_by_date (output_data_by_date, dict_by_date)
    input_data.close()
    output_data_by_zip.close ()
    output_data_by_date.close ()


if __name__ == '__main__':
    find_political_donors (debug=False)

