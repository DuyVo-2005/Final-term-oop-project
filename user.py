from account import Account
from trans import Transfer, Debt
import random
from GetPresentTime import GetPresentTime

class User:
    def __init__(self) -> None:
        self.__accountsList = []
        self.__transferList = []
        self.__debtList = []
        

    def __CreateID(self) -> int:
        __listID = []
        for Trans in self.__transferList:
            __listID.append(Trans.Get_ID())
        for Debt in self.__debtList:
            __listID.append(Debt.Get_ID())
            

        __thisTranID = random.randint(100_000, 999_999)
        while __thisTranID in __listID:
            __thisTranID = random.randint(100_000, 999_999)

        return __thisTranID

    def Get_Account_List(self) -> list:
        return self.__accountsList
    
    def Get_Transfer_List(self) -> list:
        return self.__transferList
    
    def Get_Debt_List(self) -> list:
        return self.__debtList
    
    def Get_Account_By_Name(self, accountName: str) -> Account:
        for account in self.__accountsList:
            if account.Get_Account_Name() == accountName:
                return account
        return None
    
    def Get_Transfer_By_ID(self, ID: int) -> Transfer:
        for trans in self.__transferList:
            if trans.Get_ID() == ID:
                return trans    
        return None   
    
    def Get_Debt_By_ID(self, ID: int) -> Debt:
        for debt in self.__debtList:
            if debt.Get_ID() == ID:
                return debt
        return None
    
    def Get_Total_Balance(self) -> int:
        totalBalance = 0
        for total in self.__accountsList:
            totalBalance += total.Get_Balance()
        return totalBalance

    def Add_Account(self, account: Account):
        self.__accountsList.append(account)
        
    def Delete_Account(self, accountName: str) -> bool:
        account = self.Get_Account_By_Name(accountName)
        if account:
            idList = []
            for trans in self.__transferList:
                source = trans.Get_Source_Account().Get_Account_Name()
                des = trans.Get_Des_Account().Get_Account_Name()
                
                if accountName == source or accountName == des:
                    idList.append(trans.Get_ID())
                    
            for id in idList:
                self.Delete_Transfer(id)
            self.__accountsList.remove(account)
            return True
        return False
        
    def Edit_Account(self, accountName: str, newAccountType: str, newAccountName: str, newBalance: int) -> bool:
        if self.Get_Account_By_Name(accountName):
            account = Account(accountType=newAccountType, accountName=newAccountName, balance=newBalance)
            self.__accountsList.append(account)
            return True
        return False

    def Create_Transfer(self, amount: int, sourceAccountName: str, desAccountName: str, time: str = "YYYY-MM-DD", note: str = ""):
        sourceAccount = self.Get_Account_By_Name(sourceAccountName)
        desAccount = self.Get_Account_By_Name(desAccountName)

        newTransfer = Transfer(ID=self.__CreateID(), amount=amount, sourceAccount=sourceAccount, desAccount=desAccount, note=note, time=time)
        sourceAccount.Set_Balance(sourceAccount.Get_Balance() - amount, True)
        desAccount.Set_Balance(desAccount.Get_Balance() + amount, True)
        self.__transferList.append(newTransfer)

    def Delete_Transfer(self, ID: int) -> bool:
        trans = self.Get_Transfer_By_ID(ID)
        if trans:
            sourceAccount = trans.Get_Source_Account()
            desAccount = trans.Get_Des_Account()
            
            amount = trans.Get_Amount()
            sourceAccount.Set_Balance(sourceAccount.Get_Balance() + amount, True)
            desAccount.Set_Balance(desAccount.Get_Balance() - amount, True)
            self.__transferList.remove(trans)
            return True
        return False

    def Edit_Transfer(self, ID: int, amount: int, sourceAccountName: str, desAccountName: str, time: str = "YYYY-MM-DD", note: str = "") -> bool:
        if self.Delete_Transfer(ID):
            sourceAccount = self.Get_Account_By_Name(sourceAccountName)
            desAccount = self.Get_Account_By_Name(desAccountName)
            newTransfer = Transfer(ID=ID, amount=amount, sourceAccount=sourceAccount, desAccount=desAccount, note=note, time=time)

            sourceAccount.Set_Balance(sourceAccount.Get_Balance() - amount, True)
            desAccount.Set_Balance(desAccount.Get_Balance() + amount, True)
            self.__transferList.append(newTransfer)
            return True
        return False
    
    def Create_Debt(self, fluctuation: str, amount: int, dueDate: str, interestRate: float = 0.0, time: str = "YYYY-MM-DD",  note: str = ""):
        newDebt = Debt(ID=self.__CreateID(), fluctuation=fluctuation, amount=amount, interestRate=interestRate, time=time, dueDate=dueDate, note=note)
        self.__debtList.append(newDebt)
        
    def Update_Debt(self, ID: int, amount: int, paymentDate: str = "YYYY-MM-DD"):
        debt = self.Get_Debt_By_ID(ID)
        if debt:
            if paymentDate == "YYYY-MM-DD":
                paymentDate = GetPresentTime()
            debt.Add_Payment(amount=amount, paymentDate=paymentDate)
            return True
        return False
        
    def Delete_Debt(self, ID: int):
        debt = self.Get_Debt_By_ID(ID)
        if debt:
            self.__debtList.remove(debt)
            return True
        return False
