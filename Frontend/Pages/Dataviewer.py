import glob 
import pandas as pd
import numpy as np
from numpy.typing import NDArray
from typing import Any
import camelot
import calendar
import streamlit as st

from numpy.random import default_rng as rng


df = pd.DataFrame(
    rng(0).standard_normal((50, 20)), columns=("col %d" % i for i in range(20))
)

st.dataframe(df)