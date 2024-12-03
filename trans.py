import account
from GetPresentTime import GetPresentTime

class Trans():
    def __init__(self, ID: int, amount: int, time: str = "YYYY-MM-DD", note: str = "") -> None:
        self.__amount = amount
        if time == "YYYY-MM-DD":
            time = GetPresentTime()
        self.__time = time
        self.__note = note
        self.__ID = ID

    def Get_ID(self) -> int:
        return self.__ID
    
    def Get_Amount(self) -> int :
        return self.__amount

    def Get_Time(self) -> str:
        return self.__time
    
    def Get_Note(self) -> str:
        return self.__note
    
    def Set_Note(self, newNote: str = ""):
        self.__note = newNote

    def Set_Time(self, newTime: str):
        self.__time = newTime


class Transaction(Trans):
    def __init__(self, cataLog: str, ID: int, fluctuation: str, amount: int, time: str = "YYYY-MM-DD", note: str = "") -> None:
        super().__init__(ID, amount, time, note)
        self.__cataLog = cataLog
        self.__fluctuation = fluctuation

    def Get_Catalog(self) -> str:
        return self.__cataLog
    
    def Get_Fluctuation(self) -> str:
        return self.__fluctuation


class Transfer(Trans):
    def __init__(self, ID: int, amount: int, sourceAccount: account.Account, desAccount: account.Account, time: str = "YYYY-MM-DD", note: str = "") -> None:
        super().__init__(ID, amount, time, note)
        self.__sourceAccount = sourceAccount
        self.__desAccount = desAccount

    def Get_Source_Account(self) -> account.Account:
        return self.__sourceAccount
    
    def Get_Des_Account(self) -> account.Account:
        return self.__desAccount
