from typing import NewType
from weather.models import City
import requests
from django.shortcuts import redirect, render
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=a4619b467086908a608702b90a1a5d6e'
    err= ''
    meassage=''
    meassage_class=''
    if request.method == 'POST':
        print(request.POST)
        form = CityForm(request.POST)
        if form.is_valid():
            new_city=form.cleaned_data['name']
        
            existing= City.objects.filter(name=new_city).count()
        
            if existing == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod']== 200:
                 form.save()
                 print("Form saved ")
                
                else:
                  err= 'City doesnot exist in the world'
            else:
             err='City already exist in page'

             
             form = CityForm() 
                
          
        if err :
             meassage= err
             meassage_class='is-danger'
        else:
             meassage='City added Successfuly '
             meassage_class='is-success'


    form = CityForm() 

    cities = City.objects.all()
    form = CityForm()
    weather_data = []

    for city in cities:

        r = requests.get(url.format(city.name)).json()
        
        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)
    

    context = {
        'weather_data': weather_data,'form' : form,
         'message': meassage,
         'message_class': meassage_class
        }
    return render(request, 'weather/weather.html', context)

def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')

        
