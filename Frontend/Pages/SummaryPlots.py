import glob 
import pandas as pd
import numpy as np
from numpy.typing import NDArray
from typing import Any
import camelot
import matplotlib.pyplot as plt
import streamlit as st


class GraphingBackend():
    def Balance() -> None:
        for i, account in enumerate(st.session_state["Accounts"]):
            #TODO if the balance of different accounts is order of magntidues off, plot seperate, for right now plot together
            Balance=st.session_state["Csvfile"]
            st.pyplot()
        pass
    def Change() -> None:
        pass
        
    def ExpenseProfile() -> None:
        pass

    
    def init(graphoptions) -> None:
        st.write(st.session_state["GraphOptions"])
        if st.session_state["GraphOptions"] !=[]:
            [graphtype() for graphtype in st.session_state["GraphOptions"]]

class GraphingGUI():
    def SelectionBox(graphoptions) -> list:

        st.multiselect(label="What Would you like to graph", options=graphoptions, key="GraphOptions", help="Balance=Linegraph; Change=bargraph; expense/balance profile=pie graph")
        return graphoptions

    def init() -> None:
        graphoptions=["Balance", "Change", "Expense profile", "Balance Profile"]
        GraphingGUI.SelectionBox(graphoptions)
        GraphingBackend.init(graphoptions)
        
GraphingGUI.init()

        
        
        

