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


    def Get_Acount_Name(self) -> str:
        return self.__accountName
    
    
    def Get_Acount_Type(self) -> str:
        return self.__accountType
    
    
    def Get_Balance(self) -> int:
        return self.__balance
    

    def Get_Transaction_List(self):
        return self.__transactionList
    
    
    def Get_Transfer_List(self):
        return self.__transferList
        
        
    """Edit account information such as account type, account name and balance"""
    def Edit_Account(self, balance: int, accountType: str, accountName: str):
        self.__accountType = accountType
        self.__accountName = accountName
        try: 
            self.__balance = int(balance)
        except ValueError:
            messagebox.showerror("Notification","Balance must be number")
        
        
        
    """Make money transfers between internal accounts"""
    def Create_Transfer(self, destinationAccount: str, amount: int, ID: int = 0, time: str = "DD/MM/YYYY"):
        if time == "DD/MM/YYYY":
            time = GetPresentTime()
        
        if ID == 0:
            newTransfer = Transfer(self.__CreateID(), self.__accountName, destinationAccount, amount, time)  
        else:
            newTransfer = Transfer(ID, self.__accountName, destinationAccount, amount, time)   
            
        newTransfer.Make_Transfer(self.__accountName, destinationAccount, amount)
        self.__balance += newTransfer.Get_Amount()
        
        
    
    """Create a new transaction"""
    def Create_Transaction(self, transactionType: str, amount: int, ID: int = 0, time: str = "DD/MM/YYYY", note: str = ""):
        if time == "DD/MM/YYYY":
            time = GetPresentTime()
            
        if ID == 0:
            newTransaction = Transaction(self.__CreateID(), transactionType, amount, time, note)
        else:
            newTransaction = Transaction(ID, transactionType, amount, time, note)
        
        self.__balance += newTransaction.Get_Amount()
         
         
         
    # """Create a new Debt"""
    # def Create_Debt(self, debtType: str, amout: int, interestRate: float, status: bool, ID: int = 0, debtDate: str = "DD/MM/YYYY", dueDate: str = "DD/MM/YYYY"):
    #     if time == "DD/MM/YYYY":
    #         time = GetPresentTime()
        
    #     if ID == 0:
    #         newDebt = Debt(self.__CreateID(), debtType, amout, interestRate, status, debtDate, dueDate)
    #     else:
    #         newDebt = Debt(ID, debtType, amout, interestRate, status, debtDate, dueDate)
            
    #     self.__balance += newDebt.Get_Amount()
        
    
    
    """Delete via ID"""
    def Delete(self, ID: int) -> bool:
        for transaction in self.__transactionList:
            if transaction.Get_ID() == ID:
                self.__transactionList.remove(transaction)
                self.__balance += transaction.Get_Amount()
                messagebox.showinfo("Notification","Delete Successfully!")
                return True
        
        for transfer in self.__transferList:
            if transfer.Get_ID() == ID:
                self.__transferList.remove(transfer)
                self.__balance += transfer.Get_Amount()
                messagebox.showinfo("Notification","Delete Successfully!")
                return True
            
        # for debt in self.__DebtList:
        #     if debt.Get_ID() == ID:
        #         self.__DebtList.remove(debt)
        #         self.__balance += debt.Get_Amount()
        #         messagebox.showinfo("Notification","Delete Successfully!")
        #         True
                
        return False
                
        
    
    """Update via ID"""
    def Update(self, ID: int) -> bool:
        for transaction in self.__transactionList:
            if transaction.Get_ID() == ID:
                transaction.Edit_Transaction(transactionType, amount, time, note, catalog)
                self.__balance += transaction.Get_Amount()
                messagebox.showinfo("Notification","Update Successfully!")
                return True
            
        for transfer in self.__transferList:
            if transfer.Get_ID() == ID:
                transfer.Edit_Transfer("transactionType, amount, time, note, catalog")
                self.__balance += transfer.Get_Amount()
                messagebox.showinfo("Notification","Update Successfully!")
                return True
        
        # for debt in self.__debtList:
        #     if debt.Get_ID() == ID:
        #         debt.Edit_Debt("transactionType, amount, time, note, catalog")
        #         self.__balance += debt.Get_Amount()
        #         messagebox.showinfo("Notification","Update Successfully!")
        #         return True
        
        return False
                
                
                
    """Get the current balance in the account"""    
    def Get_Balance(self):
        return self.__balance

