# Import relevant libraries and dependencies 
import time
import sys
import random
import re
import os
import validation
import database
from getpass import getpass

complaints = {}  # Empty dictionary to store user complaints
account_number = " "  # Initialize account_number variable for usage across functions


def AccountNumberGenerator():
    """
    Generates a unique 10-digit account number for each user. 
    As with the Nigerian banking system, every account number must begin with a '0'. 
    Every other account number generation rule/practice is ignored.

    Returns:
        (str) account_number - a valid account number that doesn't already exist in the database
    """
    
    first = '0'
    last = str(random.randrange(111111111, 999999999))
    account_number = (first+last)
    
    while validation.account_number_exists(account_number):
        AccountNumberGenerator()  # Run the program again if generated account number already exists
    
    else:
        print(f'\nYour new account number is: {account_number}')
        return account_number
    

def AccountCreationWizard():
    """
    Receives new user's desired username and password and append to the names and passwords lists. 
    Also assign a starting balance of NGN 0 to the user's balance. Does not allow new users use an already existing username. 
    """
    global account_number  # inherit and update the global variable user_database
    
    print('\nRain Account Creation Wizard!')
    first_name = input('\nFirst Name: ').capitalize()
    last_name = input('\nLast Name: ').capitalize()
    email = input('\nEmail Address: ').lower()

    if validation.email_exists(email):
        print("\nThis user already exists. Please login to your already existing account...")
        LoginWizard()

    else:
        approved_email = validation.EmailChecker(email)  # Confirm provided email address is of valid format
        print('')
        print('\n*****Note: Password should have at least 5 characters*****')
        password = getpass('\nPassword: ')
        approved_password = validation.PasswordChecker(password)  # Confirm password contains atleast 5 characters
        account_number = AccountNumberGenerator()
        
        if database.create_user(account_number, first_name, last_name, email, approved_password):
            print(f'\nAccount Setup complete...')
            LoginWizard()  # Launch the login portal once registration is successful

        else:
            print("Something went wrong. Please try again...")
            AccountCreationWizard()
    

def LoginWizard():
    """
    Requests for user's name and password and confirms match with existing database before proceeding to the transaction wizard.
    Exits the program if user attempts 5 incorrect password entries.
    """
    global account_number  # inherit and update the global variables name and user_database
    
    print('-----'*5)
    print('\nRain Account Login Portal')
    print('-----'*5)
    account_number = input('\nAccount Number: ')

    while not validation.account_number_exists(account_number):  # Immediately confirm validity of account number before proceeding
        print('\nAccount not found. Please enter a valid account number...')
        account_number = input('\nAccount Number: ')
    
    else:
        password = getpass('\nPassword: ')
        password_count = 1  # Track incorrect password attempts
        
        while not validation.password_match(account_number, password):
            print('\nIncorrect password. Try again...')
            print(f'\nYou have {5 - password_count} attempts remaining')
            password = getpass('\nPassword: ')
            password_count += 1
            if password_count == 5:
                sys.exit('\nToo many incorrect password attempts. Try again later...')
                
        else:
            localtime = time.asctime( time.localtime(time.time()) )
            print("\nLogin Successful!", localtime)
            print('----------'*5)
            TransactionWizard()


def logout():
    LoginWizard()


def name_and_balance(account_number):
    
    user_details = str.split(database.read_user(account_number), ",")
    account_balance = int(user_details[4])
    name = user_details[0]
    
    return name, account_balance


def withdrawal(balance):
    """
    Confirms the user wants to proceed with the withdrawal of said amount, 
    and then proceeds to verify user's balance is enough for such withdrawal.
    If withdrawal is possible within the existing balance, approve withdrawal and update the balance.
    Else, user is alerted if balance is insufficient and the transaction is terminated.
    """
    withdraw_amount = int(input("\nHow much would you like to withdraw? \n"))

    while True:
        confirm_withdraw = input(f'\nWithdraw {withdraw_amount}? [y/n] ').lower()
        
        if confirm_withdraw == 'y':
            if withdraw_amount <= balance:  # Confirm the withdrawal amount is less than the balance
                balance -= withdraw_amount
                database.update_user(account_number, 4, str(balance))
                print(f"\nWithdrawal Successful! Please take your cash.")
                break
            else:  # Cancel transaction if otherwise
                print('\nInsufficient balance...')
                break
        elif confirm_withdraw == 'n':  # Cancel withdrawal if user selects "n"
            print('\nWithdrawal canceled!')
            break
        else:
            print('\nInvalid selection...')
            continue  # Keep program running until a suitable response is provided 


def deposit(balance):
    """
    Receives as input the amount desired to be deposited by the user.
    Confirms the deposit amount, and adds same to the user's balance. 
    Terminate the transaction if the user' changes their mind.
    """
    deposit_amount = int(input("\nHow much would you like to deposit? \n"))
    
    while True:
        confirm_deposit = input(f'\nDeposit {deposit_amount}? [y/n] \n').lower()
        
        if confirm_deposit =='y':
            balance += deposit_amount
            database.update_user(account_number, 4, str(balance))
            print(f"\nTransaction Successful!")
            break
        elif confirm_deposit == 'n':
            print('\nDeposit canceled!')
            break
        else:
            print('\nInvalid selction...')
            continue  # Keep program running until a suitable answer is provided


