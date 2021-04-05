# Import relevant libraries and dependencies 
import time
import sys
import random
import re

# Launch user database with existing customer data
user_database = {
    '0705480437': ['Seyi', 'Onifade', 'seyioni@zuri.com', 'passSeyi', 100000], 
    '0688874292': ['Nonso', 'Obi', 'nonsobi@gmail.com', 'non1so', 80000]
    }

complaints = {} # Empty dictionary to store user complaints
account_number = " " # Initialize account_number variable for usage across functions
 
def passwordChecker(passkey):
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


def emailChecker(email):
    """
    Checks email address and confirms it is a valid address. 
    A valid email address follows the format: name@website.domain

    Args:
        (str) email - the user provided email address

    Returns:
        (str) valid_email - an approved email address matching the provided standard
    """
    valid_email = re.search("^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", email)
    
    while valid_email == None:
        print("\nInvalid email format. Try again...")
        email = input("\nEmail address: ")
        valid_email = re.search("^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", email)
    else:
        return valid_email


def accountNumberGenerator():
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
    while account_number in user_database.keys():
        accountNumberGenerator() # Run the program again if generated account number already exists
    else:
        print(f'\nYour new account number is: {account_number}')
        return account_number
    

def  accountCreationWizard():
    """
    Receives new user's desired username and password and append to the names and passwords lists. 
    Also assign a starting balance of NGN 0 to the user's balance. Does not allow new users use an already existing username. 
    """
    global user_database, account_number # inherit and update the global variable user_database
    
    print('\nRain Account Creation Wizard!')
    first_name = input('\nFirst Name: ').capitalize()
    last_name = input('\nLast Name: ').capitalize()
    email = input('\nEmail Address: ').lower()
    approved_email = emailChecker(email) # Confirm provided email address is of valid format
    print('')
    print('\n*****Note: Password should have at least 5 characters*****')
    password = input('\nPassword: ')
    approved_password = passwordChecker(password) # Confirm password contains atleast 5 characters
    account_number = accountNumberGenerator()
    starting_balance = 0
    user_database[account_number] = [first_name, last_name, approved_email, approved_password, starting_balance]
    print(f'\nAccount Setup complete...')
    loginWizard() # Launch the login portal once registration is successful
    
    
def loginWizard():
    """
    Requests for user's name and password and confirms match with existing database before proceeding to the transaction wizard.
    Exits the program if user attempts 5 incorrect password entries.
    """
    global account_number, user_database # inherit and update the global variables name and user_database
    
    print('-----'*5)
    print('\nRain Account Login Portal')
    print('-----'*5)
    account_number = input('\nAccount Number: ')
    while account_number not in user_database.keys(): # Immediately confirm validity of account number before proceeding
        print('\nAccount not found. Enter a valid account number')
        account_number = input('\nAccount Number: ')
    
    else:
        password = input('\nPassword: ')
        password_count = 1 #Track incorrect password attempts
        
        while password != user_database[account_number][3]:
            print('\nIncorrect password. Try again...')
            print(f'\nYou have {5 - password_count} attempts remaining')
            password = input('\nPassword: ')
            password_count += 1
            if password_count == 5:
                sys.exit('\nToo many incorrect password attempts. Try again later...')
                
        else:
            localtime = time.asctime( time.localtime(time.time()) )
            print("\nLogin Successful!", localtime)
            print('----------'*5)
            transactionWizard()


def withdrawal(withdraw_amount):
    """
    Confirms the user wants to proceed with the withdrawal of said amount, 
    and then proceeds to verify user's balance is enough for such withdrawal.
    If withdrawal is possible within the existing balance, approve withdrawal and update the balance.
    Else, user is alerted if balance is insufficient and the transaction is terminated.

    Args:
        (int) withdraw_amount - the amount the user wants to withdraw
    """
    confirm_withdraw = input(f'\nWithdraw {withdraw_amount}?[y/n]\n').lower()
    
    if confirm_withdraw == 'y':
        if withdraw_amount <= user_database[account_number][-1]: # Confirm the withdrawal amount is less than the balance
            user_database[account_number][-1] -= withdraw_amount
            print(f"\nWithdrawal Successful! Please take your cash.")
        else: # Cancel transaction if otherwise
            print('\nInsufficient balance...')
    elif confirm_withdraw == 'n': # Cancel withdrawal if user selects "n"
        print('\nWithdrawal canceled!')
    else:
        print('\nInvalid selection...')
        withdrawal(withdraw_amount) # Keep program running until a suitable response is provided 


