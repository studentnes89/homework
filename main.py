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
from geopandas.tools import geocode

df= pd.read_csv("data.csv")

df_new = df[["Region", "GRP2014", "GRP2015", "GRP2016", "I2014", "I2015", "I2016", "I_prod2014", "I_prod2015", "I_prod2016", "I_inf2014", "I_inf2015", "I_inf2016"]]
Region = st.selectbox(
        "Region", df_new["Region"].value_counts().index
    )
df_selection = df_new[lambda x: x["Region"] == Region]
df_selection



fig, ax = plt.subplots(figsize=(30,20), dpi= 200)    
sns.stripplot(df.GRP2015, df.I2015, size=90, ax=ax)
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


st.title("Region with the lowest GRP")
loc = 'Gorno-Altay'
location = geocode(loc, provider="nominatim" , user_agent = 'my_request')
point = location.geometry.iloc[0] 

data= pd.DataFrame({"longitude":[point.x], "latitude":[point.y]})

mapit = folium.Map( location=[0, 0], zoom_start=1 ) 
for lat , lon in zip(data.latitude , data.longitude): 
        folium.Marker( location=[ lat,lon ], fill_color='#43d9de', radius=8 ).add_to( mapit ) 
st_data = st_folium(mapit, width = 725)
st_data
 
                    
                    
                    ###https://pythonim.ru/libraries/geopandas-v-python
