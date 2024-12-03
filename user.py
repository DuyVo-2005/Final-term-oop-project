class User:
    def __init__(self, userName):
        self.__userName = userName
        self.__accountsList = []
        self.__debtList = []

    def Get_Name(self):
        return self.__userName

    def Set_Name(self, userName):
        self.__userName = userName

    def Get_Account_List(self):
        return self.__accountsList

    def Get_Account(self, accountName: str) -> Account:
        for account in self.__accountsList:
            if account.Get_Account_Name() == accountName:
                return account

    def Set_Accounts(self, accounts):
        self.__accountsList = accounts

    def Get_Debt_List(self):
        return self.__debtList

    def Add_Account(self, account):
        """
        Adds an account to the user's list of accounts.
        Parameters:
            account (Account): The account to be added.
        Returns:
            None
        """
        self.__accountsList.append(account)

    def Delete_Account(self, accountID):
        """
        Deletes an account from the user's list based on account ID.
        Parameters:
            accountID (int): The ID of the account to be deleted.
        Returns:
            None
        """
        self.__accountsList = [account for account in self.__accountsList if account.get_accountID() != accountID]

    def View_Balance(self):
        """
        Displays the total balance of all accounts and details for each account.
        Parameters:
            None
        Returns:
            None
        """
        totalbalance = sum(account.get_balance() for account in self.__accountsList)
        print(f"Total balance: {totalbalance}")
        for account in self.__accountsList:
            print(account)

    def Add_Debt(self, otherID, amount, debtDate, dueDate, interestRate, debtType):
        """
        Adds a new debt to the user's debt list.
        Parameters:
            otherID (str): The ID of the person or entity the debt is with.
            amount (float): The amount of the debt.
            debtDate (str): The date the debt was created (in "YYYY-MM-DD" format).
            dueDate (str): The due date for the debt (in "YYYY-MM-DD" format).
            interestRate (float): The interest rate for the debt.
            debtType (str): Type of debt, either 'Borrower' or 'Lender'.
        Returns:
            Debt: The Debt object that was added to the list.
        """
        debtID = len(self.__debtList) + 1
        newDebt = Debt(debtID, otherID, amount, debtDate, dueDate, interestRate, debtType, status="Active")
        self.__debtList.append(newDebt)
        if debtType == "Borrower":
            print(f"{self.__userName} borrowed {amount} from {otherID}. Debt ID: {debtID} created.")
        else:
            print(f"{self.__userName} lent {amount} to {otherID}. Debt ID: {debtID} created.")
        return newDebt

    def Delete_Debt(self, debtID):
        """
        Deletes a debt from the user's debt list based on the debt ID.
        Parameters:
            debtID (int): The ID of the debt to be deleted.     
        Returns:
            None
        """
        self.__debtList = [debt for debt in self.__debtList if debt.get_debtID() != debtID]

    def Update_Debt(self, debtID, newAmount=None, newDueDate=None, newInterestRate=None, newStatus=None):
        """
        Updates an existing debt's details such as amount, due date, interest rate, or status.
        Parameters:
            debtID (int): The ID of the debt to be updated.
            newAmount (float, optional): The new debt amount (if any).
            newDueDate (str, optional): The new due date (if any).
            newInterestRate (float, optional): The new interest rate (if any).
            newStatus (str, optional): The new status of the debt (if any).
        Returns:
            bool: True if the debt was updated successfully, False if the debt ID was not found.
        """
        debt = next((debt for debt in self.__debtList if debt.get_debtID() == debtID), None)
        if debt:
            if newAmount is not None:
                debt.set_amount(newAmount)
            if newDueDate is not None:
                debt.set_dueDate(newDueDate)
            if newInterestRate is not None:
                debt.set_interestRate(newInterestRate)
            if newStatus is not None:
                debt.set_status(newStatus)
            print(f"Debt {debtID} updated successfully.")
            return True
        else:
            print(f"Debt with ID {debtID} not found.")
            return False

    def View_Debts(self):
        """
        Displays all debts associated with the user.
        """
        if not self.__debtList:
            print("No debts yet.")
        for debt in self.__debtList:
            print(debt)
