import glob 
import pandas as pd
import numpy as np
from numpy.typing import NDArray
from typing import Any
import camelot
import matplotlib.pyplot as plt
import streamlit as st
from typing import Tuple
import matplotlib.gridspec as gridspec
from datetime import datetime
#plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')
class utils():
    def month_to_number(month) -> str:
        return datetime.strptime(month, "%B").strftime("%m")
    def dateformating(year, month) -> str:
        return f"{year}-{utils.month_to_number(month)}-01"
class graphing:
    class plotting():
        def Balance(fig,dataframe) -> plt.Figure:
            for ax in fig.axes:
                ax.plot(pd.to_datetime(dataframe["date"], format="%Y-%m-%d"), dataframe["balance"], marker="o")
                plt.xticks(rotation=45)

            return fig
        
        def Change(fig,positive,negative,i) -> plt.Figure:
            width = 0.25  # the width of the bars
            multiplier = 0

            fig, ax = plt.subplots(layout='constrained')
            #https://www.geeksforgeeks.org/python/plotting-multiple-bar-charts-using-matplotlib-in-python/
            for attribute, measurement in penguin_means.items(): #https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html
                offset = width * multiplier
                rects = ax.bar(x + offset, measurement, width, label=attribute)
                ax.bar_label(rects, padding=3)
                multiplier += 1
            for ax in fig.axes:


    class InitalizationAndAesthetics:
        def BalanceInit(dataframe) -> plt.Figure:
            
            limits=[[1e5,1e6],[10000,1e5],[1000,10000],[0,1000] ]
            rows=[]
            st.dataframe(dataframe)
            for i, (low, high) in enumerate(limits):
                # safer condition: values actually inside the range
                if np.any((dataframe["balance"] > low) &
                        (dataframe["balance"] < high)):
                    rows.append((low, high, i))
            fig = plt.figure(figsize=(7, 3+2*len(rows)))
            gs = gridspec.GridSpec(
                len(rows), 1,
                hspace=0.1
            )
            
            axes = []
            for idx, (low, high, _) in enumerate(rows):
                ax = fig.add_subplot(
                    gs[idx],
                    sharex=axes[0] if axes else None
                )
                ax.set_ylim(low, high)
                axes.append(ax)

            # 3️⃣ hide x labels except bottom
            for ax in axes[:-1]:
                ax.label_outer()

            return fig

        def ChangeInit() -> plt.Figure:
            length = len(st.session_state["Accounts"])
            fig = plt.subplots(figsize=(7, 3+2*length), nrows=length)
            
            return fig


    class Backend():
        
        
        def Balance() -> None:

            userdataframe=st.session_state["userdataframe"]

            mask = userdataframe["accountID"].isin(st.session_state["Accounts"])
            userdataframebalance = userdataframe[mask]

            figure = graphing.InitalizationAndAesthetics.BalanceInit(userdataframe)


            for i, account in enumerate(st.session_state["Accounts"]):

                
                mask=userdataframe["accountID"] == account
                Balance= userdataframe[mask]
                figure = graphing.plotting.Balance(figure, Balance)
                
                st.pyplot(figure)
            pass
        def Change() -> None:
            userdataframe=st.session_state["userdataframe"]

            figure = graphing.InitalizationAndAesthetics.ChangeInit()


            months=st.session_state["Months"]
            years=st.session_state["Years"]
            start, end = utils.dateformating(years[0], months[0]), utils.dateformating(years[1], months[1])

            months = pd.date_range(
                start=start,
                end=end,
                freq="MS"   # Month Start
            ).strftime("%Y-%m").tolist()

            for i, account in enumerate(st.session_state["Accounts"]):
                mask=userdataframe["accountID"] == account
                
                monthpositive = []
                monthnegative = []

                for month in months:
                    start = month.to_timestamp("M") - pd.offsets.MonthEnd(1) + pd.Timedelta(days=1)
                    end = month.to_timestamp("M")

                    mask = userdataframe["dates"].between(start, end)
                    currentdataframe = userdataframe["dates"][mask]


                    positiveindicies = np.where(currentdataframe["amount"] > 0 )[0]
                    negativeindicies = np.where(currentdataframe["amount"] < 0 )[0]
                    monthpositive.append(np.sum(currentdataframe["amount"][positiveindicies]))
                    monthnegative.append(np.sum(currentdataframe["amount"][negativeindicies]))

                graphing.plotting.Change(figure, monthpositive, monthnegative, i)
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

        
        
        

