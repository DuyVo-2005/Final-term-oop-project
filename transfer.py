from trans import *
class Transfer(Trans):
    def __init__(self, TransactionID: int, amount: int, time: str, accountNameSource: str = "",accountNameDestination: str = "") -> None:
        super().__init__(ID, amount, time)
        self.__accounccountNameSource = accountNameSource
        self.__accountNameDestination = accountNameDestination
        
    def Get_Account_Name_Source(self):
        return self.__accounccountNameSource

    def Set_Aaccount_Name_Source(self, newAccountNameSource: str):
        self.__accounccountNameSource = newAccountNameSource

    def Get_Account_Name_Destination(self):
        return self.__accountNameDestination

    def Set_Account_Name_Destination(self, newAccountNameDestination: str):
        self.__accountNameDestination = newAccountNameDestinationt

    def Make_Transfer(self, sourceAccount: 'Account', destinationAccount: 'Account', amount: int, time: str = "DD/MM/YYYY") -> bool:
        """Function to make transfer from sourceAccount to destinationAccount with the amount of money is amount
        Parameters:
            sourceAccount (class): the source account class makes a money transfer
            destinationAccount (class): the destination account class receives a money transfer
            amount (int): the amount of money transfer
        Returns:
            bool
        """
        super.Edit_Trans(account, time)
        if sourceAccount.Get_Balnace() < amount:
            messagebox.showerror(
                "Notification", "You don't have enough money for transfer"
            )
            return False
        else:
            self.Set_ID(sourceAccount.__CreateID())
            self.__accountNameSource = sourceAccount.Get_Account_Name()
            self.__accountNameDestination = destinationAccount.Get_Account_Name()
            sourceAccount.Set_Balnace(sourceAccount.Get_Balnace() - amount)
            destinationAccount.Set_Balnace(destinationAccount.Get_Balnace() + amount)
            self.__amount = amount
            sourceAccount.Get_Transfer_List().append(self)
            destinationAccount.Get_Transfer_List().append(self)
        return True
    def Edit_Transfer(self, sourceAccount: 'Account', destinationAccount: 'Account', amount: int) -> bool:
        """Function to make transfer from sourceAccount to destinationAccount with the amount of money is amount
        Parameters:
            sourceAccount (class): the source account class makes a money transfer
            destinationAccount (class): the destination account class receives a money transfer
            amount (int): the amount of money transfer
        Returns:
            bool
        """
        if sourceAccount.Get_Balnace() < amount:
            messagebox.showerror(
                "Notification", "You don't have enough money for transfer"
            )
            return False
        else:
            self.Set_ID(sourceAccount.__CreateID())
            self.__accountNameSource = sourceAccount.Get_Account_Name()
            self.__accountNameDestination = destinationAccount.Get_Account_Name()
            sourceAccount.Set_Balnace(sourceAccount.Get_Balnace() - amount)
            destinationAccount.Set_Balnace(destinationAccount.Get_Balnace() + amount)
            self.__amount = amount
            sourceAccount.Get_Transfer_List().append(self)
            destinationAccount.Get_Transfer_List().append(self)
        return True