from django.shortcuts import render
import pandas as pd
# Create your views here.
from .RecommendationEngine import get_data_frame,Recommendation_System,get_player_id_position
from django.db import connection
#from django_pandas.io import read_frame
from .models import Playerdata 


query = str(Playerdata.objects.all().query) 
df = pd.read_sql_query(query, connection)

def index(request):
    if request.method != 'POST':
        return render(request,'catalog/index.html')
        
    else:
        name=request.POST.get('player_name')
        if name in list(df.short_name):
            player_id,position=get_player_id_position(df,name)
            data_frame=get_data_frame(df,position)
            recommended_list=Recommendation_System(data_frame,player_id,5)
            context={}
            #context['supporting_text']="Players having similar ability to {} are: ".format(name)
            #context['list_of_names']=recommended_list
            context['searchedName']=name
            context['recommendedNames1']=recommended_list[0]
            context['recommendedNames2']=recommended_list[1]
            context['recommendedNames3']=recommended_list[2]
#           context['recommendedNames4']=recommended_list[3]
            context['recommendedNames5']=recommended_list[3]
            return render(request,'catalog/index.html',context)
        else:
            context={}
            context['supporting_text']="No player named {} present in database".format(name)
            return render(request,'catalog/index.html',context)