from django.urls import path
from . import views 

urlpatterns=[

    path('',views.maps, name="maps"),
    path('total_confirmed/', views.total_confirmed, name="total_confirmed")
]