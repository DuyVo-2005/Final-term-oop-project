from tkinter import *
from tkinter import messagebox
import datetime
import random

TransferID_List = []

# transaction vs transfer

class User:
    def __init__(self):
        self.Transaction_List = []
    def Create_Transaction(self, TransactionID, Transaction_Type, Amount, Time, Note):
        # print("Tạo giao dịch mới")
        # self.TransactionID = input("Nhập mã giao dịch:")
        # self.transaction_type = input("Nhập loại giao dịch: ")
        # self.amount = int(input("Nhập số lượng: "))

        self.TransactionID = TransactionID

        if (
            Transaction_Type.capitalize() != "Income"
            or Transaction_Type.capitalize() != "Spending"
        ):
            messagebox.showerror(
                "Notification", "Transaction type must be Income or Spending!"
            )
        else:
            self.Transaction_Type = Transaction_Type

        try:
            self.Amount = float(Amount)
        except ValueError:
            messagebox.showerror("Notification", "Amount must be float")

        # true format for time: DD/MM/YYYY
        Date_Format = "%Y/%m/%d %H:%M:%S"
        try:
            Date_Format = "%d/%m/%Y %H:%M:%S"
            self.Time = Time
            dt = datetime.datetime.strptime(Time, Date_Format)
        except ValueError:
            messagebox.showerror(
                "Notification", "Date time must be in format DD/MM/YYYY !"
            )
        self.Note = Note
        
class Transaction(User):
    def __init__(
        self, TransactionID="", Transaction_Type="", Amount=0.0, Time="", Note=""
    ):
        super().__init__()
        self.TransactionID = TransactionID
        self.Transaction_Type = Transaction_Type
        self.Amount = Amount
        self.Time = Time
        self.Note = Note

    def Edit_Transaction(self, TransactionID, Transaction_Type, Amount, Time, Note):
        self.TransactionID = TransactionID

        if (
            Transaction_Type.capitalize() != "Income"
            or Transaction_Type.capitalize() != "Spending"
        ):
            messagebox.showerror(
                "Notification", "Transaction type must be Income or Spending!"
            )
        else:
            self.Transaction_Type = Transaction_Type

        try:
            self.Amount = float(Amount)
        except ValueError:
            messagebox.showerror("Notification", "Amount must be float")

        # true format for time: DD/MM/YYYY
        Date_Format = "%Y/%m/%d %H:%M:%S"
        try:
            Date_Format = "%d/%m/%Y %H:%M:%S"
            self.Time = Time
            dt = datetime.datetime.strptime(Time, Date_Format)
        except ValueError:
            messagebox.showerror(
                "Notification", "Date time must be in format DD/MM/YYYY !"
            )
        self.Note = Note

    def GetTransactionHistory(AccountName):
        """Function to get transaction history
        Parameters:
            AccountName (string): The name of account want to get transaction history
        Returns:
            List: array contains transaction history list     
        """        Transaction_History = []
        for Transaction_ in super().Transaction_List:
            if Transction_.TransactionID == TransactionID:
                    
ransaction_History.append(Transaction_)
#                print(f"Transaction ID: {Transaction_.TransactionID}")

#                print(f"Transaction Type: {Transaction_.Transaction_Type}")

#                print(f"Amount: {Transaction_.Amount}")

    def Transaction_Classification(self):
        pass

class Transfer:
    def __init__(self):
        self.TransferID = ""
        self.Account_Name_Source = ""
        self.Account_Name_Destination = ""
        self.Amount = 0.0
        self.Time = ""

    def Make_Transfer(Sour e_Account, Destination_Account):
        Temporary_TransferID = str(random.randint(1,10000000000))
        while Temporary_TransferID not in TransferID_List:
            self.TransferID = Temporary_TransferID
            TransferID_List.append(Temporary_TransferID)
            self.Account_Name_Source = Soure_Account.Account_Name
             self.Account_Name_Destination =    Destination_Account.Account_Name

        
