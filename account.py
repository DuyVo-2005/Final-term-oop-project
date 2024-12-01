from tkinter import messagebox

class Account:
    
    def __init__(self, accountType = "", accountName = "", balance = 0):
        self.__accountType = accountType
        self.__accountName = accountName
        self.__balance = balance
        self.__transactionList = []
        self.__loanList = []


    """Edit account information such as account type, account name and balance"""
    def Edit_Account(self, accountType, accountName, balance):
        self.__accountType = accountType
        self.__accountName = accountName
        try: 
            self.__balance = int(balance)
        except ValueError:
            messagebox.showerror("Notification","balance must be interger")
        
        
    """Make money transfers between internal accounts"""
    def Transfer(self, transferID, destinationAccount, amount, time):
        action = Transfer(transferID, self.__accountName, accountNameDestination, amount, time)        
        action.Make_Transfer(self.__accountName, destinationAccount, amount)
        
    
    """Create a new transaction"""
    def Create_Transaction(self, transactionID, transactionType, amount, time, note):
        for transaction in self.__transactionList:
            if transactionID == transaction.Get_ID():
                messagebox.showerror("Notification","This transaction id already exists!")
                return
        newTransaction = Transaction(transactionID, transactionType, amount, time, note)
        if transactionType == "Income":
            self.__balance += amount
        else:
            self.__balance -= amount
        self.__transactionList.append(newTransaction)
         
    
    """Delete transaction via transaction ID"""
    def Delete_Transaction(self, transactionID):
        if len(self.__transactionList) == 0:
            messagebox.showerror("Notification", "Transation list is empty! Can't delete!")
        elif transactionID not in self.__transactionList:
            messagebox.showerror("Notification", "Transaction id doesn't exist! Can't delete!")
        else:
            for transaction in self.__transactionList:
                if transactionID == transaction.Get_ID():
                    self.__transactionList.remove(transaction)
                    messagebox.showinfo("Notification","Delete Successfully!")
                    break
    
    
    """Delete transaction via transaction ID"""
    def Update_Transaction(self, transactionID):
        if len(self.__transactionList) == 0:
            messagebox.showerror("Notification", "Transation list is empty! Can't update!")
        elif transactionID not in self.__transactionList:
            messagebox.showerror("Notification", "Transaction id doesn't exist! Can't update!")
        else:
            for transaction in self.__transactionList:
                if transactionID == transaction.Get_ID():
                    transaction.Edit_Transaction(transactionType, amount, time, note, catalog)
                    messagebox.showinfo("Notification","Update Successfully!")
                    break
        
                
    """Get the current balance in the account"""    
    def Get_Balance(self):
        return self.__balance
    
     
    """View the history of transaction types (income/spending) made"""
    def Show_Transaction_History(self, dateTime):
        for transaction in self.__transactionList:
            if transaction.Get_Time() == dateTime:
                transaction.Get_Transaction_History()
    
    
    """Filter the list of catalogs"""
    def Classify_Catalog(self, newCatalog):
        for transaction in self.__transactionList:
            if newCatalog == transaction.Get_New_Catalog():
                print(transaction)
        
        
    # def Create_Loan(self, lenderName, amount, loanTime, dueTime, interestRate, note, paymentStatus):
    #     loan = Loan(lenderName, amount, loanTime, dueTime, interestRate, note, paymentStatus)
    #     self.loanList.append(loan)
        
    
    # def Delete_Loan(self, lenderName):
    #     for loan in self.loanList[:]:
    #         if loan.Get_Payment_Status() == 1 | lenderName == loan.Get_Lender_Name():
    #             self.loanList.remove(loan)
                
                
    # def Update_Loan(self, lenderName):
    #     for loan in self.loanList:
    #         if loan.Get_Lender_Name() == lenderName:
    #             loan.Edit_Loan()
                
            
