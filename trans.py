import account
from GetPresentTime import GetPresentTime
from datetime import datetime, timedelta

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

        
class Debt(Trans):
    def __init__(self, ID: int, fluctuation: str, amount: int, interestRate: float, dueDate: str, time: str = "YYYY-MM-DD", note: str = "") -> None:
        if time == "YYYY-MM-DD":
            time = GetPresentTime()
            
        time_date = datetime.strptime(time, "%Y-%m-%d")
        dueDate_date = datetime.strptime(dueDate, "%Y-%m-%d")
        if dueDate_date < time_date:
            dueDate_date = time_date + timedelta(days=365)
        dueDate = dueDate_date.strftime("%Y-%m-%d")
        
        super().__init__(ID, amount, time, note)
        self.__fluctuation = fluctuation
        self.__interestRate = interestRate
        self.__dueDate = dueDate
        self.__paymentHistory = []
        days_diff = (datetime.strptime(dueDate, "%Y-%m-%d") - datetime.strptime(time, "%Y-%m-%d")).days
        self.__remainingAmount = int(amount + (amount * (interestRate / 100) * days_diff))


    def Get_Fluctuation(self) -> str:
        return self.__fluctuation

    def Get_InterestRate(self) -> float:
        return self.__interestRate

    def Get_DueDate(self) -> str:
        return self.__dueDate

    def Get_Paid(self) -> str:
        return (self.__remainingAmount == 0)

    def Get_Remaining_Amount(self) -> int:
        return self.__remainingAmount

    def Get_PaymentHistory(self) -> list:
        return self.__paymentHistory

    def Set_Fluctuation(self, fluctuation: str):
        self.__fluctuation = fluctuation

    def Set_InterestRate(self, rate: float):
        self.__interestRate = rate

    def Set_DueDate(self, dueDate: str):
        self.__dueDate = dueDate


    def Add_Payment(self, amount: int, paymentDate: str = "YYYY-MM-DD") -> bool:
        if paymentDate == "YYYY-MM-DD":
            paymentDate = GetPresentTime()
        if amount > 0 and amount <= self.__remainingAmount:
            self.__paymentHistory.append({"date": paymentDate, "amount": amount})
            self.__remainingAmount -= amount
            if self.__remainingAmount < 0:
                self.__remainingAmount = 0
            return True
        return False



    