def ChangePassword():
    """
    Receives new password as input from the user, confirms its validity, 
    and stores it in the user_database as a replacement for the existing password.
    """
    print('\n*****Note: Password should be at least 5 characters*****')
    password = getpass('\nEnter new password: ')
    approved_password = validation.PasswordChecker(password)  # Confirm validity of new password
    database.update_user(account_number, 3, approved_password)
    print('\nNew password set...')


def LodgeComplaint():
    complaint = input("\nWhat issue would you like to report? \n")
    complaints[account_number] = complaint
    print("\nThank you for contacting us. Your complaint will be reviewed immediately.")
        

def transfer(balance):
    """
    Requests the amount to be transferred and a valid 10-digit receiving account number that starts with '0'. 
    Asks the user to confirm the transfer, and checks to confirm transfer amount is within user's exisiting balance.
    Transfer is terminated if the amount excedes the user's balance or the user fails to confirm.
    
    Args:
        (int) balance - User's current balance
    """
    # Block users from transferring to the same account doing the transfer

    transfer_amount = int(input("\nEnter transfer amount: "))
    transfer_account = input("\nEnter receiving account number: ")
    
    # Confirm receiving account is a valid account type
    confirm_account = re.search("^0[0-9]{9}$", transfer_account)
    
    while confirm_account == None:
        print("\nInvalid account number...")
        transfer_account = input("\nEnter receiving account number: ")
        confirm_account = re.search("^0[0-9]{9}$", transfer_account)

    # Prompt user to confirm transfer details
    while True:
        confirm_transfer = input(f"\nTransfer {transfer_amount} to {transfer_account}? [y/n] ").lower()

        if confirm_transfer == 'y':
            if transfer_amount <= balance:  # Confirm transaction is possible within user's account balance
                balance -= transfer_amount
                database.update_user(account_number, 4, str(balance))
                print("\nTransfer Successful!")
                print(f"\nTransferred {transfer_amount} to {transfer_account}")
                break
            else:
                print("\nTransfer failed! You do not have enough money for this transfer...")
                break
        elif confirm_transfer == 'n':
            print("\nTransaction terminated!")
            break
        else:
            print("\nYou've entered an invalid command. Try again...")
            continue


def TransactionWizard():
    """
    Receive user's desired transaction as a number input and execute. 
    Possible transactions include withdrawal(1), deposits(2), balance checks(3), and dispute resolution(4).
    Withdrawal: Only permits the withdrawal of funds available in the user's balance; automatically updates balance.
    Deposit: Adds deposited amount to user's existing balance.
    Balance check: Prints out user's current balance.
    Dispute resolution: Receives user's complaint and sends to where it may be needed.
    """
   
    global account_number  # inherit and update (if needed) the global variables name and user_database
    first_name, balance = name_and_balance(account_number)
    
    # Receive action command from user
    print(f'\nWelcome {first_name}! What would you like to do today?')
    
    while True:
        try:  # Catch the error if someone enters a string instead of an integer value
            action = int(input("\nEnter: \n1 - Withdrawal \n2 - Deposit \n3 - Check Account Balance"
            "\n4 - Transfer \n5 - Dispute Resolution \n6 - Change Password \n0 - Logout \n"))
        except ValueError:
            print("Ooops!!! Expected a number, got a string. Try again later...")
            continue
        else:
            break

    if action not in range(0, 7):
        print('\nYou have selected an invalid option. Please try again...')
        TransactionWizard()
    
    if action == 0:
        logout()

    elif action == 1:
        # Receive amount to be withdrawn and subtract it from user's balance
        withdrawal(balance)
        
    elif action == 2:
        # Receive amount to deposit and add to user's previous balance 
        deposit(balance)
        
    elif action == 3:
        # Check user' balance
        print(f'\nAccount balance: NGN {balance}')
        
    elif action == 4:
        # Transfer funds to provided account if it is within user's balance
        transfer(balance)

    elif action == 5:
        # Record user complaint and exit
        LodgeComplaint()
        
    elif action == 6:
        # Receive new password entry and confirm it matches stated guidelines
        ChangePassword()


def main():
    """
    First determines if the user wishes to create an account (as a new user) or login (old user).
    Allows the user determine whether or not the program should keep running.
    """

    print('\nRain Bank')
    print('-----'*5)
    create_or_login = input('\nEnter 1 to create an account or 2 to login to an existing account: ')

    while create_or_login not in ['1', '2']:
        print('\nInvalid Selection. Try again...')
        create_or_login = input('\nEnter 1 to create an account or 2 to log  into existing account: ')

    if create_or_login == '1':
        AccountCreationWizard()
    elif create_or_login == '2':
        LoginWizard()
    
    another_transaction = input('\nWould you like to carry out another transaction? [y/n] ').lower()
        
    while another_transaction == 'y':
        TransactionWizard()
        another_transaction = input('\nWould you like to carry out another transaction? [y/n] ').lower()
    else:
        print("\nProgram shutdown initiated.... \nShutdown Complete!")
        print("--------"*10)


if __name__ == "__main__":
    main()