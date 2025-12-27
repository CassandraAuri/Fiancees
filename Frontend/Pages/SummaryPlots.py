import glob 
import pandas as pd
import numpy as np
from numpy.typing import NDArray
from typing import Any
import camelot
import matplotlib.pyplot as plt
import streamlit as st

class Graphing():
    def SelectionBox() -> None:
        graphoptions=["Balance (line plot)", "Change (bar graph)", "Expense profile (pie)", "Balance Profile (pie) "]
        st.multiselect(label="What Would you like to graph", options=graphoptions, key="GraphOptions")

    def init() -> None:
        Graphing.SelectionBox()

Graphing.init()
        
        
        

