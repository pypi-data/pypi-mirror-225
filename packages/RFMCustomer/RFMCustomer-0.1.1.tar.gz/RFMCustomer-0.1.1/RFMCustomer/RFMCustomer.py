import pandas as pd
import numpy as np
import datetime
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

class CustomerSegmentation:
    def __init__(self, dataframe, day:str, positions:list, rfm, segment, color_gradient = False):
        self.dataframe = dataframe
        self.day = day
        self.positions = positions
        self.rfm = rfm
        self.segment = segment
        self.color_gradient = color_gradient
        
    def RFMCustomer(dataframe, day:str, positions:list):
        # Apply variable type transformation from string to datetime
        # The function a string like '20230628' with the format like 'yyyymmdd'.
        dataframe = dataframe.iloc[:, positions]
        
        if isinstance(dataframe, pd.DataFrame):
            day = datetime.strptime(day, "%Y%m%d")
            dataframe["Date"] = dataframe["Date"].apply(lambda x : datetime.strptime(x, "%Y%m%d"))
            rfm = dataframe.groupby('Customer ID').agg({
                'Date': lambda x : (day - x.max()).days,
                'Order ID': lambda x : len(x),
                'Sales': lambda x : x.sum()
            })
            rfm.columns = ["Recency", "Frequency", "Monetary"]
            
            rfm["R"] = pd.qcut(rfm["Recency"], 5, labels = [5,4,3,2,1])
            rfm["F"] = pd.qcut(rfm["Frequency"], 5, labels = [1,2,3,4,5])
            rfm["M"] = pd.qcut(rfm["Monetary"], 5, labels = [1,2,3,4,5])
            rfm["SCORE"] = rfm["R"].astype(str) + rfm["F"].astype(str) + rfm["M"].astype(str)
            
            def SEGMENTATION(row):
                if row["R"] >= 1 and row["R"] <= 2 and row["F"] >= 1 and row["F"] <= 2:
                    return 'Hibernating'
                elif row["R"] >= 1 and row["R"] <= 2 and row["F"] >= 3 and row["F"] <= 4:
                    return 'At Risk'
                elif row["R"] >= 1 and row["R"] <= 2 and row["F"] == 5:
                    return 'Can\'t looser'
                elif row["R"] >= 3 and row["F"] >= 1 and row["F"] <= 2:
                    return 'About to sleep'
                elif row["R"] == 3 and row["F"] == 3:
                    return 'Need attention'
                elif row["R"] >= 3 and row["R"] <= 4 and row["F"] >= 4 and row["F"] <= 5:
                    return 'Loyal customers'
                elif row["R"] == 4 and row["F"] == 1:
                    return 'Promising'
                elif row["R"] == 5 and row["F"] == 1:
                    return 'New customers'
                elif row["R"] >= 4 and row["R"] <= 5 and row["F"] >= 2 and row["F"] <= 3:
                    return 'Potential loyalists'
                elif row["R"] == 5 and row["F"] >= 4 and row["F"] <= 5:
                    return 'Champions'
            
            rfm["Segment"] = rfm["R"].astype(str) + rfm["F"].astype(str)
            rfm["R"] = rfm["R"].astype(int)
            rfm["F"] = rfm["F"].astype(int)
            rfm["Segment"] = rfm.apply(SEGMENTATION, axis = 1)
            
            return rfm
        else:
            print("Verificar que el input `dataframe` sea del tipo dataframe.")
    
    def RFMTable(rfm, color_gradient = False):
        rfm_group = rfm.groupby("Segment").mean().sort_values("Monetary", ascending = False)
        if color_gradient == True: 
            return rfm_group[["Recency", "Frequency", "Monetary"]].style.background_gradient(cmap='Blues')
        else:
            return rfm_group[["Recency", "Frequency", "Monetary"]]
    
    def RFMAnalysis(rfm):
        dataplot = pd.DataFrame(rfm.groupby("Segment")["SCORE"].count()).apply(lambda x : round(x/len(rfm["SCORE"])*100,2)).sort_values(by = 
                    "SCORE", ascending = True).rename(columns = {'SCORE':'Clientes (%)'})
        fig, ax = plt.subplots(figsize = (8,6), dpi = 70)
        dataplot.plot(ax = ax, kind = 'barh', color = 'mediumaquamarine')
        ax.bar_label(ax.containers[0], fontsize = 12)
        for i in ['bottom', 'left']:
            ax.spines[i].set_color('black')
            ax.spines[i].set_linewidth(1.5) 
        right_side = ax.spines["right"]
        right_side.set_visible(False)
        top_side = ax.spines["top"]
        top_side.set_visible(False)
        ax.set_axisbelow(True)
        ax.grid(color='gray', linewidth=1, axis='y', alpha=0.4)
        plt.xlabel('Porcentaje de clientes')
        plt.ylabel('Segmento RFM')
        plt.title("Customers By Segment (%)", size = 16, fontweight = 'bold')
        plt.show()
    
    def RFMAnalysisByCategory(rfm):
        rfm_group = round(rfm[["Recency", "Frequency", "Monetary"]],2)
        fig = plt.figure(figsize=(15,8))
        ax1 = fig.add_subplot(2,2,1)
        ax1.bar(rfm_group.index, rfm_group["Recency"].sort_values(ascending = False), color = '#C79FEF')
        plt.xticks(rotation = 90)
        plt.subplots_adjust(hspace=0.9)
        ax1.set_title("Recency", size = 14)

        for i in ['bottom', 'left']:
            ax1.spines[i].set_color('black')
            ax1.spines[i].set_linewidth(1.5) 
        right_side = ax1.spines["right"]
        right_side.set_visible(False)
        left_side = ax1.spines["left"]
        left_side.set_visible(False)
        top_side = ax1.spines["top"]
        top_side.set_visible(False)
        bottom_side = ax1.spines["bottom"]
        bottom_side.set_visible(False)
        ax1.set_axisbelow(True)
        ax1.grid(color='gray', linewidth=1, axis='y', alpha=0.4)
        ax1.bar_label(ax1.containers[0], fontsize = 9)

        ax2 = fig.add_subplot(2,2,2)
        ax2.bar(rfm_group.index, rfm_group["Frequency"].sort_values(ascending = False), color = "#40E0D0")
        plt.xticks(rotation = 90)
        ax2.set_title("Frequency", size = 14)

        for i in ['bottom', 'left']:
            ax1.spines[i].set_color('black')
            ax1.spines[i].set_linewidth(1.5) 
        right_side = ax2.spines["right"]
        right_side.set_visible(False)
        left_side = ax2.spines["left"]
        left_side.set_visible(False)
        top_side = ax2.spines["top"]
        top_side.set_visible(False)
        bottom_side = ax2.spines["bottom"]
        bottom_side.set_visible(False)
        ax2.set_axisbelow(True)
        ax2.grid(color='gray', linewidth=1, axis='y', alpha=0.4)
        ax2.bar_label(ax2.containers[0], fontsize = 9)

        ax3 = fig.add_subplot(2,1,2)
        ax3.bar(rfm_group.index, rfm_group["Monetary"].sort_values(ascending = False), color = "#FFA150")
        ax3.set_title("Monetary", size = 14)
        for i in ['bottom', 'left']:
            ax3.spines[i].set_color('black')
            ax3.spines[i].set_linewidth(1.5) 
        right_side = ax3.spines["right"]
        right_side.set_visible(False)
        left_side = ax3.spines["left"]
        left_side.set_visible(False)
        top_side = ax3.spines["top"]
        top_side.set_visible(False)
        bottom_side = ax3.spines["bottom"]
        bottom_side.set_visible(False)
        ax3.set_axisbelow(True)
        ax3.grid(color='gray', linewidth=1, axis='y', alpha=0.4)
        ax3.bar_label(ax3.containers[0], fontsize = 9)

        plt.suptitle("RFM Analysis By Segment", size = 16, fontweight = 'bold')
        plt.show()
        
    def RFMFindClientsBySegment(rfm, segment):
        segments = rfm["Segment"].unique()
        if segment in segments:
            rfm = rfm.reset_index()
            rfm = rfm[rfm["Segment"] == segment]
            return rfm
        else:
            print(f'''
Por favor, inserta un segmento válido.
Teniendo en cuenta que los segmentos válidos son \n{",".join(segments)}.
            ''')