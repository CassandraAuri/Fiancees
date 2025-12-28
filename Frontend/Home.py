import glob 
import pandas as pd
import numpy as np
from numpy.typing import NDArray
from typing import Any
import camelot
import calendar
import streamlit as st
from datetime import datetime
class csvlogic():
    def month_to_number(month) -> str:
        return datetime.strptime(month, "%B").strftime("%m")
    def dateformating(year, month) -> str:
        return f"{year}-{csvlogic.month_to_number(month)}-01"
    
    def readcsv() -> None:
        if "csvmasterfile" not in st.session_state:
            st.session_state["csvmasterfile"] = pd.read_csv("../data.csv")#TODO get file when stupid backend dev gets it done (rolls eyes), im going to prettify now
            pass
    def userselecteddataframe() -> None:
        
        userdataframe=st.session_state["csvmasterfile"]

        #Select Accounts
    
        if st.session_state["Accounts"] == []:
            pass
        else:
            mask=userdataframe["accountID"].isin(st.session_state["Accounts"])
            userdataframe=userdataframe[mask]
            #Select Date
            months=st.session_state["Months"]
            years=st.session_state["Years"]
            userselecteddates=[csvlogic.dateformating(years[0], months[0]), csvlogic.dateformating(years[1], months[1])]
            st.write(userdataframe.keys())
            mask = (userdataframe['date'] > userselecteddates[0]) & (userdataframe['date'] <= userselecteddates[1])
            userdataframefinal=userdataframe[mask]
            st.write()
            st.session_state["userdataframe"]= userdataframefinal

class Dates_UserSelected():
    
    def monthslider() -> None:
        months = list(calendar.month_name)[1:]  # January → December
        if "Months" not in st.session_state:
            st.session_state["Months"]=[months[0], months[-1]]
        st.select_slider("Month Range",options=months, value=st.session_state["Months"], key="Months")
        if st.session_state["Months"][0] == st.session_state["Months"][1]:
            st.warning("Choose a Month range, not the same month")

    def yearslider() -> None:
        years = [2023,2024,2025,2026]
        
        if "Years" not in st.session_state:
            st.session_state["Years"] = [2023, 2026]
        
        st.select_slider("Month Range",options=years, value=st.session_state["Years"], key="Years")

        
        if st.session_state["Years"][0] == st.session_state["Years"][1]:
            st.warning("Choose a Month range, not the same month")
    def accounts() -> None:
        if "Accounts" not in st.session_state:
            st.session_state["Accounts"] = []
        Accounts= [0,1]
        st.multiselect("Accounts to plot", options=Accounts, key="Accounts")
    


    def init() -> None:
        csvlogic.readcsv()
        Dates_UserSelected.yearslider()
        Dates_UserSelected.monthslider()
        Dates_UserSelected.accounts()
        csvlogic.userselecteddataframe()
    
        
       


class Streamlit():
    def Streamlitinit():
        st.title("Home Navigation Page")
        

        Dates_UserSelected.init()
        pages=Pagedocuments.pages_init()
        pg = st.navigation(pages, position="top")
        pg.run()
class Pagedocuments():
    def pages_init() -> dict:
        Path="Pages/"
        pages = glob.glob(f"{Path}*.py")
        pagesdict = [ st.Page(page, title=page.removesuffix(".py").removeprefix("Pages/")) for page in pages]
        return pagesdict

Streamlit.Streamlitinit()