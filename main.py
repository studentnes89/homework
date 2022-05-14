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

st.header("Economical Growth")
df= pd.read_csv("data.csv")
st.markdown("Please, choose the Region of Russian Federation and get information about Gross Regional Product (GRP) and Infrastructures")
df_new = df[["Region", "GRP2014", "GRP2015", "GRP2016", "I2014", "I2015", "I2016", "I_prod2014", "I_prod2015", "I_prod2016", "I_inf2014", "I_inf2015", "I_inf2016"]]
Region = st.selectbox(
        "Region", df_new["Region"].value_counts().index
    )
df_selection = df_new[lambda x: x["Region"] == Region]
df_selection


st.markdown("This graph shows the correlation beetween important economic growth indicators")
fig = plt.figure(figsize=(50, 20), dpi= 80)
sns.heatmap(df.corr(), xticklabels=df.corr().columns, yticklabels=df.corr().columns, cmap='RdYlGn', center=0, annot=True)
plt.title('Correlogram of GRP', fontsize=60)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
st.pyplot(fig)

df_new = df[["GRP2014", "I2014", "I_prod2014", "I_inf2014"]]


st.markdown("Let`s see closer. It`s an example of correlation beetween indicators in one year")

fig = plt.figure(figsize=(50, 20), dpi= 20)
sns.heatmap(df_new.corr(), xticklabels=df_new.corr().columns, yticklabels=df_new.corr().columns, cmap='RdYlGn', center=0, annot=True)
plt.title('Correlogram of GRP2014', fontsize=60)
plt.xticks(fontsize=50)
plt.yticks(fontsize=50)
st.pyplot(fig)

st.markdown("We have noticed the dependence beetween GRP and Infrastructure. Let`s show it on a graph")
fig, ax = plt.subplots(figsize=(30,20), dpi= 80)    
sns.stripplot(df.GRP2015, df.I2015, size=20, ax=ax)
plt.title('Dependence of GRP on Investment', fontsize=40)
plt.xticks(fontsize=5)
plt.yticks(fontsize=30)
ax.set_xlabel("GRP2015", fontsize=30)
ax.set_ylabel("Investments2015", fontsize=30)
st.pyplot(fig)

st.markdown("We distribute the regions by the smallest, medium and large GRP")
df2=df.sort_values(by=["GRP2014"])[::10]
fig, ax = plt.subplots(figsize=(16,10))
ax = sns.barplot(x="Region", y="GRP2014", data=df2)
plt.title('Distribution of regions by GRP level from the smallest to the largest', fontsize=30)
st.pyplot(fig)

st.markdown("Investments consist of Infrastructure and Production Investments. Let`s see the separation of them on the graph")
###FROM: https://pythonru.com/biblioteki/seaborn-plot
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
x = df['I_prod2014']
y = df['I_inf2014']
z = df['I2014']
ax.set_xlabel("Production I")
ax.set_ylabel("Infrastructure I")
ax.set_zlabel("Investment (all)")
ax.scatter(x, y, z)
plt.title('Separation of Investments', fontsize=10)
st.pyplot(fig)
###END FROM

###Построение карты частично основывалось на примере с данного сайта: https://pythonim.ru/libraries/geopandas-v-python
st.markdown("Where is the Regions with the smallest and the biggest GRP are located?")
st.title("Region with the smallest GRP")
loc = 'Gorno-Altay'
location = geocode(loc, provider="nominatim" , user_agent = 'my_request')
point = location.geometry.iloc[0] 

data= pd.DataFrame({"longitude":[point.x], "latitude":[point.y]})

mapit = folium.Map( location=[0, 0], zoom_start=1 ) 
for lat , lon in zip(data.latitude , data.longitude): 
        folium.Marker( location=[ lat,lon ], fill_color='#43d9de', radius=8 ).add_to( mapit ) 
st_data = st_folium(mapit, width = 725)
st_data

st.title("Region with the biggest GRP")
loc = 'Moscow'
location = geocode(loc, provider="nominatim" , user_agent = 'my_request')
point = location.geometry.iloc[0] 

data= pd.DataFrame({"longitude":[point.x], "latitude":[point.y]})

mapit = folium.Map( location=[0, 0], zoom_start=1 ) 
for lat , lon in zip(data.latitude , data.longitude): 
        folium.Marker( location=[ lat,lon ], fill_color='#43d9de', radius=8 ).add_to( mapit ) 
st_data = st_folium(mapit, width = 725)
st_data


                    
                    
                    
