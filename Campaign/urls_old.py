from django.urls import path,include
from .views import *

urlpatterns = [
    # campaign set
    path('campset/create', create_campset),
    path('campset/all', all_campset),
    path('campset/one', one_campset),
    path('campset/status_campset', status_campset),

    # campaign
    path('camp/create', create_camp),
    path('camp/all', all_camp),
    path('camp/one', one_camp),
    path('camp/status_camp', status_camp),
    path('camp/filter_campaign', filter_campaign)
    
]