def deposit(deposit_amount):
    """
    Receives as input the amount desired to be deposited by the user.
    Confirms the deposit amount, and adds same to the user's balance. 
    Terminate the transaction if the user' changes their mind.

    Args:
        (int) deposit_amount - the amount the user wishes to deposit
    """
    confirm_deposit = input(f'\nDeposit {deposit_amount}? [y/n] \n').lower()
    
    if confirm_deposit =='y':
        user_database[account_number][-1] -= deposit_amount
        print(f"\nTransaction Successful!")
    elif confirm_deposit == 'n':
        print('\nDeposit canceled!')
    else:
        print('\nInvalid selction...')
        deposit(deposit_amount) # Keep program running until a suitable answer is provided


def changePassword():
    """
    Receives new password as input from the user, confirms its validity, 
    and stores it in the user_database as a replacement for the existing password.
    """
    print('\n*****Note: Password should be at least 5 characters*****')
    password = input('\nEnter new password: ')
    approved_password = passwordChecker(password) # Confirm validity of new password
    print('\nNew password set...')
    user_database[account_number][3] = approved_password


def transactionWizard():
    """
    Receive user's desired transaction as a number input and execute. 
    Possible transactions include withdrawal(1), deposits(2), balance checks(3), and dispute resolution(4).
    Withdrawal: Only permits the withdrawal of funds available in the user's balance; automatically updates balance.
    Deposit: Adds deposited amount to user's existing balance.
    Balance check: Prints out user's current balance.
    Dispute resolution: Receives user's complaint and sends to where it may be needed.
    """
   
    global account_number, user_database  # inherit and update (if needed) the global variables name and user_database
    balance = user_database[account_number][-1]
    first_name = user_database[account_number][0]
    # Receive action command from user
    print(f'\nWelcome {first_name}! What would you like to do today?')
    
    try: # Catch the error if someone enters a string instead of an integer value
        action = int(input("\nEnter: \n1 - Withdrawal \n2 - Deposit \n3 - Check Account Balance \n4 - Dispute Resolution \n5 - Change Password \n"))
    except TypeError:
        print("Expected a number, got a string. Try again later...")

    while action not in range(1, 6):
        print('\nYou have selected an invalid option. Please try again...')
        action = int(input("\nEnter: \n1 - Withdrawal \n2 - Deposit \n3 - Balance Checker \n4 - Dispute Resolution \n5 - Change Password\n"))
    
    if action == 1:
        # Receive amount to be withdrawn and subtract it from user's balance
        withdraw_amount = int(input("\nHow much would you like to withdraw? \n"))
        withdrawal(withdraw_amount)
        
    elif action == 2:
        # Receive amount to deposit and add to user's previous balance 
        deposit_amount = int(input("\nHow much would you like to deposit? \n"))
        deposit(deposit_amount)
        
    elif action == 3:
        # Check user' balance
        print(f'\nAccount balance: NGN {balance}')
        
    elif action == 4:
        # Record user complaint and exit
        complaint = input("\nWhat issue would you like to report? \n")
        complaints[account_number] = complaint
        print("\nThank you for contacting us. Your complaint will be reviewed immediately.")
        
    elif action == 5:
        # Receive new password entry and confirm it matches stated guidelines
        changePassword()
    

def main():
    """
    First determines if the user wishes to create an account (as a new user) or login (old user).
    Allows the user determine whether or not the program should keep running.
    """

    while True:
        print('\nRain Bank')
        print('-----'*5)
        create_or_login = input('\nEnter 1 to create an account or 2 to log  into existing account: ')

        while create_or_login not in ['1', '2']:
            print('\nInvalid Selection. Try again...')
            create_or_login = input('\nEnter 1 to create an account or 2 to log  into existing account: ')

        if create_or_login == '1':
            accountCreationWizard()
        elif create_or_login == '2':
            loginWizard()
        
        repeat_program = input('\nWould you like to carry out another transaction? [y/n] ').lower()
        
        if repeat_program != 'y':
            print("\nProgram shutdown initiated.... \nShutdown Complete!")
            print("--------"*10)
            break


if __name__ == "__main__":
    main()