# using python 3.8
# Teller machine class task (Dec. 2019)
# "If all else fails think what would Kabir do."

# Work in progress ✘ ✔
# To-Do's: ✘ finalize data structure (key:values pairs); ✘ check if database exists on start-up; ✘ file op; bankers' functions; ✘ any new feature? 
# 

# fallback account (used only if database file not found)
root_db = {'admin':{'pin':'adminpass', 'type':'root'} }

# test data (will be replaced by file)
user_db = {'banker1':{'pin':'pass1', 'type':'banker'}, '001':{'pin':'1234','type':'client','is_active':'active','name':'Valued Customer','email':'vc@email.com','phone':'02555667','date joined':'2019-12-09','balance':50697.00}}


def prompt_user(string,task_list):
    print('\n'+string)
    for i in range(len(task_list)):
         print("{} : {}".format(i+1,task_list[i]))
    # print('─'*80)
    print('')
    return input()

def authentication():
    print('─'*10+'Authenticate'+'─'*10)
    user = input("Account No: ")
    passwd = input("PIN: ")

    if user in user_db.keys():
        if passwd == user_db[user]['pin']:
            listed = []
            listed.append(user)
            listed.append(user_db[user]['type'])
            return listed
        else:
            return [user, 'failed']
    else:
        return ['failed','failed']

def print_logout():
    print("You have been logged out. Thank you.\n\n")

def is_active(UID):
    if user_db[UID]['is_active'] == 'active':
        return True
    else:
        return False
    
def show_balance(UID):
    bal = user_db[UID]['balance']
    print("✔ Your current balance:",bal,"\n\n")
    # return

def withdrawal(UID):
    while True: 
        print("Enter amount for withdrawal (must be multiple of 500): ")
        cout = int(input())
        # minimum 500tk is kept for active service
        if user_db[UID]['balance'] - cout > 500:
            if cout%500 == 0:
                confirm = input("Cash out Tk {}?\nEnter 0 to continue, any other key to cancel\n".format(cout))
                if confirm == '0':
                    oldbal = user_db[UID]['balance']
                    print("✔ Your old balance was: ",oldbal)
                    newbal = oldbal - cout
                    user_db[UID]['balance'] = newbal
                    print("✔ Your new balance is: ",newbal)
                    print("\nDon't forget your withdrawn cash.")
                    print_logout()
                    break
                else:
                    print("\nCancelled. Your balance remains unchanged, Thank you!\n\n")
                    client(UID)
            else:
                print("✘ Amount must be multiple of 500.\nWe don't have smaller bank-notes, thank you.\n\n")
        else:
            print("✘ Insufficient balance! Please enter smaller amount, thank you.\n\n")



def client(UID):
    while True:    
        if is_active(UID) == True:
            selection = prompt_user("Please, select:",["Check Balance", "Cash out","Exit"])
            if selection == '1':
                show_balance(UID)
            elif selection == '2':
                withdrawal(UID)
                break
            elif selection == '3':
                print_logout()
                break
            else:
                print("✘ Wrong input!\n")
                client()
        else:
            print("✘ Account barred! Please contact support. ph. 02555121\n\n")

def cl_view():
    pass
def cl_add():
    pass
def cl_mod():
    pass
def recharge():
    pass
def cl_rm():
    pass

def banker(UID):
    while True:
        selection = prompt_user("Please, select task:",["View accounts", "Add account","Modify account", "Add balance", "Remove account","Log out"])
        if selection == '1':
            cl_view()
        elif selection == '2':
            cl_add()
        elif selection == '3':
            cl_mod()
        elif selection == '4':
            recharge()
        elif selection == '5':
            cl_rm()
        elif selection == '6':
            # return to main
            print_logout()
            break
        else:
            print("✘ Wrong input!\n\n")

def add_banker():
        username = input("Enter banker's username: ")
        passwd = input("Enter banker's password: ")
        return {username:{'pin':passwd,'type':'banker'} } 

            
            
def root(UID):
    # as a fallback 'root' only creates the missing database, that's all.
    print("The bank database is missing")
    while True:
        selection = prompt_user("# Select task:",["Create/add banker account","Log out"])
        if selection == '1':
            user_db.update(add_banker())
            # write(user_db)
        elif selection == '2':
            print_logout()
            break
        else:
            print("✘ Wrong input!\n\n")    
    
# authentication() returned list:[UID, type]         
def main():
    while True:
        try:
            status = authentication()
        
            if status[1] == 'banker':
                print("✔ Authenticated as a banker")
                banker(status[0])
            elif status[1] == 'client':
                print("✔ Authenticated as a client")
                client(status[0])
            elif status[1] == 'root':
                print("✔ Authenticated as root")
                root(status[0]) 
            elif status[1] == 'failed':
                print("✘ Authentication failed!\n\n")
            else:
                print("✘ Wrong data\n\n")
        except EOFError:
            break

if __name__ == '__main__':
    main()
