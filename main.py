import streamlit as st
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
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
plt.title('Dependence of GDP on Investment', fontsize=22)
st.pyplot(fig)


fig = plt.figure(figsize=(50, 20), dpi= 80)
sns.heatmap(df.corr(), xticklabels=df.corr().columns, yticklabels=df.corr().columns, cmap='RdYlGn', center=0, annot=True)
plt.title('Correlogram of GDP', fontsize=22)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
st.pyplot(fig)

df_new = df[["GRP2014", "I2014", "I_prod2014", "I_inf2014"]]
df_new

fig = plt.figure(figsize=(50, 20), dpi= 80)
sns.heatmap(df_new.corr(), xticklabels=df_new.corr().columns, yticklabels=df_new.corr().columns, cmap='RdYlGn', center=0, annot=True)
plt.title('Correlogram of GDP2014', fontsize=22)
plt.xticks(fontsize=9)
plt.yticks(fontsize=9)
st.pyplot(fig)

df2=df.sort_values(by=["GRP2014"])[::10]
fig, ax = plt.subplots(figsize=(16,10))
ax = sns.barplot(x="Region", y="GRP2014", data=df2)
plt.title('Distribution of regions by GDP level from the smallest to the largest', fontsize=22)
st.pyplot(fig)

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
x = df['I_prod2014']
y = df['I_inf2014']
z = df['I2014']
ax.set_xlabel("Production I")
ax.set_ylabel("Infrastructure I")
ax.set_zlabel("All I")
ax.scatter(x, y, z)
plt.title('Separation of Investments', fontsize=22)
st.pyplot(fig)

