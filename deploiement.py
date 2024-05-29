import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from matplotlib import pyplot as plt

# Charger les données avec la nouvelle méthode de mise en cache
@st.cache_data
def load_data():
    data = pd.read_csv('Africa_climate_change.csv')
    data['DATE'] = pd.to_datetime(data['DATE'], format='%Y%m%d %H%M%S')
    data["PRCP"] = data["PRCP"].fillna(data["PRCP"].mean())
    data["TAVG"] = data["TAVG"].fillna(data["TAVG"].mean())
    data["TMAX"] = data["TMAX"].fillna(data["TMAX"].mean())
    data["TMIN"] = data["TMIN"].fillna(data["TMIN"].mean())
    return data

data = load_data()

st.title('Tableau de bord sur le changement climatique en Afrique')

# Afficher les données
if st.checkbox('Afficher les données brutes'):
    st.write(data)

# Afficher le nombre de valeurs manquantes
st.subheader('Valeurs manquantes')
st.write(data.isna().sum())

# Graphique de distribution par pays
st.subheader('Distribution des enregistrements par pays')
fig, ax = plt.subplots()
data.groupby('COUNTRY').size().plot(kind='barh', color=sns.color_palette('Dark2'), ax=ax)
ax.spines[['top', 'right']].set_visible(False)
st.pyplot(fig)

# Graphique linéaire des fluctuations moyennes de la température en Tunisie et au Cameroun
st.subheader('Fluctuations moyennes de la température en Tunisie et au Cameroun')
tunisia_data = data[data['COUNTRY'] == 'Tunisia']
cameroon_data = data[data['COUNTRY'] == 'Cameroon']
combined_data = pd.concat([tunisia_data, cameroon_data])
fig = px.line(combined_data, x='DATE', y='TAVG', color='COUNTRY',
              title='Temperature Fluctuations de la Tunisia et Cameroon',
              labels={'DATE': 'Date', 'TAVG': 'Moyenne de Temperature (°F)'})
st.plotly_chart(fig)

# Filtre pour afficher les données de 1980 à 2005
st.subheader('Fluctuations de température (1980-2005) en Tunisie et au Cameroun')
start_date = st.date_input('Date de début', value=pd.to_datetime('1980-01-01'))
end_date = st.date_input('Date de fin', value=pd.to_datetime('2005-12-31'))
tunisia_data_filtered = tunisia_data[(tunisia_data['DATE'] >= pd.to_datetime(start_date)) & (tunisia_data['DATE'] <= pd.to_datetime(end_date))]
cameroon_data_filtered = cameroon_data[(cameroon_data['DATE'] >= pd.to_datetime(start_date)) & (cameroon_data['DATE'] <= pd.to_datetime(end_date))]
combined_data_filtered = pd.concat([tunisia_data_filtered, cameroon_data_filtered])
fig = px.line(combined_data_filtered, x='DATE', y='TAVG', color='COUNTRY',
              title=f'Temperature Fluctuations ({start_date.year}-{end_date.year}) in Tunisia and Cameroon',
              labels={'DATE': 'Year', 'TAVG': 'Avg Temperature (°F)'})
fig.update_layout(xaxis_title="Year", yaxis_title="Average Temperature (°F)")
st.plotly_chart(fig)

# Histogrammes pour la distribution de la température au Sénégal
st.subheader('Distribution de la température au Sénégal')
senegal_data = data[data['COUNTRY'] == 'Senegal']
fig = go.Figure()
fig.add_trace(go.Histogram(x=senegal_data[(senegal_data['DATE'] >= '1980-01-01') & (senegal_data['DATE'] <= '2000-12-31')]['TAVG'], 
                           name='1980-2000', opacity=0.75))
fig.add_trace(go.Histogram(x=senegal_data[(senegal_data['DATE'] > '2000-12-31') & (senegal_data['DATE'] <= '2023-12-31')]['TAVG'], 
                           name='2000-2023', opacity=0.75))
fig.update_layout(title_text='Temperature Distribution au Senegal (1980-2000 vs 2000-2023)',
                  xaxis_title_text='Temperature (°F)', yaxis_title_text='Count', barmode='overlay')
st.plotly_chart(fig)

# Graphique des températures moyennes par pays
st.subheader('Température moyenne par pays')
avg_temp_per_country = data.groupby('COUNTRY')['TAVG'].mean().reset_index()
fig = px.bar(avg_temp_per_country, x='COUNTRY', y='TAVG', title='Temperature moyenne par pays')
st.plotly_chart(fig)
