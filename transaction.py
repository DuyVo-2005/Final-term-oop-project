from trans import *
class Transaction(Trans):
    def __init__(self, ID: int, amount: int, time: str, transactionType: str, catalog: str, note: str = "") -> None:
        super().__init__(ID, amount, time)
        self.__transactionType = transactionType
        self.__note = note
        self.__catalog = catalog

    def Get_Type(self):
        return self.__transactionType

    def Set_Type(self, newType: str = ""):
         self.__transactionType = newType

    def Get_Note(self):
        return self.__note

    def Set_Note(self, newNote: str = ""):
        self.__note = newNote

    def Get_Catalog(self):
        return self.__catalog

    def Set_Catalog(self, newCatalog: str):
        self.__catalog = newCatalog

    def Edit_Transaction(self, transactionType, amount, time, note, catalog) -> bool:
        """Function to edit existed transaction
        Parameters:
            transactionID(str): The id of transaction want to edit
            transactionType(str): The type of transaction want to edit (Income or Spending)
            amount(int): The amount of transaction want to edit
            time(datetime): The time of transaction want to edit
            note(str): The note of transaction want to edit
            catalog(str): The catalog of transaction want to edit
        Returns:
            None
        """
        super().Edit_Trans(amount, time)
        if (
            transactionType.capitalize() != "Income"
            and transactionType.capitalize() != "Spending"
        ):
            messagebox.showerror(
                "Notification", "Transaction type must be Income or Spending!"
            )
            return False
        else:
            self.Set_Type(transactionType)
            if transactionType.capitalize() == "Spending":
                self.Set_Amount(int((-1) * amount))

        self.Set_Note(note)
        global catalog_hint
        if catalog.capitalize() not in catalog_hint.values():
            messagebox.showerror("Notification", "Error catalog input!")
            return False
        else:
            self.Set_Catalog(catalog)

    def __str__(self):
        return f"{self.__transactionID} | {self.__time} | {self.__transactionType} | {self.__amount} | {self.__note} | {self.__catalog}"