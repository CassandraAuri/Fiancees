import glob 
import pandas as pd
import numpy as np
from numpy.typing import NDArray
from typing import Any, List
import camelot
import os

class Loader():
    data_filename = "Data/FinancesData.csv"
    update_filename = "Data/FinancesUpdate.csv"
    accountId_filename= "Data/AccountIDs.csv"

    @staticmethod
    def upload():
        """
        Checks if any new files must be added and adds them to the datafile
        """
        with open(Loader.update_filename, "r") as updatefile:
            updates = pd.read_csv(updatefile)        
        newfiles = [filename for filename in glob.glob(f"Statements/*") if Loader.check(filename, updates)]

        with open(Loader.accountId_filename, "r") as accountfile:
            accountIDs = pd.read_csv(accountfile)
        for filename in newfiles:
            if "MasterCard Statement" in filename:
                '''RBC Statement'''
                statements = Loader.RBCtoTransaction(filename, accountIDs)
            elif "monthly-statement-transactions" in filename:
                '''Wealthsimple Statement'''
                statements = Loader.WealthsimpletoTransaction(filename,accountIDs)
            else:
                raise(NotImplementedError(f"{filename} is not a supported statement type"))
            
            #Append transactions to datafile
            #Update the updates file

    @staticmethod  
    def check(filename: str, updates)-> bool:
        '''Checks if the file exists and needs uploading to the datafile'''
        if(not os.path.exists(filename)):
            raise(FileNotFoundError(f"{filename} does not exist"))
        elif(filename in updates["filename"].values and 
             os.path.getmtime(filename)==float(updates[updates["filename"]==filename]["timestamp"].iloc[0])):
            return False
        else:
            return True

    def RBCtoTransactions(filename, accountIDs)->List[Transaction]:
        #Cassandra's code for reading RBC PDF statements
        tables = camelot.read_pdf(
            filename,
            flavor="stream"   # RBC statements work best with stream
        )
        df_raw = pd.concat([t.df for t in tables], ignore_index=True)
        df = df_raw.copy()
        df.columns = ["transaction_date", "posting_date", "description", "amount", "extra"]
        df = df.fillna("")
        import re
        mask = (
            df["transaction_date"].str.match(
                r"(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+\d{1,2}",
                na=False
            )
            & df["amount"].str.contains(r"\$", na=False)
        )
        df_tx = df[mask].copy()
        df_tx["amount"] = (
            df_tx["amount"]
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .astype(float)
        )
        accountId = accountIDs[accountIDs["Number"]==filename.split(" ")[-1:-4]]["AccountID"].iloc[0]
        balance = None #TODO: Extract balance from statement
        currency = "CAD" #Default currency
        year = int(re.search(r"\d{4}", filename.split(" ")[2]).group(0))
        transactions = [Transaction(entry.transaction_date, accountId, entry.amount, balance, entry.description, currency) for entry in df_tx.itertuples()]
        return transactions

    def WealthsimpletoTransactions(filename, accountIDs)->List[Transaction]:
        statements = np.array(pd.read_csv(filename))
        transactions = []
        for entry in statements:
            accountID = accountIDs[accountIDs["AccountName"]==filename.split("_")[0]]["AccountID"].iloc[0] 
            transaction = Transaction(entry[0], accountID, entry[3], entry[4], entry[2], entry[5])
            transactions.append(transaction)
        return transactions

class Transaction():
    """Implements a financial transaction as a dictionary-like object"""
    def __init__(self, date, accountID, amount, balance, description, currency="CAD"):
        self.date = date
        self.accountID = accountID
        self.amount = amount
        self.balance = balance
        self.description = description
        self.currency = currency