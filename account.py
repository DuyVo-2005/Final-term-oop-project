import random

class Account():
    def __init__(self, accountType: str, accountName: str, balance: int = 0) -> None:
        self.__initBalance = balance
        self.__accountType = accountType
        self.__accountName = accountName
        self.__balance = balance
        self.__transactionList = []

    def Get_Account_Name(self) -> str:
        return self.__accountName
    
    def Get_Transaction_List(self) -> list:
        return self.__transactionList
           
    def Get_Balance(self) -> int:
        return self.__balance
    
    def Get_Acount_Type(self) -> str:
        return self.__accountType
    
    def Get_Init_Balance(self) -> int:
        return self.__initBalance
    
    def Set_Account_Name(self, newAccountName: str):
        self.__accountName = newAccountName
    
    def Set_Account_Type(self, newAccountType: str):
        self.__accountType = newAccountType
    
    def Set_Balance(self, newBalance: int, isTrans: bool):
        if not isTrans:
            t = newBalance - self.__balance
            self.__initBalance = self.__balance + t
        self.__balance = newBalance

    def __CreateID(self) -> int:
        __listID = []
        for Trans in self.__transactionList:
            __listID.append(Trans.Get_ID())

        __thisTranID = random.randint(10_000_000, 99_999_999)
        while __thisTranID in __listID:
            __thisTranID = random.randint(10_000_000, 99_999_999)

        return __thisTranID
    
    def Get_Transaction_By_ID(self, ID: int):
        for trans in self.__transactionList:
            if trans.Get_ID() == ID:
                return trans
            
        return None        
    
    def Create_Transaction(self, cataLog: str, fluctuation: str, amount: int, time: str = "YYYY-MM-DD", note: str = "", ID: int =0) -> bool:
        if amount > 0:
            # Import trans chỉ khi cần thiết
            import trans
            newTransaction = trans.Transaction(ID=self.__CreateID() if ID == 0 else ID, amount=amount, cataLog=cataLog, fluctuation=fluctuation, note=note, time=time)
            if fluctuation == "spend":
                self.__balance -= amount
            else:
                self.__balance += amount

            self.__transactionList.append(newTransaction)
            return True
        return False

    def Delete_Transaction(self, ID: int) -> bool:
        trans = self.Get_Transaction_By_ID(ID)
        if trans:
            if trans.Get_Fluctuation() == "spend":
                self.__balance += trans.Get_Amount()
            else:
                self.__balance -= trans.Get_Amount()
            
            self.__transactionList.remove(trans)
            return True
        
        return False

    def Edit_Transaction(self, ID: int, cataLog: str, fluctuation: str, amount: int, time: str = "YYYY-MM-DD", note: str = "") -> bool:
        if self.Delete_Transaction(ID):
            # Import trans chỉ khi cần thiết
            import trans
            newTransaction = trans.Transaction(ID=ID, amount=amount, cataLog=cataLog, fluctuation=fluctuation, note=note, time=time)
            if fluctuation == "spend":
                self.__balance -= amount
            else:
                self.__balance += amount

            self.__transactionList.append(newTransaction)
            return True
        return False
