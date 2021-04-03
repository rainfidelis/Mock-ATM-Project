# Import relevant libraries and dependencies 
import time
import sys

# Launch user database with existing customer data
user_database = {
    'Rain': ['passRain', 1000000], 
    'Femi': ['passFemi', 500000], 
    'Nonso': ['passNonso', 450000], 
    'Seyi': ['passSeyi', 80000]
    }

name = " " # Initialize global name variable for usage across functions
 
def PasswordChecker(passkey):
    """
    Confirms validity of newly created password. 
    Only passwords with at least 5 characters are accepted. 
    To improve password difficulty, code could be extended to accept only passwords with minimum 5 characters,
    and at least 1 uppercase letter.
    """
    global user_database, name
    while len(passkey) < 5:
        print('\nNote: Password should have at least 5 characters')
        passkey = input('\nEnter password: ')
    if len(passkey) >= 5:
        user_database[name][0] = passkey
        print('\nNew password set...')
 
 
def  AccountCreationWizard():
    """
    Receives new user's desired username and password and append to the names and passwords lists. 
    Also assign a starting balance of NGN 0 to the user's balance. Does not allow new users use an already existing username. 
    """
    global user_database, name # inherit and update the global variable user_database
    
    print('\nRain Account Creation Wizard!')
    name = input('\nName: ').capitalize()
    while name in user_database.keys(): # Check if name already exists.
        print('\nThis username already exists. Try again...')
        name = input('\nName: ').capitalize()
    if name not in user_database.keys():
        print(f'\nUsername stored as "{name}"')
        user_database[name] = ['', 0] # Initialize new database slot for variable 'name' with placeholder password and balance
        print('\nNote: Password should have at least 5 characters')
        password = input('\nPassword: ')
        PasswordChecker(password)
        print(f'\nAccount Setup complete...')
        print('----------'*5)
    
    
def LoginWizard():
    """
    Requests for user's name and password and confirms match with existing database before proceeding to the transaction wizard.
    Exits the program if user attempts 5 incorrect password entries.
    """
    global name, user_database # inherit and update the global variables name and user_database
    
    print('-----'*5)
    print('\nRain Account Login Portal')
    print('-----'*5)
    name = input('\nName: ').capitalize()
    while name not in user_database.keys():
        print('\nThe name you entered does not exist.')
        name = input('\nEnter name to login: ').capitalize()
    
    if name in user_database.keys():
        password = input('\nPassword: ')
        password_count = 1 #Track incorrect password attempts
        
        while password != user_database[name][0]:
            print('\nThe password you entered does not match. Try again...')
            print(f'You have {5 - password_count} attempts remaining')
            password = input('\nPassword: ')
            password_count += 1
            if password_count == 5:
                sys.exit('\nToo many incorrect password attempts. Try again later...')
                
        if password == user_database[name][0]:
            localtime = time.asctime( time.localtime(time.time()) )
            print ("\nLogin Successful!", localtime)
            print('----------'*5)
       
 
def TransactionWizard():
    """
    Receive user's desired transaction as a number input and execute. 
    Possible transactions include withdrawal(1), deposits(2), balance checks(3), and dispute resolution(4).
    Withdrawal: Only permits the withdrawal of funds available in the user's balance; automatically updates balance.
    Deposit: Adds deposited amount to user's existing balance.
    Balance check: Prints out user's current balance.
    Dispute resolution: Receives user's complaint and sends to where it may be needed.
    """
   
    global name, user_database  # inherit and update (if needed) the global variables name and user_database
    balance = user_database[name][1]
    # Receive action command from user
    print(f'\nWelcome {name}! What would you like to do today?')
    
    action = int(input("\nEnter: \n1 - Withdrawal \n2 - Deposit \n3 - Check Account Balance \n4 - Dispute Resolution \n5 - Change Password \n"))
    
    while action not in range(1, 6):
        print('\nYou have selected an invalid option. Please try again...')
        action = int(input("\nEnter: \n1 - Withdrawal \n2 - Deposit \n3 - Balance Checker \n4 - Dispute Resolution \n"))
    
    if action == 1:
        # Receive amount to be withdrawn and subtract it from user's balance
        withdraw_amount = int(input("\nHow much would you like to withdraw? \n"))
        confirm_withdraw = input(f'\nWithdraw {withdraw_amount}?[y/n]\n').lower()
        
        while confirm_withdraw not in ['y', 'n']:
            print('\nInvalid selection...')
            confirm_withdraw = input(f'\nWithdraw {withdraw_amount}? [y/n] \n').lower()
        
        if confirm_withdraw == 'y':
            if withdraw_amount <= balance: # Confirm the withdrawal amount is less than the balance
                user_database[name][1] = balance - withdraw_amount
                print(f"\nWithdrawal Successful! Please take your cash.")
            else: # Cancel transaction if otherwise
                print('\nInsufficient balance...')
        else: # Cancel withdrawal if user selects "n"
            print('\nWithdrawal canceled!')
    
    elif action == 2:
        # Receice amount to deposit and add to user's previous balance 
        deposit = int(input("\nHow much would you like to deposit? \n"))
        confirm_deposit = input(f'\Deposit {deposit}? [y/n] \n').lower()
        
        while confirm_deposit not in ['y', 'n']:
            print('\nInvalid selction...')
            confirm_deposit = input(f'\nDeposit {deposit}? [y/n] \n').lower()
        
        if confirm_deposit =='y':
            user_database[name][1] = balance + deposit
            print(f"\nTransaction Successful!")
        else:
            print('\nDeposit canceled!')
        
    elif action == 3:
        # Check user' balance
        print(f'\nAccount balance: NGN {balance}')
        
    elif action == 4:
        # Record user complaint and exit
        complaint = input("\nWhat issue would you like to report? \n")
        print("\nThank you for contacting us. Your complaint will be reviewed immediately.")
        
    elif action == 5:
        # Receive new password and store it in the user_database
        print('\nNote: Password should be at least 5 characters')
        password = input('\nEnter new password: ')
        PasswordChecker(password)
    
    else:
        print('\nInvalid Selection...')
 

def program():
    """
    Determine if user first wants to create an account. 
    If yes, create account and store new details before running the login and transaction wizards.
    Otherwise, immediately run the login and transaction wizards for an existing account holder.
    """
    print('\nRain Bank')
    print('-----'*5)
    create_or_login = input('\nEnter 1 to create an account or 2 to log  into existing account: ')

    while create_or_login not in ['1', '2']:
        print('\nInvalid Selection. Try again...')
        create_or_login = input('\nEnter 1 to create an account or 2 to log  into existing account: ')

    if create_or_login == '1':
        AccountCreationWizard()
        LoginWizard()
        TransactionWizard()
    elif create_or_login == '2':
        LoginWizard()
        TransactionWizard()
    

def main():
    """
    Keeps the program running until the user decides otherwise. Allows user decide whether or not they want to perform another transaction.
    """
    response = 'y'
    while response == 'y':
        program()
        response = input('\nWould you like to carry out another transaction? [y/n] ').lower()
        
        if response == 'n':
            print("\nProgram shutdown initiated.... \nShutdown Complete!")
            print("--------"*10)
            
        while response not in ['y', 'n']:
            print('\nInvalid selection...')
            response = input('\nWould you like to carry out another transaction? [y/n] ')

main()