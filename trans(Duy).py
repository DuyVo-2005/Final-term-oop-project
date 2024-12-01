from tkinter import *
from tkinter import messagebox
import datetime
import random
#from account import *

catalog_hint = {
    1: "Food",
    2: "Moving",
    3: "Entertainment",
    4: "Salary",
    5: "Portfolio",
    6: "Other",
}
other_index = int(6)

class Trans():
    def __init__(self, amount: int, time: str) -> None:
        self.__ID = ""
        self.__amount = amount
        self.__time = time

    def Get_ID(self):
        return self.__ID

    def Set_ID(self, newID):
        self.__ID =  newID
    
    def Get_Amount(self):
        return self.__amount

    def Set_Amount(self, newAmount: int):
        self.__amount = newAmount

    def Get_Time(self):
        return self.__time

    def Set_Time(self, newTime: str):
        self.__time = newTime
    
    def __GetPresentTime(
) -> str:
        datetime_now = datetime.datetime.now()
        formatted_datetime = datetime_now.strftime("%Y-%m-%d")
        return formatted_datetime


class Transaction(Trans):
    def __init__(self, ID: int, amount: int, time: str, transactionType: str, catalog: str, note: str = "") -> None:
        super().__init__(ID, amount, time)
        self.__transactionType = transactionType
        self.__note = note
        self.__catalog = catalog

    def Get_Type(self):
        return self.__transactionType

    def Set_Type(self, newType: str = ""):
         self.__transactionType = newType

    def Get_Note(self):
        return self.__note

    def Set_Note(self, newNote: str = ""):
        self.__note = newNote

    def Get_Catalog(self):
        return self.__catalog

    def Set_Catalog(self, newCatalog: str):
        self.__catalog = newCatalog

    def Edit_Transaction(self, transactionType, amount, time, note, catalog) -> bool:
        """Function to edit existed transaction
        Parameters:
            transactionID(str): The id of transaction want to edit
            transactionType(str): The type of transaction want to edit (Income or Spending)
            amount(int): The amount of transaction want to edit
            time(datetime): The time of transaction want to edit
            note(str): The note of transaction want to edit
            catalog(str): The catalog of transaction want to edit
        Returns:
            None
        """
        if (
            transactionType.capitalize() != "Income"
            and transactionType.capitalize() != "Spending"
        ):
            messagebox.showerror(
                "Notification", "Transaction type must be Income or Spending!"
            )
            return False
        else:
            self.Set_Type(transactionType)

        try:
            if transactionType.capitalize() != "Income":
                self.Set_Amount(int(amount))
            else:
                #transaction type is spending
                self.Set_Amount(int((-1) * amount))
        except ValueError:
            messagebox.showerror("Notification", "amount must be integer")
            return False

        # true format for time: DD/MM/YYYY
        try:
            dateFormat = "%d/%m/%Y"
            self.Set_Time(datetime.datetime.strptime(time, dateFormat))
        except ValueError:
            messagebox.showerror(
                "Notification", "Date time must be in format DD/MM/YYYY!"
            )
            return False
        self.Set_Note(note)
        global catalog_hint
        if catalog.capitalize() not in catalog_hint.values():
            messagebox.showerror("Notification", "Error catalog input!")
            return False
        else:
            self.Set_Catalog(catalog)

    def __str__(self):
        return f"{self.__transactionID} | {self.__time} | {self.__transactionType} | {self.__amount} | {self.__note} | {self.__catalog}"

class Transfer(Trans):
    def __init__(self, TransactionID: int, amount: int, time: str, accountNameSource: str = "",accountNameDestination: str = "") -> None:
        super().__init__(ID, amount, time)
        self.__accounccountNameSource = accountNameSource
        self.__accountNameDestination = accountNameDestination
        
    def Get_Account_Name_Source(self):
        return self.__accounccountNameSource

    def Set_Aaccount_Name_Source(self, newAccountNameSource: str):
        self.__accounccountNameSource = newAccountNameSource

    def Get_Account_Name_Destination(self):
        return self.__accountNameDestination

    def Set_Account_Name_Destination(self, newAccountNameDestination: str):
        self.__accountNameDestination = newAccountNameDestinationt

    def Make_Transfer(self, sourceAccount: 'Account', destinationAccount: 'Account', amount: int) -> bool:
        """Function to make transfer from sourceAccount to destinationAccount with the amount of money is amount
        Parameters:
            sourceAccount (class): the source account class makes a money transfer
            destinationAccount (class): the destination account class receives a money transfer
            amount (int): the amount of money transfer
        Returns:
            bool
        """
        if sourceAccount.Get_Balnace() < amount:
            messagebox.showerror(
                "Notification", "You don't have enough money for transfer"
            )
            return False
        else:
            self.Set_ID(sourceAccount.__CreateID())
            self.__accountNameSource = sourceAccount.Get_Account_Name()
            self.__accountNameDestination = destinationAccount.Get_Account_Name()
            sourceAccount.Set_Balnace(sourceAccount.Get_Balnace() - amount)
            destinationAccount.Set_Balnace(destinationAccount.Get_Balnace() + amount)
            self.__amount = amount
            sourceAccount.Get_Transfer_List().append(self)
            destinationAccount.Get_Transfer_List().append(self)
        return True
    #def Edit_Transfer(self, sourceAccount: 'Account', destinationAccount: 'Account', amount: int) -> bool:
#        """Function to make transfer from sourceAccount to destinationAccount with the amount of money is amount
#        Parameters:
#            sourceAccount (class): the source account class makes a money transfer
#            destinationAccount (class): the destination account class receives a money transfer
#            amount (int): the amount of money transfer
#        Returns:
#            bool
#        """
#        if sourceAccount.Get_Balnace() < amount:
#            messagebox.showerror(
#                "Notification", "You don't have enough money for transfer"
#            )
#            return False
#        else:
#            self.Set_ID(sourceAccount.__CreateID())
#            self.__accountNameSource = sourceAccount.Get_Account_Name()
#            self.__accountNameDestination = destinationAccount.Get_Account_Name()
#            sourceAccount.Set_Balnace(sourceAccount.Get_Balnace() - amount)
#            destinationAccount.Set_Balnace(destinationAccount.Get_Balnace() + amount)
#            self.__amount = amount
#            sourceAccount.Get_Transfer_List().append(self)
#            destinationAccount.Get_Transfer_List().append(self)
#        return True