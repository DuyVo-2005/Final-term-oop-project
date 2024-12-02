from tkinter import messagebox
from trans import *
import random
import datetime

class Account:
    def __init__(self, balance: int, accountType: str = "", accountName: str = ""):
        self.__accountType = accountType
        self.__accountName = accountName
        self.__balance = balance
        self.__transactionList = []
        self.__transferList = []
        self.__DebtList = []


    def __CreateID(self) -> int:
        __listID = []
        for Trans in self.__transactionList:
            __listID.append(Trans.Get_ID())
        for Loans in self.__loanList:
            __listID.append(Loans.Get_ID())

        __thisTranID = random.randint(10_000_000, 99_999_999)
        while __thisTranID in __listID:
            __thisTranID = random.randint(10_000_000, 99_999_999)

        return __thisTranID
    
    def __GetPresentTime(self) -> str:
        pass

        
        
    """Edit account information such as account type, account name and balance"""
    def Edit_Account(self, balance: int, accountType: str, accountName: str):
        self.__accountType = accountType
        self.__accountName = accountName
        try: 
            self.__balance = int(balance)
        except ValueError:
            messagebox.showerror("Notification","Balance must be number")
        
        
        
    """Make money transfers between internal accounts"""
    def Create_Transfer(self, destinationAccount: str, amount: int, time: str = "DD/MM/YYYY HH:MM:SS"):
        if time == "DD/MM/YYYY HH:MM:SS":
            time = self.__GetPresentTime()
            
        newTransfer = Transfer(self.__CreateID(), self.__accountName, destinationAccount, amount, time)        
        newTransfer.Make_Transfer(self.__accountName, destinationAccount, amount)
        
        
    
    """Create a new transaction"""
    def Create_Transaction(self, transactionType: str, amount: int, time: str = "DD/MM/YYYY HH:MM:SS", note: str = ""):
        if time == "DD/MM/YYYY HH:MM:SS":
            time = self.__GetPresentTime()
        
        newTransaction = Transaction(self.__CreateID(), transactionType, amount, time, note)
        self.__balance += newTransaction.Get_Amount()
         
         
         
    """Create a new Debt"""
    def Create_Debt(self, debtType: str, amout: int, interestRate: float, status: bool, debtDate: str = "DD/MM/YYYY HH:MM:SS", dueDate: str = "DD/MM/YYYY HH:MM:SS"):
        if time == "DD/MM/YYYY HH:MM:SS":
            time = self.__GetPresentTime()
            
        newDebt = Debt(self.__CreateID(), debtType, amout, interestRate, status, debtDate, dueDate)
        
    
    
    """Delete via ID"""
    def Delete(self, ID: int) -> bool:
        for transaction in self.__transactionList:
            if transaction.Get_ID() == ID:
                self.__transactionList.remove(transaction)
                self.__balance += amount
                messagebox.showinfo("Notification","Delete Successfully!")
                return True
        
        for transfer in self.__transferList:
            if transfer.Get_ID() == ID:
                self.__transferList.remove(transfer)
                self.__balance += amount
                messagebox.showinfo("Notification","Delete Successfully!")
                return True
            
        for debt in self.__DebtList:
            if debt.Get_ID() == ID:
                self.__DebtList.remove(debt)
                self.__balance += amount
                messagebox.showinfo("Notification","Delete Successfully!")
                True
                
        return False
                
        
    
    """Update via ID"""
    def Update(self, ID: int) -> bool:
        for transaction in self.__transactionList:
            if transaction.Get_ID() == ID:
                transaction.Edit_Transaction(transactionType, amount, time, note, catalog)
                self.__balance += amount
                messagebox.showinfo("Notification","Update Successfully!")
                return True
            
        for transfer in self.__transferList:
            if transfer.Get_ID() == ID:
                transfer.Edit_Transfer("transactionType, amount, time, note, catalog")
                self.__balance += amount
                messagebox.showinfo("Notification","Update Successfully!")
                return True
        
        for transaction in self.__transactionList:
            if transaction.Get_ID() == ID:
                transaction.Edit_Debt("transactionType, amount, time, note, catalog")
                self.__balance += amount
                messagebox.showinfo("Notification","Update Successfully!")
                return True
        
        return False
                
                
                
    """Get the current balance in the account"""    
    def Get_Balance(self):
        return self.__balance
                 
    
    
    """Filter the list of catalogs"""
    def Classify_Catalog(self, newCatalog):
        for transaction in self.__transactionList:
            if newCatalog == transaction.Get_New_Catalog():
                print(transaction)
        
                
            
