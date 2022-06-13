import streamlit as st
import wikipedia
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from bs4 import BeautifulSoup
import requests
from pywaffle import Waffle
import folium
import json
from streamlit_folium import st_folium
import sklearn
from sklearn.linear_model import LinearRegression
import re
import networkx as nx
from networkx.algorithms import bipartite
from scipy.sparse import csc_matrix

with st.echo(code_location='below'):
    def print_hello(name="World"):
        st.header(f" Привет, {name}!")


    st.write("Введите ваше имя")
    name = st.text_input("Your name", key="name", value="мой дружочек")
    a = print_hello(name)
    st.markdown(
        "В данном приложении вы узнаете немного о ресторанах Мишлен, сможете выбрать подходящий именно для Вас в любой точке мира, или же в любимой Москве. А также даже попробуете заказать пиццу")

    df = pd.read_csv("df_23.csv")
    st.markdown(
        "Давайте побольше узнаем о ценовых категориях в ресторанах Мишлен. Обратите внимание на обозначения среднего чека на человека.")
    st.markdown("Обозначения в долларах: 1 : 1-10;   11 : 11-50;   111 : 51-80;   1111 : 81-120;   11111 : 121-300")
    st.markdown("Итак, на следующем изображении вы можете увидеть, сколько ресторанов в каждой ценовой категории")
    ### построение визуализации (вафля)
    df_vaf = df.groupby('price').size().reset_index(name='counts')
    n_categories = df_vaf.shape[0]
    colors = [plt.cm.inferno_r(i / float(n_categories)) for i in range(n_categories)]
    figure = plt.figure(
        FigureClass=Waffle,
        plots={
            111: {
                'values': df_vaf['counts'],
                'labels': ["{0} ({1})".format(n[0], n[1]) for n in df_vaf[['price', 'counts']].itertuples()],
                'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.05, 1), 'fontsize': 12},
                'title': {'label': ' Распределение ценовых категорий у ресторанов Мишлен', 'loc': 'center',
                          'fontsize': 26}
            },
        },
        rows=7,
        colors=colors,
        figsize=(16, 9)
    )
    st.pyplot(figure)
    st.markdown("А какие же регионы наиболее дорогие и наоборот?")
    df2 = df.sort_values(by=["price"])
    fig, ax = plt.subplots(figsize=(20, 10))
    ax = sns.barplot(x="region", y="price", data=df2)
    plt.title('Distribution of regions by Michelen resturants price level', fontsize=30)
    st.pyplot(fig)

    ##Выбираем регион

    st.header("Рестораны Мишлен")
    st.markdown("В данном разделе вы сможете подобрать ресторан Мишлен, который подходит именно вам")
    st.markdown("Пожалуйста, выберите регион, в котором вы бы хотели испытать гастрономическое удовольствие.")
    Region = st.selectbox(
        "Region", df["region"].value_counts().index
    )
    df_selection = df[(df['region'] == Region)]
    st.markdown("Пожалуйста, выберите кухню, которые представлены в выбранном вами регионе.")
    Cuisine = st.selectbox(
        "Cuisine", df_selection["cuisine"].value_counts().index
    )
    df_selection = df[(df['region'] == Region) & (df['cuisine'] == Cuisine)]

    st.markdown(
        "Пожалуйста, выберите средний чек на человека. Выбор будет доступен если в выбранном вами регионе с определенной кухней представлены рестораны разных ценовых категорий")
    st.image('https://avatars.mds.yandex.net/i?id=630bf6a72ffd8e17c86e4908d3cddbc0-4230863-images-thumbs&n=13',
             width=200)
    average_check = st.radio("Select option", df_selection['price'].unique())
    st.write("Average check:", average_check)
    df_selection = df_selection[df_selection["price"] == average_check]
    st.markdown("В данной таблицу представдены все рестораны, подходящие по параметрам, которые были выбраны ранее")
    df_show = df_selection[["name", "region", "city", "price", "cuisine", "url"]]
    df_show

    st.markdown("Если в таблице представлены несколько ресторанов, можете выбрать любой из них")
    restaurant = st.radio("Select option", df_selection['name'].unique())
    st.write("Restaurant:", restaurant)
    df_selection_2 = df_selection[df_selection["name"] == restaurant]
    df_show = df_selection_2[["name", "region", "city", "price", "cuisine", "url"]]
    df_show
    st.markdown(
        "Для того чтобы насладиться ужином в выбранном ресторане, вам необходимо будет совершить путешествие в другой город. Посмотрите в каком замечательном месте находится ваш ресторан")
    st.markdown(
        "P.S. (Данные описания и картинки города я получаю с помощью веб-скреппинга, однако не у всех ресторанов на сате Мишлен есть описание и картинка с достопримечательностями города. Попробуйте выбрать Австрию, Тайпей, Грецию чтобы насладиться также описанием и фотографиями доспримечательностей)")

    cit = df_selection['city'][0:1].values[0]
    cit = wikipedia.search(cit)[0]
    st.write(cit)
    city = cit.replace(" ", "_")
    ssilka = 'https://en.wikipedia.org/wiki/' + city
    r = requests.get(ssilka)
    t = BeautifulSoup(r.text, 'html.parser')
    for link in t("img"):
        a = link.get('src')
    if (a is None) == False:
        itog = a
        ind = 1
    if ind == 1:
        break
    url = "https:" + itog
    st.image(url)
    discrp = df_selection_2['description'][0:1].values[0]
    st.write("Описание ресторана")
    discrp

    st.header("Географическое расположение ресторана")
    st.markdown(
        "Давайте же посмотрим на карте, где выбранный вами ресторан находится на карте. Он выделен розовым маркером.")
    st.header("Ааа, о ужас!")
    st.image('https://avatars.mds.yandex.net/i?id=158d4ddefbcb6b7b16a2354feb1bd061-4971670-images-thumbs&n=13',
             width=250)
    st.markdown(
        "Вы проделали долгий путь, приехали в ресторан, но вам там не понравилось. Очент грустно((( Что же делать?")
    st.image('https://avatars.mds.yandex.net/i?id=20ccdf5b3f2bb81bdd399e208e520ac4-5460273-images-thumbs&n=13',
             width=250)
    st.markdown(
        "Не переживайте, мы и это продумали! На карте также отмечены рестораны Мишлен поблизости (в регионах, где их несколько). Они выделены голубыми маркерами. Если вы наведете курсор на маркер, то высветится название ресторана! Да, Да, Всё для вашего удобства!")
    ###Карта
    lat = df_selection['latitude']
    lon = df_selection['longitude']
    name = df_selection['name']
    name_2 = df_selection_2['name']
    lat_2 = df_selection_2['latitude']
    lon_2 = df_selection_2['longitude']
    map = folium.Map(location=[lat_2, lon_2], zoom_start=9)
    folium.TileLayer('cartodbpositron').add_to(map)
    for lat, lon, name in zip(lat, lon, name):
        folium.Marker(location=[lat, lon], tooltip=str(name), icon=folium.Icon(color='blue'),
                      legend_name="Ресторан").add_to(map)
    for lat_2, lon_2, name_2 in zip(lat_2, lon_2, name_2):
        folium.Marker(location=[lat_2, lon_2], tooltip=str(name_2), icon=folium.Icon(color='pink'),
                      legend_name="Ресторан").add_to(map)
    st_data = st_folium(map, width=750)

    st.header("Москва и рестораны Мишлен?")
    st.markdown("Как вы думаете, в Москве есть рестораны Мишлен?")
    st.image("https://avatars.mds.yandex.net/i?id=9287d4e35f021a596a4f404bb0ef8ab9-5875528-images-thumbs&n=13",
             width=200)
    st.markdown("И вы, конечно, правы! Есть, и не один!! Пожалуйста, выберите ресторан из предложенного списка")
    rest_df = pd.read_csv("rest_df.csv")
    Restaurant_name = st.selectbox(
        "Restaurant_name", rest_df["name"].value_counts().index
    )
    df_selection = rest_df[(rest_df['name'] == Restaurant_name)]
    st.write(df_selection['name'][0:1].values[0])
    st.markdown("Правда, волшебная атмосфера?")
    st.image(df_selection['url'][0:1].values[0])

    st.header("Вы не москвич? И переживаете, что не сможете найти свое удовольствие?")
    st.markdown(
        "Да не переживайте, автор проекта все продумал!! На карте ниже вы увидете, где находятся эти волшебные места. При этом выбранный вами ресторан будет подсвечиваться розовым, а остальные будут оставаться голубыми, также навядя курсор на марке, высветится название")

    lat = rest_df['lat']
    lon = rest_df['lon']
    name = rest_df['name']
    name_2 = df_selection['name']
    lat_2 = df_selection['lat']
    lon_2 = df_selection['lon']
    map = folium.Map(location=[55.75, 37.61], zoom_start=12.5)
    for lat, lon, name in zip(lat, lon, name):
        folium.Marker(location=[lat, lon], tooltip=str(name), icon=folium.Icon(color='blue'),
                      legend_name="Ресторан").add_to(map)
    for lat_2, lon_2, name_2 in zip(lat_2, lon_2, name_2):
        folium.Marker(location=[lat_2, lon_2], tooltip=str(name_2), icon=folium.Icon(color='pink'),
                      legend_name="Ресторан").add_to(map)
    st_data = st_folium(map, width=750)

    st.header("Дороговато?")
    st.markdown("Вы студент и пока не можете себе позволить обед в ресторане Мишлен?")
    st.image("https://avatars.mds.yandex.net/i?id=6f0f9384b53314d8e6d72b0a64ec2148-5664046-images-thumbs&n=13",
             width=200)
    st.header("Пиццаааа")
    st.markdown(
        "Ну и сдался вам этот Мишлен. Давайте лучше закажем пиццу! Ведь пока вы думаете с друзьями над новым прибыльным проектом, вам нужно подкрепиться!!")

    pizza_df = pd.read_csv("pizza_df.csv")
    pizza_df['company'] = pizza_df['company'].str.replace('A', "5")
    pizza_df['company'] = pizza_df['company'].str.replace('B', "4")
    pizza_df['company'] = pizza_df['company'].str.replace('C', "3")
    pizza_df['company'] = pizza_df['company'].str.replace('D', "2")
    pizza_df['company'] = pizza_df['company'].str.replace('E', "1")
    pizza_df = pizza_df.rename(columns={'price_rupiah': 'price'})
    for i in range(len(pizza_df.index)):
        yacheika = pizza_df['price'][i:i + 1].values[0]
        length = len(yacheika)
        new_yacheika = yacheika[2:(length - 4)]
        pizza_df.loc[i, 'price'] = new_yacheika

    pizza_df['extra_sauce'] = pizza_df['extra_sauce'].str.replace('yes', "1")
    pizza_df['extra_sauce'] = pizza_df['extra_sauce'].str.replace('no', "0")
    pizza_df['extra_cheese'] = pizza_df['extra_cheese'].str.replace('yes', "1")
    pizza_df['extra_cheese'] = pizza_df['extra_cheese'].str.replace('no', "0")
    pizza_df['extra_mushrooms'] = pizza_df['extra_mushrooms'].str.replace("yes", "1")
    pizza_df['extra_mushrooms'] = pizza_df['extra_mushrooms'].str.replace('no', "0")

    pizza_df['company'] = pd.to_numeric(pizza_df['company'])
    pizza_df['price'] = pd.to_numeric(pizza_df['price'])
    pizza_df['extra_sauce'] = pd.to_numeric(pizza_df['extra_sauce'])
    pizza_df['extra_cheese'] = pd.to_numeric(pizza_df['extra_cheese'])
    pizza_df['extra_mushrooms'] = pd.to_numeric(pizza_df['extra_mushrooms'])

    pizza_df = pizza_df[["company", "price", "diameter", "extra_sauce", "extra_cheese", "extra_mushrooms"]]
    pizza_df["price"] = pizza_df.price.mul(3)
    st.markdown("Представляете, вы сможете выбрать пиццу с любыми параметрами и из любой компании, ну не сказка ли?")
    st.markdown("Пожалуйста, выберите рейтинг компании, где 5 - наивысший, 1 - наименьший")

    Company_raiting = st.selectbox(
        "Company", (5, 4, 3, 2, 1)
    )
    st.markdown("Пожалуйста, выберите диаметр пиццы")
    Diameter = st.columns(2)
    diameter = Diameter[0].number_input("Diameter", value=20)
    st.markdown("Хотите побольше соуса?")
    st.image("https://avatars.mds.yandex.net/i?id=6cee412ce1888538cd65d48400d1a691-5522949-images-thumbs&n=13",
             width=150)
    Extra_sauce = st.expander("Optional addings", True)
    extra_sauce = Extra_sauce.slider(
        "Extra Sauce",
        min_value=0.0,
        max_value=10.0
    )
    st.markdown("Или может быть любите много сыра?")
    st.image("https://avatars.mds.yandex.net/i?id=7f614ca37974fa56c9a4dd4272c222b0-7047516-images-thumbs&n=13",
             width=150)
    Extra_cheese = st.expander("Optional addings", True)
    extra_cheese = Extra_cheese.slider(
        "Extra cheese",
        min_value=0.0,
        max_value=10.0
    )
    st.markdown("А грибочки?")
    st.image("https://avatars.mds.yandex.net/i?id=7341e777084623275cda374c10155e0d-6974903-images-thumbs&n=13",
             width=150)
    Extra_mushrooms = st.expander("Optional addings", True)
    extra_mushrooms = Extra_mushrooms.slider(
        "Extra mushrooms",
        min_value=0.0,
        max_value=10.0
    )

    model = LinearRegression()
    model.fit(pizza_df.drop(columns=["price"]), pizza_df["price"])
    price = model.intercept_ + Company_raiting * model.coef_[0] + diameter * model.coef_[1] + extra_sauce * model.coef_[
        2] + extra_cheese * model.coef_[3] + extra_mushrooms * model.coef_[4]

    url_sir = "http://tuimazy-sushi.ru/uploads/newNew/0.jpg"
    url_gribi = "https://sakura-rolls31.ru/image/cache/catalog/gubkin/grib-1000x700.jpg"
    url_sous = "https://eatwell101.club/wp-content/uploads/2019/09/best-marinara-sauce-for-pizza-inspirational-pizza-sauce-vs-marinara-surprising-similarities-and-of-best-marinara-sauce-for-pizza.jpg"
    url_pysto = "https://avatars.mds.yandex.net/i?id=b7d3653f0d0bd0232886b3be4855f053-5232716-images-thumbs&n=13"
    ##Доп картинки
    if (extra_cheese > 0) and (extra_sauce == 0) and (extra_mushrooms == 0):
        st.image(url_sir, width=300)
    if (extra_cheese > 0) and (extra_sauce == 0) and (extra_mushrooms > 0):
        st.image(url_gribi, width=300)
    if (extra_cheese > 0) and (extra_sauce > 0) and (extra_mushrooms > 0):
        st.image(url_gribi, width=300)
    if (extra_cheese == 0) and (extra_sauce == 0) and (extra_mushrooms > 0):
        st.image(url_gribi, width=300)
    if (extra_cheese > 0) and (extra_sauce > 0) and (extra_mushrooms == 0):
        st.image(url_sir, width=300)
    if (extra_cheese == 0) and (extra_sauce > 0) and (extra_mushrooms == 0):
        st.image(url_sous, width=300)
    if (extra_cheese == 0) and (extra_sauce == 0) and (extra_mushrooms == 0):
        st.image(url_pysto, width=300)
        st.markdown("Точно хочешь без начинки?")
    st.markdown("Price:")
    st.write(round(price))

    pizza_df_new = pizza_df.copy()
    for i in range(len(pizza_df_new.index)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        if (pr >= 69) and (pr < 204):
            pri = 1
        elif (pr >= 204) and (pr < 339):
            pri = 2
        elif (pr >= 339) and (pr < 474):
            pri = 3
        elif (pr >= 474) and (pr < 609):
            pri = 4
        elif (pr >= 609) and (pr <= 744):
            pri = 5
        pizza_df_new.loc[i, 'price'] = pri
    st.header("Приятного аппетита!")

    st.header("А что внутри?")
    st.markdown(
        "Интересно, как программа предсказывает цену? Это работает с помощью машинного обучения. Давайте убедимся, что между параметрами есть взаимосвязь, например, между диаметром и ценой")

    fig, ax = plt.subplots(figsize=(30, 20), dpi=80)
    sns.stripplot(pizza_df.diameter, pizza_df.price, size=20, ax=ax)
    plt.title('Dependence of diameter on price', fontsize=40)
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=30)
    ax.set_xlabel("Diameter", fontsize=30)
    ax.set_ylabel("Price", fontsize=30)
    st.pyplot(fig)
    st.markdown("Да, связь же есть!")

    st.markdown("Интересно, а в каждой категории цены встречаются пиццы со всеми категориями добавок?")
    st.markdown("Чтобы это узнать преобразую таблицу с данными и выведу её на экран")
    st.markdown("Идею можете посмотреть в коде с хештегом: преобразование таблицы с пиццой.")
    pizza_df_new = pizza_df.copy()
    for i in range(len(pizza_df_new.index)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        if (pr >= 69) and (pr < 204):
            pri = 1
        elif (pr >= 204) and (pr < 339):
            pri = 2
        elif (pr >= 339) and (pr < 474):
            pri = 3
        elif (pr >= 474) and (pr < 609):
            pri = 4
        elif (pr >= 609) and (pr <= 744):
            pri = 5
        pizza_df_new.loc[i, 'price'] = pri
    tab = pd.DataFrame(
        {'name': ['sauce', 'cheese', 'mushrooms'], '1': [0, 0, 0], '2': [0, 0, 0], '3': [0, 0, 0], '4': [0, 0, 0],
         '5': [0, 0, 0]})
    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_sauce'][i:i + 1].values[0]
        if (pr == 1) and (sa == 1):
            tab.loc[0, '1'] = 1
    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_sauce'][i:i + 1].values[0]
        if (pr == 2) and (sa == 1):
            tab.loc[0, '2'] = 1
    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_sauce'][i:i + 1].values[0]
        if (pr == 3) and (sa == 1):
            tab.loc[0, '3'] = 1
    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_sauce'][i:i + 1].values[0]
        if (pr == 4) and (sa == 1):
            tab.loc[0, '4'] = 1
    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_sauce'][i:i + 1].values[0]
        if (pr == 5) and (sa == 1):
            tab.loc[0, '5'] = 1

    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_cheese'][i:i + 1].values[0]
        if (pr == 1) and (sa == 1):
            tab.loc[1, '1'] = 1
    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_cheese'][i:i + 1].values[0]
        if (pr == 2) and (sa == 1):
            tab.loc[1, '2'] = 1
    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_cheese'][i:i + 1].values[0]
        if (pr == 3) and (sa == 1):
            tab.loc[1, '3'] = 1
    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_cheese'][i:i + 1].values[0]
        if (pr == 4) and (sa == 1):
            tab.loc[1, '4'] = 1
    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_cheese'][i:i + 1].values[0]
        if (pr == 5) and (sa == 1):
            tab.loc[1, '5'] = 1

    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_mushrooms'][i:i + 1].values[0]
        if (pr == 1) and (sa == 1):
            tab.loc[2, '1'] = 1
    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_mushrooms'][i:i + 1].values[0]
        if (pr == 2) and (sa == 1):
            tab.loc[2, '2'] = 1
    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_mushrooms'][i:i + 1].values[0]
        if (pr == 3) and (sa == 1):
            tab.loc[2, '3'] = 1
    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_mushrooms'][i:i + 1].values[0]
        if (pr == 4) and (sa == 1):
            tab.loc[2, '4'] = 1
    for i in range(len(pizza_df_new)):
        pr = pizza_df_new['price'][i:i + 1].values[0]
        sa = pizza_df_new['extra_mushrooms'][i:i + 1].values[0]
        if (pr == 5) and (sa == 1):
            tab.loc[2, '5'] = 1
    tab
    st.markdown("в каждой категории цены встречаются пиццы со всеми категориями добавок.")
    st.markdown("Продемонстрируем это на графе.")
    list_tab = [(0, 5), (0, 6), (0, 7), (1, 5), (1, 6), (1, 7), (2, 5), (2, 6), (2, 7), (3, 5), (3, 6), (3, 7), (4, 5),
                (4, 6), (4, 7)]
    G = nx.Graph()
    k = nx.path_graph(8)
    G.add_nodes_from(k, color='blue')
    G.add_edges_from(list_tab, color='pink')
    figure, ax = plt.subplots()
    pos = nx.kamada_kawai_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='pink')
    st.pyplot(figure)
