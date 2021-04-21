import os
import re
import mock_atm
import database


starting_path = "database/user_record/"


def PasswordChecker(passkey):
    """
    Confirms validity of newly created password. 
    Only passwords with at least 5 characters are accepted.

    Args:
        (str) passkey - a string of letters and numbers provided as password

    Returns:
        (str) passkey - an approved passkey of minimum 5 characters
    """
    while len(passkey) < 5:
        print('\n*****Password should have at least 5 characters*****')
        passkey = input('\nEnter password: ')
    else:
        return passkey


def account_number_exists(account_number):
    # Find existing user in database
    path = starting_path + account_number + ".txt"
    
    if os.path.exists(path):
        return True
    
    return False


def email_exists(email):
    accounts = os.listdir(starting_path)
   
    for account in accounts:
        user_details = str.split(database.read_user(account), ",")
        if email in user_details:
            return True
    
    return False


def EmailChecker(email):
    """
    Checks email address and confirms it is a valid address. 
    A valid email address follows the format: name@website.domain

    Args:
        (str) email - the user provided email address

    Returns:
        (str) valid_email - an approved email address matching the provided standard
    """
    if email_exists(email):
        print("\nThis user already exists. Please log into your already existing account...")
        mock_atm.LoginWizard()

    else:
        valid_email = re.search("^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", email)
        
        while valid_email == None:
            print("\nInvalid email format. Try again...")
            email = input("\nEmail address: ").lower()
            valid_email = re.search("^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", email)
        
        else:
            return email
