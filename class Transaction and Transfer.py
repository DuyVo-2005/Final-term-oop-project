from tkinter import *
from tkinter import messagebox
import datetime
import random

# transaction vs transfer


catalog_hint = {
    1: "Food",
    2: "Moving",
    3: "Entertainment",
    4: "Salary",
    5: "Portfolio",
    6: "Other",
}
other_index = int(6)


class Account:
    def __init__(self, balnace=0):
        self.__balnace = balnace
        self.__transactionList = []
        self.__transactionIDList = []
        self.__transferList = []
        self.__transferIDList = []

    def Get_Balnace(self):
        return self.__balnace

    def Get_Transaction_List(self):
        return self.__transactionList

    def Create_Transaction(self, transactionType, amount, time, note):
        """
        Function to create new transaction
        Parameters:
            self (self@Account): the class itself
            transactionType (str): The type of transaction want to create (Income or Spending)
            amount(int): The amount of transaction want to create
            time (datetime): The time of transaction want to create
            note (str): The note of transaction want to create
            note (catalog): The catalog of transaction want to create
        Returns:
            None
        """
        newTransaction = Transaction()
        temporaryID = random.randint(1, 10000000000)
        while temporaryID in self.__transactionIDList:
            temporaryID = random.randint(1, 10000000000)
        newTransaction.Set_ID(temporaryID)
        self.__transactionIDList.append(temporaryID)

        if (
            transactionType.capitalize() != "Income"
            and transactionType.capitalize() != "Spending"
        ):
            messagebox.showerror(
                "Notification", "Transaction type must be Income or Spending!"
            )
        else:
            newTransaction.Set_Type(transactionType.capitalize())

        try:
            int(amount)
            newTransaction.Set_Amount(int(amount))
        except ValueError:
            messagebox.showerror("Notification", "amount must be integer")

        # true format for time: DD/MM/YYYY
        dateFormat = "%Y/%m/%d %H:%M:%S"
        try:
            dateFormat = "%d/%m/%Y %H:%M:%S"
            newTime = datetime.datetime.strptime(time, dateFormat)
            newTransaction.Set_Time(newTime)
        except ValueError:
            messagebox.showerror(
                "Notification", "Date time must be in format DD/MM/YYYY HH:MM:SS!"
            )
        newTransaction.Set_Note(note)
        # Giao dien cai them dua tren console nay
        global catalog_hint
        print("Catalog hint")
        for key in catalog_hint.keys():
            print(f"{key}. {catalog_hint[key]}")
        try:
            choice = int(input("Enter your choice (corresponding number): "))
        except ValueError:
            messagebox.showerror("Notification", "Error catalog input!")
        else:
            global other_index
            if choice == other_index:
                newCatalog = input("Enter your new catalog name: ")
                newTransaction.Set_Catalog(newCatalog)
                catalog_hint.update({other_index: newCatalog})
                other_index += 1
                catalog_hint.update({other_index: "other"})
            elif choice < 1 or choice > other_index:
                messagebox.showerror("Notification", "Error catalog input!")
            else:
                newTransaction.Set_Catalog(catalog_hint[choice])
            self.Get_Transaction_List().append(newTransaction)

    def Delete_Transaction(self, transactionID):
        if len(self.__transactionList) == 0:
            messagebox.showerror(
                "Notification", "Transation list is empty! Can't delele!"
            )
        elif transactionID not in self.__transactionIDList:
            messagebox.showinfo(
                "Notification", "Transaction id doesn't exist! Can't delele!"
            )
        else:
            self.__transactionIDList.remove(transactionID)
            self.__transactionList = [
                transaction_
                for transaction_ in self.__transactionList
                if transaction_.Get_ID() != transactionID
            ]

    def Make_Transfer(self, sourceAccount, destinationAccount, amount):
        """Function to make transfer from sourceAccount to destinationAccount with the amount of money is amount
        Parameters:
            sourceAccount (class): the source account class makes a money transfer
            destinationAccount (class): the destination account class receives a money transfer
        Returns:
            None
        """
        if sourceAccount.balnace < amount:
            messagebox.showerror(
                "Notification", "You don't have enough money for transfer"
            )
        else:
            newTransfer = Transfer()
            newTransfer.transferID = random.randint(1, 10000000000)
            while newTransfer.transferID in self.transferIDList:
                newTransfer.transferID = random.randint(1, 10000000000)
            self.transferIDList.append(newTransfer.transferID)
            newTransfer.accountNameSource = sourceAccount.accountName
            newTransfer.accountNameDestination = destinationAccount.accountName
            sourceAccount.balnace -= amount
            destinationAccount.balnace += amount
            newTransfer.amount = amount
            self.transferList.append(newTransfer)

    def Classify_Transaction(self):
        """Function to classify catalog transaction
        Parameters:
            None
        Returns:
            None
        """
        temporaryTransactionList = sorted(
            self.transactionList.copy(),
            key=lambda transaction_class: transaction_class.catalog,
        )
        for transaction in temporaryTransactionList:
            print(transaction)


