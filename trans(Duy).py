from tkinter import *
from tkinter import messagebox
import datetime
import random
from account import *

def GetPresentTime(
) -> str:
        datetime_now = datetime.datetime.now()
        formatted_datetime = datetime_now.strftime("%Y-%m-%d")
        return formatted_datetime

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
    def __init__(self, amount: int, time: str = "DD/MM/YYYY") -> None:
        self.__ID = ""
        self.__amount = amount
        self.__time = time

    def Get_ID(self):
        return self.__ID

    def Set_ID(self, newID: int):
        self.__ID =  newID
    
    def Get_Amount(self):
        return self.__amount

    def Set_Amount(self, newAmount: int):
        self.__amount = newAmount

    def Get_Time(self):
        return self.__time

    def Set_Time(self, newTime: str):
        self.__time = newTime        
        
    def Edit_Trans(self, amount: int, time: str = "DD/MM/YYYY") -> bool:
        if time is not "DD/MM/YYYY":
            dateFormat = "%d/%m/%Y"
            self.Set_Time(datetime.datetime.strptime(time, dateFormat))
        else:
            messagebox.showerror(
                "Notification", "Date time isn't valid! Default set system date"
            )
            self.Set_Time(GetPresentTime())
        try:
            self.Set_Amount(int(amount))           
        except ValueError:
            messagebox.showerror("Notification", "amount must be integer")
            return False            
        return True            
