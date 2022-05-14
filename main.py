import streamlit as st
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df= pd.read_csv("data.csv")
df

large = 22; med = 16; small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'axes.titlesize': med,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")

fig, ax = plt.subplots(figsize=(50,40), dpi= 80)    
sns.stripplot(df.GRP2015, df.I2015, size=20, ax=ax)
plt.title('Counts Plot', fontsize=22)
st.pyplot(fig)


plt.figure(figsize=(50, 20), dpi= 80)
sns.heatmap(df.corr(), xticklabels=df.corr().columns, yticklabels=df.corr().columns, cmap='RdYlGn', center=0, annot=True)
plt.title('Correlogram of GDP', fontsize=22)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.gcf().savefig("correlation.png")
