from account import Account
from trans import Transfer
import random

class User:
    def __init__(self) -> None:
        self.__accountsList = []
        self.__transferList = []

    def __CreateID(self) -> int:
        __listID = []
        for Trans in self.__transferList:
            __listID.append(Trans.Get_ID())

        __thisTranID = random.randint(100_000, 999_999)
        while __thisTranID in __listID:
            __thisTranID = random.randint(100_000, 999_999)

        return __thisTranID

    def Get_Account_List(self) -> list:
        return self.__accountsList
    
    def Get_Transfer_List(self) -> list:
        return self.__transferList
    
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

    def Add_Account(self, account: Account):
        self.__accountsList.append(account)

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
