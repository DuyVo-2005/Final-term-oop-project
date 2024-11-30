from tkinter import *
from tkinter import messagebox
import datetime


# transaction vs transfer
class Transaction:
    def __init__(
        self, TransactionID="", Transaction_Type="", Amount=0.0, Time="", Note=""
    ):
        self.TransactionID = TransactionID
        self.Transaction_Type = Transaction_Type
        self.Amount = Amount
        self.Time = Time
        self.Note = Note

    def create_transaction(self, TransactionID, Transaction_Type, Amount, Time, Note):
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

    def delete_transaction(self, TransactionID):
        # trong user
        pass

    def edit_transaction(self, TransactionID, transaction_type, amount, time, note):
        self.TransactionID = TransactionID
        self.transaction_type = transaction_type
        self.time = time
        self.note = note


class Transfer:
    def __init__(self):
        self.TransferID = ""
        self.Account_Name_Source = ""
        self.Account_Name_Destination = ""
        self.Amount = 0.0
        self.Time = ""

    def Make_Transfer(Destination):
        pass
