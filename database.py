import os
import re

starting_path = "database/user_record/"

def create_user(account_number, first_name, last_name, email, password):
    # Create new user in database
    success = False

    try:
        f = open(starting_path + account_number + ".txt", 'x')
        
    except FileExistsError:
        print("User account already exists")
        # Read existing file
        
    else:
        user_details = first_name + "," + last_name + "," + email + "," + password + "," + str(0)
        f.write(user_details)
        success = True
    
    finally:
        f.close()
        return success


def read_user(account_number):
    # Read existing user in database
    account_path = re.search("^0[0-9]{9}(\.txt)$", account_number)
    plain_account_number = re.search("^0[0-9]{9}", account_number)
    
    try:
        if account_path != None:
            f = open(starting_path + account_number, 'r')
        elif plain_account_number != None:
            f = open(starting_path + account_number + ".txt", 'r')
        else:
            print("Invalid account number format")
    
    except FileNotFoundError:
        print("User not found...")
    
    except TypeError:
        print("Invalid account number format...")

    else:
        data = f.read()
        f.close()
        return data

    
def update_user(account_number, pos, new_data):
    # Update existing user details in specified position
    modified_user_details = ""
    
    # read user detail into a list and modify desired position
    data_list = str.split(read_user(account_number), ',')
    data_list[pos] = new_data
    
    for detail in data_list:
        if detail == data_list[-1]:
            modified_user_details += detail  # do not add a trailing comma after the last list item
        else:
            modified_user_details += (detail + ",")  # add detail and trailing comma
    
    # open file for writing and append modified user details
    f = open(starting_path + account_number + ".txt", 'w')
    f.write(modified_user_details)
    f.close()


def delete_user(account_number):
    # Delete existing user file in database

    success = False
    path = starting_path + account_number + ".txt"
    
    if os.path.exists(path):
        os.remove(path)
        # print("Delete successful")
        success = True

    else:
        print("User file not found. Try again...")
    
    return success
