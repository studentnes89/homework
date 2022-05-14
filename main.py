import streamlit as st
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import folium
from streamlit_folium import st_folium
import json
df= pd.read_csv("data.csv")

df_new = df[["Region", "GRP2014", "GRP2015", "GRP2016", "I2014", "I2015", "I2016", "I_prod2014", "I_prod2015", "I_prod2016", "I_inf2014", "I_inf2015", "I_inf2016"]]
Region = st.selectbox(
        "Region", df_new["Region"].value_counts().index
    )
df_selection = df_new[lambda x: x["Region"] == Region]
df_selection



fig, ax = plt.subplots(figsize=(50,40), dpi= 80)    
sns.stripplot(df.GRP2015, df.I2015, size=20, ax=ax)
plt.title('Dependence of GDP on Investment', fontsize=40)
st.pyplot(fig)


fig = plt.figure(figsize=(50, 20), dpi= 80)
sns.heatmap(df.corr(), xticklabels=df.corr().columns, yticklabels=df.corr().columns, cmap='RdYlGn', center=0, annot=True)
plt.title('Correlogram of GDP', fontsize=40)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
st.pyplot(fig)

df_new = df[["GRP2014", "I2014", "I_prod2014", "I_inf2014"]]


fig = plt.figure(figsize=(50, 20), dpi= 80)
sns.heatmap(df_new.corr(), xticklabels=df_new.corr().columns, yticklabels=df_new.corr().columns, cmap='RdYlGn', center=0, annot=True)
plt.title('Correlogram of GDP2014', fontsize=40)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
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
ax.set_zlabel("Investment (all)")
ax.scatter(x, y, z)
plt.title('Separation of Investments', fontsize=22)
st.pyplot(fig)

geo = f"geo.json"
m = folium.Map(location = [0,0], zoom_start = 3)
folium.Choropleth(
        geo_data=geo,
        name="choropleth",
        data=df_1_clean,
        columns=["GRP2014", "Region"],
        key_on="ADMIN",
        fill_color="YlGn",
        fill_opacity=0.7,
        nan_fill_opacity = 0,
        line_opacity=0.2,
        legend_name="Region",
    ).add_to(m)
folium.LayerControl().add_to(m)
st_data = st_folium(m, width = 725)
st_data
