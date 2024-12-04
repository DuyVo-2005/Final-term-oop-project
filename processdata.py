import pandas as pd
from trans import *
from account import *
from user import *

AccountListPath = "data\\AccountList.txt"
TransactionDataPath = "data\\TransactionData.csv"
TransferDataPath = "data\\TransferData.csv"
DebtListPath = "data\\DebtList.txt"
DebtPaymentDataPath = "data\\DebtPaymentData.csv"

def readData() -> User:
    user = User()

    # Xử Lý Các Account
    accountlist = open(AccountListPath, 'r', encoding='utf-8').readlines()
    for row in accountlist:
        account_name = row.split("|")[1].strip().lower()
        user.Add_Account(Account(balance=int(row.split("|")[2]), 
                                    accountType=row.split("|")[0].strip().lower(),
                                    accountName=account_name))
    

    # Xử Lý Các Transaction của các Account
    data = pd.read_csv(TransactionDataPath, header=0, encoding='utf-8')
    list_account = user.Get_Account_List()
    for row in data.itertuples():
        account_name = row._1.strip().lower()
        for account in list_account:
            if account.Get_Account_Name() == account_name:
                user.Get_Account_By_Name(account_name).Create_Transaction(ID=row[2],
                                                                        cataLog=str(row[6]).split("|")[0],
                                                                        fluctuation=str(row[3]).strip().lower(),
                                                                        amount=int(row[5]),
                                                                        time=str(row[4]),
                                                                        note=str(row[6]).split("|")[1])
    

    # Xử lý các Transfer của User
    data = pd.read_csv(TransferDataPath, header=0, encoding='utf-8')
    for row in data.itertuples():
        sourceAccName = str(row[3]).strip()
        desAccName = str(row[4]).strip()
        id = int(row[1])
        amount = int(row[2])
        time = str(row[5])
        note = str(row[6])
        user.Create_Transfer(ID=id,
                           amount=amount, 
                           sourceAccountName=sourceAccName,
                           desAccountName=desAccName,
                           time=time,
                           note=note)


    # Xử lý các Debt của User
    data = open(DebtListPath, 'r', encoding='utf-8').readlines()
    for row in data:
        # ID|fluctuation|amount|interestRate|dueDate|time|note
        user.Create_Debt(ID= int(row.split("|")[0]),
                       fluctuation= row.split("|")[1].strip().lower(), 
                       amount= int(row.split("|")[2]), 
                       dueDate= row.split("|")[4].strip(), 
                       interestRate= float(row.split("|")[3]), 
                       time= row.split("|")[5].strip(),  
                       note= row.split("|")[6].strip())

    # Xử lý thông tin các debt
    data = pd.read_csv(DebtPaymentDataPath, header=0, encoding='utf-8')
    for row in data.itertuples():
        id = int(row[1])
        amount = int(row[2])
        payDate = str(row[3]).strip()

        user.Get_Debt_By_ID(ID=id).Add_Payment(amount=amount, paymentDate=payDate)
        
    return user

            
def writeData(user: User):

    # Xử lý các Account và các Transaction của các Account
    columns = ['Account Name', 'ID', 'Fluctuation', 'Time', 'Amount', 'Transaction Attribute']
    data = pd.DataFrame(columns=columns)
    data.to_csv(TransactionDataPath, mode='w', index=False, encoding='utf-8')
    accountlist = open(AccountListPath, 'w', encoding='utf-8')
    for account in user.Get_Account_List():
        accountlist.write(f"{account.Get_Acount_Type().strip().lower()}|{account.Get_Account_Name().strip().lower()}|{account.Get_Init_Balance()}\n")
        Account_Name = [f"{account.Get_Account_Name()}"] * len(account.Get_Transaction_List())
        tID = []
        Fluctuation = []
        Time = []
        Amount = []
        Transaction_Attribute = []

        for transaction in account.Get_Transaction_List():
            tID.append(int(transaction.Get_ID()))
            Fluctuation.append(transaction.Get_Fluctuation().strip().lower())
            Time.append(transaction.Get_Time().strip())
            Amount.append(int(transaction.Get_Amount()))
            Transaction_Attribute.append(f"{transaction.Get_Catalog().strip()}|{transaction.Get_Note().strip()}")

        data = pd.DataFrame({
            'Account Name': Account_Name,
            'ID': tID,
            'Fluctuation': Fluctuation,
            'Time': Time,
            'Amount': Amount,
            'Transaction Attribute': Transaction_Attribute
        })
        data.to_csv(TransactionDataPath, mode='a', index=False, header=False, encoding='utf-8')


    # Xử lý các Transfer của User
    columns = ['ID', 'Amount', 'SourceAccountName', 'DesAccountName', 'Time', 'Note']
    data = pd.DataFrame(columns=columns)
    data.to_csv(TransferDataPath, mode='w', index=False, encoding='utf-8')
    tid = []
    Amount = []
    SourceAccountName = []
    DesAccountName = []
    Time = []
    Note = []
    for transfer in user.Get_Transfer_List():
        tid.append(int(transfer.Get_ID()))
        Amount.append(int(transfer.Get_Amount()))
        SourceAccountName.append(transfer.Get_Source_Account().Get_Account_Name().strip().lower())
        DesAccountName.append(transfer.Get_Des_Account().Get_Account_Name().strip().lower())
        Time.append(transfer.Get_Time().strip())
        Note.append(transfer.Get_Note().strip())

    data = pd.DataFrame({
        'ID': tid,
        'Amount': Amount,
        'SourceAccountName': SourceAccountName,
        'DesAccountName': DesAccountName,
        'Time': Time,
        'Note': Note
    })
    data.to_csv(TransferDataPath, mode='a', index=False, header=False, encoding='utf-8')

    # Xử lý Debt
    columns = ['ID', 'Amount', 'PaymentDate']
    data = pd.DataFrame(columns=columns)
    data.to_csv(DebtPaymentDataPath, mode='w', index=False, encoding='utf-8')
    debtlist = open(DebtListPath, 'w', encoding='utf-8')
    for debt in user.Get_Debt_List():
        # ID|fluctuation|amount|interestRate|dueDate|time|note
        debtlist.write(f"{debt.Get_ID()}|{debt.Get_Fluctuation()}|{debt.Get_Amount()}|{float(debt.Get_InterestRate())}|{debt.Get_DueDate()}|{debt.Get_Time()}|{debt.Get_Note()}\n")

        tid = []
        amount = []
        paymentDate = []
        for payment in debt.Get_PaymentHistory():
            tid.append(debt.Get_ID())
            amount.append(payment['amount'])
            paymentDate.append(payment['date'])

        data = pd.DataFrame({
            'ID': tid,
            'Amount': amount,
            'PaymentDate': paymentDate
        })
        data.to_csv(DebtPaymentDataPath, mode='a', index=False, header=False, encoding='utf-8')
