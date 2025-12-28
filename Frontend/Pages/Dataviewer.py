import glob 
import pandas as pd
import numpy as np
from numpy.typing import NDArray
from typing import Any
import camelot
import calendar
import streamlit as st

if "userdataframe" in st.session_state:
    st.dataframe(st.session_state["userdataframe"])
else:
    st.write("Please initalize conditions to create a datatable")