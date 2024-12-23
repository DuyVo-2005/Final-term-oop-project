from datetime import datetime, timedelta
class Debt:
    def __init__(self, debtID: str, otherID: str, amount: float, debtDate: str, dueDate: str, interestRate: float, debtType: str, status: str = "Active") -> None:
        self.__debtID = debtID
        self.__otherID = otherID
        self.__amount = amount
        self.__debtDate = datetime.strptime(debtDate, "%Y-%m-%d")
        self.__dueDate = datetime.strptime(dueDate, "%Y-%m-%d")
        self.__interestRate = interestRate
        self.__debtType = debtType
        self.__status = status
        self.__debtList = []

    def Get_DebtID(self) -> str:
        return self.__debtID

    def Set_DebtID(self, debtI: str) -> None):
        self.__debtID = debtID

    def Get_OtherID(self) -> str:
        return self.__otherID

    def Set_OtherID(self, otherID: str) -> None:
        self.__otherID = otherID

    def Get_Amount(self) -> float:
        return self.__amount

    def Set_Amount(self, amount: float) -> None:
        self.__amount = amount

    def Get_DebtDate(self) -> datatime:
        return self.__debtDate

    def Set_DebtDate(self, debtDate: str) -> None:
        self.__debtDate = datetime.strptime(debtDate, "%Y-%m-%d")

    def Get_DueDate(self) -> datatime:
        return self.__dueDate

    def Set_DueDate(self, dueDate: str) -> None:
        self.__dueDate = datetime.strptime(dueDate, "%Y-%m-%d")

    def Get_InterestRate(self) -> float:
        return self.__interestRate

    def Set_InterestRate(self, interestRate: float) -> None:
        self.__interestRate = interestRate

    def Get_DebtType(self) -> str:
        return self.__debtType

    def Set_DebtType(self, debtType: str) -> None:
        self.__debtType = debtType

    def Get_Status(self) -> str:
        return self.__status

    def Set_Status(self, status: str) -> None:
        self.__status = status

    def Add_Payment(self, paymentAmount: float, paymentDate: str) -> None:
        """
        Adds a payment to the debt and updates the debt balance. 
        If the debt is fully paid, it updates the status to 'Paid'.
        Parameters:
            paymentAmount (float): The amount paid towards the debt.
            paymentDate (str): The date of the payment in "YYYY-MM-DD" format.
        Returns:
            None
        """
        paymentDate = datetime.strptime(paymentDate, "%Y-%m-%d")        
        self.__debtList.append({"payment_date": paymentDate, "amount": paymentAmount})
        self.__amount -= paymentAmount
        if self.__amount <= 0:
            self.__status = "Paid"

    def Get_PaymentHistory(self) -> list:
        return self.__debtList
    
    def Calculate_Interest(self, compound: bool = False) -> float:
         """
        Calculates the interest on the debt based on the interest rate and the duration.
        If "compound" is True, compound interest is calculated, otherwise, simple interest is applied.
        Parameters:
            compound (bool, optional): Whether to use compound interest (default is False for simple interest).
        Returns:
            float: The total amount due after interest is applied.
        """
        today = datetime.now()
        periods = (today - self.__debtDate).days / 365.0
        if compound:
            total_amount = self.__amount * (1 + self.__interestRate / 100) ** periods
        else:
            total_amount = self.__amount * (1 + (self.__interestRate / 100) * periods)
        return round(total_amount, 2)
    
    def Reminder_Due_Date(self) -> None:
         """
        Checks the due date of the debt and provides reminders if the debt is nearing its due date
        or is overdue.
        Parameters:
            None
        Returns:
            None
        """
        today = datetime.now()
        days_to_due = (self.__dueDate - today).days
        if self.__status == "Active":
            if days_to_due > 0:
                if days_to_due <= 7:  
                    print(f"Reminder: Debt {self.__debtID} is due in {days_to_due} days.")
            elif days_to_due == 0:
                print(f"Reminder: Today is the last day to pay off Debt {self.__debtID}.")
            else:
                print(f"Warning: Debt {self.__debtID} is overdue by {abs(days_to_due)} days.")
    
    def Check_Due_Status(self) -> None:
        """
        Checks if the debt is overdue based on the current date and updates the status to "Overdue"
        if the due date has passed.
        Parameters:
            None
        Returns:
            None
        """
        today = datetime.now()
        if self.__status == "Active" and today > self.__dueDate:
            self.__status = "Overdue"

    def __str__(self) -> str:
        """
        Returns a string representation of the debt, including key details such as the debt amount,
        due date, status, interest rate, and payment history.
        Parameters:
            None
        Returns:
            str: A formatted string describing the debt details.
        """
        self.check_due_status()
        payments = len(self.__debtList)
        return (f"Debt ID: {self.__debtID}, Other ID: {self.__otherID}, Amount: {self.__amount}, "
                f"Debt Date: {self.__debtDate.date()}, Due Date: {self.__dueDate.date()}, Status: {self.__status}, "
                f"Debt Type: {self.__debtType}, Interest Rate: {self.__interestRate}%, Payments: {payments}")
        self.check_due_status()
        payments = len(self.__debtList)
        return (f"Debt ID: {self.__debtID}, Other ID: {self.__otherID}, Amount: {self.__amount}, "
                f"Debt Date: {self.__debtDate.date()}, Due Date: {self.__dueDate.date()}, Status: {self.__status}, "
                f"Debt Type: {self.__debtType}, Interest Rate: {self.__interestRate}%, Payments: {payments}")
