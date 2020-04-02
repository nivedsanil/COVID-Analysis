from django.shortcuts import render
import folium 
import pandas as pd
import requests
import json
import os
import csv 
from pandas.io.json import json_normalize
# Create your views here.

def maps(request):

    country_geo = os.path.join(os.getcwd(),'countries.geo.json')

    
    url = "https://api.covid19api.com/summary"

    response = requests.request("GET", url)
    response_dict=response.json()

    df=json_normalize(response_dict['Countries'])
    df.to_csv('covid_data3.csv', index=False)

    covid_data=pd.read_csv('covid_data3.csv')

    # Sum of total confirmed
    confirmed_cases=covid_data['TotalConfirmed'].sum()
     # Sum of total deaths
    death_cases=covid_data['TotalDeaths'].sum()
     # Sum of total recovered
    recovered_cases=covid_data['TotalRecovered'].sum()

    # Total Confirmed Cases 

    m = folium.Map(tiles="cartodbpositron", max_bounds=True, no_wrap = True, min_zoom=2, max_zoom=18, zoom_start=2)

    folium.Choropleth( 

        geo_data=country_geo,
        name='choropleth',
        data=covid_data,
        columns=['Country', 'TotalConfirmed'],
        key_on='feature.properties.name',
        fill_color='Reds',
        fill_opacity=0.7,
        line_opacity=0.2,
        nan_fill_color = 'white',
        legend_name='COVID Confirmed', 

    ).add_to(m)

    folium.TileLayer('cartodbdark_matter').add_to(m)
    map_html = m._repr_html_()

    # Total Deaths

    death = folium.Map(tiles="cartodbpositron", max_bounds=True, no_wrap = True, min_zoom=2, max_zoom=18, zoom_start=2)

    folium.Choropleth( 

        geo_data=country_geo,
        name='choropleth',
        data=covid_data,
        columns=['Country', 'TotalDeaths'],
        key_on='feature.properties.name',
        fill_color='Reds',
        fill_opacity=0.7,
        line_opacity=0.2,
        nan_fill_color = 'white',
        legend_name='COVID Deaths', 

    ).add_to(death)

    folium.TileLayer('cartodbdark_matter').add_to(death)
    death_html = death._repr_html_()

    # Recovered

    recovered = folium.Map(tiles="cartodbpositron", max_bounds=True, no_wrap = True, min_zoom=2, max_zoom=18, zoom_start=2)

    folium.Choropleth( 

        geo_data=country_geo,
        name='choropleth',
        data=covid_data,
        columns=['Country', 'TotalRecovered'],
        key_on='feature.properties.name',
        fill_color='Greens',
        fill_opacity=0.7,
        line_opacity=0.2,
        nan_fill_color = 'white',
        legend_name='COVID Recovered', 

    ).add_to(recovered)

    folium.TileLayer('cartodbdark_matter').add_to(recovered)
    recovered_html = recovered._repr_html_()

    country_name=[]
    cases=[]

    for i in range(1,len(response_dict['Countries'])):

        country_name.append(response_dict['Countries'][i]['Country'])
        cases.append(response_dict['Countries'][i]['TotalConfirmed'])
    
    country_stats=zip(country_name,cases)
    context={

        'map_html':map_html,
        'death_html':death_html,
        'recovered_html':recovered_html,
        'confirmed_cases':confirmed_cases,
        'death_cases':death_cases,
        'recovered_cases':recovered_cases,
        'country_stats':country_stats,

    }

    return render(request, 'pages/maps.html',context)


def total_confirmed(request):

    return render(request, 'pages/total_confirmed.html')
