from django.shortcuts import render
import requests
# Create your views here.

def charts(request):
    
   
    urlcountry= "https://api.covid19api.com/countries"

    if request.method == "POST":

        name=request.POST['name']

        url = "https://api.covid19api.com/country/"+name+"/status/confirmed/live"

        payload = []
        headers= []

        response = requests.request("GET", url, headers=headers, data = payload)
        response_country = requests.request("GET", urlcountry, headers=headers, data = payload)

        country_dict=response_country.json()
        chart_dict=response.json()

        dates=[]
        cases=[]
        
        response_country = requests.request("GET", urlcountry, headers=headers, data = payload)
    
        country=[]

        for j in range(0, len(country_dict)):

            country.append(country_dict[j]['Slug'])

        for i in range (0,len(chart_dict)):
            
            dates.append(chart_dict[i]['Date'])
            cases.append(chart_dict[i]['Cases'])

        # chart_data=zip(dates,cases)
        
        context = {

            'countries':country,
            'dates':dates,
            'cases':cases,      
        }

        return render(request, 'pages/trend-charts.html', context)

    else:

        payload = []
        headers= []

        response_country = requests.request("GET", urlcountry, headers=headers, data = payload)
        country_dict=response_country.json()

        country=[]

        for j in range(0, len(country_dict)):

            country.append(country_dict[j]['Slug'])

        context = {

            'countries':country
        }

        return render(request, 'pages/trend-charts.html', context)

