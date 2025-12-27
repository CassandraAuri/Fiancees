import glob 
import pandas as pd
import numpy as np
from numpy.typing import NDArray
from typing import Any
import camelot
class Loader():
    
    def load(AccountName, bank) ->NDArray:
        if bank == "Wealthsimple":
            Loader.LoadWealthsimple(AccountName)
        elif bank == "RBC":
            if type(AccountName) != "str" or len(AccountName) != 4:
                ValueError("AccountName must be <Accounttype>-#4dig")
            if "Mastercard" in AccountName:
                PDFCHECKER()
                files = glob.glob(f"{AccountName}*.csv")
                
                pass
            else:
                NotImplementedError(f"This account type is not currently supported")

        else:
            NotImplementedError(f"{bank} has not been implemented yet")
    def LoadRBC(AccountName) -> NDArray:
        
    def LoadWealthsimple(AccountName) -> NDArray:
            files = glob.glob(f"{AccountName}*.csv")
            statement = np.array(
                pd.read_csv(
                    file for file in files 
                    )
                )
            return statement


        
    def PDFChecker(Accountname):
        if len(glob.glob(f"MasterCard*".csv)) == None:
            pass
    def RBCtoCSV(file) -> pd.DataFrame:
        raise(NotImplementedError)

   

class MoneyData():
    def init()
        