class Transaction:
    def __init__(
        self,
        TransactionID="",
        transactionType="",
        amount=0.0,
        time="",
        note="",
        catalog="",
    ):
        self.__transactionID = TransactionID
        self.__transactionType = transactionType
        self.__amount = amount
        self.__time = time
        self.__note = note
        self.__catalog = catalog

    def Get_ID(self):
        return self.__transactionID

    def Set_ID(self, newID):
        self.__transactionID = newID

    def Get_Type(self):
        return self.__transactionType

    def Set_Type(self, newType):
        self.__transactionType = newType

    def Get_Amount(self):
        return self.__amount

    def Set_Amount(self, newAmount):
        self.__amount = newAmount

    def Get_Time(self):
        return self.__time

    def Set_Time(self, newTime):
        self.__time = newTime

    def Get_Note(self):
        return self.__note

    def Set_Note(self, newNote):
        self.note = newNote

    def Get_Catalog(self):
        return self.__catalog

    def Set_Catalog(self, newCatalog):
        self.__catalog = newCatalog

    # def Edit_Transaction(self, transactionType, amount, time, note, catalog):
    #     """Function to edit existed transaction
    #     Parameters:
    #         transactionID(str): The id of transaction want to delete
    #         transactionType(str): The type of transaction want to create (Income or Spending)
    #         amount(float): The amount of transaction want to create
    #         time(datetime): The time of transaction want to create
    #         note(str): The note of transaction want to create
    #         catalog(str): The catalog of transaction want to create
    #     Returns:
    #         None
    #     """
    #     if (
    #         transactionType.capitalize() != "Income"
    #         or transactionType.capitalize() != "Spending"
    #     ):
    #         messagebox.showerror(
    #             "Notification", "Transaction type must be Income or Spending!"
    #         )
    #     else:
    #         self.transactionType = transactionType

    #     try:
    #         self.amount = float(amount)
    #     except ValueError:
    #         messagebox.showerror("Notification", "amount must be float")

    #     # true format for time: DD/MM/YYYY
    #     date_format = "%Y/%m/%d %H:%M:%S"
    #     try:
    #         date_format = "%d/%m/%Y %H:%M:%S"
    #         self.time = time
    #         dt = datetime.datetime.strptime(time, date_format)
    #     except ValueError:
    #         messagebox.showerror(
    #             "Notification", "Date time must be in format DD/MM/YYYY !"
    #         )
    #     self.note = note
    #     print("Catalog hint")
    #     for key in catalog_hint.keys():
    #         print(f"{key}. {catalog_hint[key]}")
    #     try:
    #         choice = int(input("Enter your choice (corresponding number): "))
    #     except ValueError:
    #         messagebox.showerror("Notification", "Error catalog input!")
    #     else:
    #         if catalog.capitalize() not in catalog_hint.values():
    #             messagebox.showerror("Notification", "Error catalog input!")
    #         else:
    #             self.catalog = catalog
    # if newTransaction.Get_Catalog().capitalize() not in catalog_hint.values():
    #     messagebox.showerror("Notification", "Error catalog input!")
    # else:
    #     newTransaction.Set_Catalog(catalog)
    # self.__transactionList.append(newTransaction)

    def GetTransactionHistory(TransactionID):
        """Function to get transaction history
        Parameters:
            AccountName (string): The name of account want to get transaction history
        Returns:
            List: array contains transaction history list
        """
        for Transaction_ in super().Transaction_List:
            if Transaction_.TransactionID == TransactionID:
                return Transaction_

    def __str__(self):
        return f"{self.__transactionID} | {self.__time} | {self.__transactionType} | {self.__amount} | {self.__catalog}"


# class transfer plays role such as a struct
class Transfer:

    def __init__(
        self,
        transferID="",
        accountNameSource="",
        accountNameDestination="",
        amount=0.0,
        time="",
    ):
        self.__transferID = transferID
        self.__accounccountNameSource = accountNameSource
        self.__accountNameDestination = accountNameDestination
        self.__amount = amount
        self.__time = time

    def Get_ID(self):
        return self.__transferID

    def Set_ID(self, newID):
        self.__transferID = newID

    def Get_Account_Name_Source(self):
        return self.__accounccountNameSource

    def Set_Aaccount_Name_Source(self, newAccountNameSource):
        self.__accounccountNameSource = newAccountNameSource

    def Get_Account_Name_Destination(self):
        return self.Get_Account_Name_Destination

    def Set_Account_Name_Destination(self, newAccountNameDestination):
        self.__accountNameDestination = newAccountNameDestination

    def Set_Amount(self):
        return self.__amount

    def Get_Amount(self, newAmount):
        self.__amount = newAmount

    def Get_Time(self):
        return self.__time

    def Set_Time(self, newTime):
        self.__time = newTime


newAccount = Account(100000)
# print(newAccount.Get_Balnace())
newAccount.Create_Transaction("Spending", 200000, "22/11/2011 11:12:13", "Hi")
newAccount.Create_Transaction("IncomE", 500000, "22/11/2011 11:12:13", "Hello")
# lst = newAccount.Get_Transaction_List()
# print(str(lst[0].Get_Time()))
for account in newAccount.Get_Transaction_List():
    print(account)
n = int(input())
newAccount.Delete_Transaction(n)
for account in newAccount.Get_Transaction_List():
    print(account)
