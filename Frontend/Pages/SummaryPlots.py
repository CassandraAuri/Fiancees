import glob 
import pandas as pd
import numpy as np
from numpy.typing import NDArray
from typing import Any
import camelot
import matplotlib.pyplot as plt
import streamlit as st
from typing import Tuple
#plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')
class graphing:
    class plotting():
        def axiscreator(fig, i) -> None:
            ax = fig.add_subplot(i, 1, i) 

        def Balance(fig,dataframe) -> plt.Figure:
            if len(fig.axes) == 0:
                graphing.plotting.axiscreator(fig, len(fig.axes)+1) #creates an axis object
                min,max=graphing.InitalizationAndAesthetics.Balance_ylimit_setter(dataframe)
                st.write(min,ax)
                fig.axes[0].set_ylim(min,max)
            for ax in fig.axes:
                ymin, ymax = ax.get_ylim()
                if np.max(dataframe["balance"]) >ymax:
                    graphing.plotting.axiscreator(fig, len(fig.axes)+1)
                    fig.axes[len(fig.axes)+1].set_ylim(graphing.InitalizationAndAesthetics.Balance_ylimit_setter(dataframe))
                else:
                    ax.plot(dataframe["date"], dataframe["balance"], marker="o")

            return fig
        

    class InitalizationAndAesthetics:
        def BalanceInit() -> plt.Figure:
            fig = plt.figure()
            return fig
        def Balance_ylimit_setter(dataframe) -> Tuple[int, int]:
            max = np.max(dataframe["balance"])
            st.write(max)
            if max>0 and max<1000:
                return (0, 1000)
            elif max>1000 and max<10000:
                return (1000,10000)
            elif max>10000:
                return (10000,max+1000)
            else: 
                ValueError("You seriously messed up dude")



    class Backend():
        
        
        def Balance() -> None:
            figure = graphing.InitalizationAndAesthetics.BalanceInit()

            userdataframe=st.session_state["userdataframe"]


            for i, account in enumerate(st.session_state["Accounts"]):

                mask=userdataframe["accountID"] == account
                Balance= userdataframe[mask]

                figure = graphing.plotting.Balance(figure, Balance)
                
                st.pyplot(figure)
            pass
        def Change() -> None:
            pass
            
        def ExpenseProfile() -> None:
            pass

        #TODO Node viewer
        def init(graphoptions) -> None:
            st.write(st.session_state["GraphOptions"])
            if st.session_state["GraphOptions"] !=[]:
                for graph in st.session_state["GraphOptions"]:
                    getattr(graphing.Backend, graph)()

    class GUI():
        def SelectionBox(graphoptions) -> list:

            st.multiselect(label="What Would you like to graph", options=graphoptions, key="GraphOptions", help="Balance=Linegraph; Change=bargraph; expense/balance profile=pie graph")
            return graphoptions

        def init() -> None:
            graphoptions=["Balance", "Change", "ExpenseProfile", "BalanceProfile"]
            graphing.GUI.SelectionBox(graphoptions)
            graphing.Backend.init(graphoptions)
        
graphing.GUI.init()

        
        
        

