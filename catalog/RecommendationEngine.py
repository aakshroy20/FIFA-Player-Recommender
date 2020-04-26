# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 02:33:57 2020

@author: Private
"""


from .models import Playerdata
import pandas as pd
from sklearn.preprocessing import StandardScaler
from django.db import connection
from sklearn.metrics.pairwise import sigmoid_kernel
from django_pandas.io import read_frame

def get_data_frame(df,position):
    nongk_rs_cols = ['potential', 'skill_moves', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
    gk_rs_cols = ['potential','gk_diving','gk_handling','gk_kicking','gk_reflexes','gk_speed','gk_positioning']
    if (position=='Goalkeeper'):
      data_frame=df[df['Position']=='Goalkeeper'].set_index('sofifa_id')
      data_frame=data_frame[gk_rs_cols]
    elif(position=='Attacker'):
      data_frame=df[df['Position']=='Attacker'].set_index('sofifa_id')
      data_frame=data_frame[nongk_rs_cols]
    elif(position=='Defender'):
      data_frame=df[df['Position']=='Defender'].set_index('sofifa_id')
      data_frame=data_frame[nongk_rs_cols]
    else:
      data_frame=df[df['Position']=='Midfielder'].set_index('sofifa_id')
      data_frame=data_frame[nongk_rs_cols]
                          
    return data_frame


def Recommendation_System(df,player_id,k):

  query = str(Playerdata.objects.all().query) 
  df1 = pd.read_sql_query(query, connection)    
  ID2namesmapper=df1.set_index('sofifa_id')['short_name']  
  sc=StandardScaler()  
  df_sc=sc.fit_transform(df)
  kn=sigmoid_kernel(df_sc,df_sc)
  so_fifa_id=list(df.index)
  kn_df=pd.DataFrame(kn,index=so_fifa_id,columns=so_fifa_id)
  try:
    temp_dict=kn_df[player_id].to_dict()
    temp_list=list({k: v for k, v in sorted(temp_dict.items(), key=lambda item: item[1], reverse=True)}.keys())
    temp_list.remove(player_id)
    return ID2namesmapper[temp_list[0:k]].to_list()
  except:
    print('PlayerID not present in the database')
    



def get_player_id_position(df,name):
  query = str(Playerdata.objects.all().query) 
  df1 = pd.read_sql_query(query, connection)

  names2IDmapper=df1.set_index('short_name')['sofifa_id']  
  if name in names2IDmapper.index:
    player_id=names2IDmapper[name]
    position=df[df['sofifa_id']==player_id]['Position'].to_list()[0]
  return player_id,position
  