import streamlit as st
import pandas as pd
import math 
import numpy as np 
import datetime
from datetime import date, timedelta, datetime
#from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def data1(date_str): 
  import datetime  
  date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
  u1="https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-secondaire/Taux-de-reference-des-bons-du-tresor?"
  #u2="date=24%2F02%2F2023&"
  u3="block=e1d6b9bbf87f86f8ba53e8518e882982#address-c3367fcefc5f524397748201aee5dab8-e1d6b9bbf87f86f8ba53e8518e882982"
  u21="date="
  u22=date_obj.day
  u23="%2F"
  u24=date_obj.month
  u25="%2F"
  u26=date_obj.year
  u27="&"
  u2=u21+ str(u22) + u23 + str(u24) + u25 + str(u26) + u27
  url=u1+u2+u3
  data1=pd.read_html(url)
  data1[0].drop(data1[0].index[-1], inplace=True)
  data1[0]["Maturité"] = pd.to_datetime(data1[0]["Date d'échéance"],format='%d/%m/%Y') - pd.to_datetime(data1[0]['Date de la valeur'],format='%d/%m/%Y')
  data1[0]["Maturité"] = data1[0]["Maturité"].dt.total_seconds().astype(float)/ (24 * 60 * 60)
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace('%','')
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace(',','.')
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].astype(float)
  return data1[0]

# Définir une fonction de multiplication par 100
def multiply_by_100(x):
    return x * 100

def court_terme(date_str): 
  import datetime  
  date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
  u1="https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-secondaire/Taux-de-reference-des-bons-du-tresor?"
  #u2="date=24%2F02%2F2023&"
  u3="block=e1d6b9bbf87f86f8ba53e8518e882982#address-c3367fcefc5f524397748201aee5dab8-e1d6b9bbf87f86f8ba53e8518e882982"
  u21="date="
  u22=date_obj.day
  u23="%2F"
  u24=date_obj.month
  u25="%2F"
  u26=date_obj.year
  u27="&"
  u2=u21+ str(u22) + u23 + str(u24) + u25 + str(u26) + u27
  url=u1+u2+u3
  data1=pd.read_html(url)
  data1[0].drop(data1[0].index[-1], inplace=True)
  data1[0]["Maturité"] = pd.to_datetime(data1[0]["Date d'échéance"],format='%d/%m/%Y') - pd.to_datetime(data1[0]['Date de la valeur'],format='%d/%m/%Y')
  data1[0]["Maturité"] = data1[0]["Maturité"].dt.total_seconds().astype(float)/ (24 * 60 * 60)
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace('%','')
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace(',','.')
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].astype(float)/100
  n=len(data1[0])
  L=[]
  for i in range(len(data1[0])):
    if data1[0]['Maturité'][i]<=365:
      L.append(i)
  indice1=L[-1]+1 
  l=[]
  for i in range(len(data1[0])):
    if data1[0]['Maturité'][i]>=365:
      l.append(i)
  indice2=l[0]-1
  # initialiser les listes de données
  x1_data = []
  x2_data = []
  # boucle for pour remplir les listes
  for i in range(indice1+1):
    x1_data.append(data1[0].iloc[i,2])
    x2_data.append(data1[0].iloc[i,4]) 
  # créer un DataFrame à partir des listes de données
  data2 = pd.DataFrame({'Maturity': x2_data, 'Taux': x1_data})
  # afficher le DataFrame
  a=(360/data2.iloc[indice1,0])*((1+data2.iloc[indice1,1])**(data2.iloc[indice1,0]/365)-1)
  data2.iloc[indice1,1]=a # taux monetaire
  data2['Taux'] = data2['Taux'].apply(multiply_by_100)
  # TMP
  u4="https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Marche-monetaire-interbancaire?startDate=&"
  #u5="endDate=26%2F02%2F2023&"
  u6="block=ae14ce1a4ee29af53d5645f51bf0e97d#address-d3239ec6d067cd9381f137545720a6c9-ae14ce1a4ee29af53d5645f51bf0e97d"
  u51="endDate="
  u52=date_obj.day
  u53="%2F"
  u54=date_obj.month
  u55="%2F"
  u56=date_obj.year
  u57="&"
  u5=u51+ str(u52) + u53 + str(u54) + u55 + str(u56) + u57
  url2=u4+u5+u6
  data=pd.read_html(url2)
  data[0].iloc[0,1]
  b=[i for i in data[0].iloc[0,1]]
  c=b[0]+b[2]+b[3]+b[4]
  d=int(c)/100000  
  # créer un DataFrame à partir des listes de données
  TMP = pd.DataFrame({'Maturity': [1], 'Taux': [d]})
  TMP['Taux'] = TMP['Taux'].apply(multiply_by_100)
  df_concat1 = pd.concat([TMP, data2])
  df_concat1  = df_concat1.reset_index(drop=True) # Réinitialiser l'indexation à partir de 0
  return df_concat1 

def long_terme(date_str): 
  import datetime  
  date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
  u1="https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-secondaire/Taux-de-reference-des-bons-du-tresor?"
  #u2="date=24%2F02%2F2023&"
  u3="block=e1d6b9bbf87f86f8ba53e8518e882982#address-c3367fcefc5f524397748201aee5dab8-e1d6b9bbf87f86f8ba53e8518e882982"
  u21="date="
  u22=date_obj.day
  u23="%2F"
  u24=date_obj.month
  u25="%2F"
  u26=date_obj.year
  u27="&"
  u2=u21+ str(u22) + u23 + str(u24) + u25 + str(u26) + u27
  url=u1+u2+u3
  data1=pd.read_html(url)
  data1[0].drop(data1[0].index[-1], inplace=True)
  data1[0]["Maturité"] = pd.to_datetime(data1[0]["Date d'échéance"],format='%d/%m/%Y') - pd.to_datetime(data1[0]['Date de la valeur'],format='%d/%m/%Y')
  data1[0]["Maturité"] = data1[0]["Maturité"].dt.total_seconds().astype(float)/ (24 * 60 * 60)
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace('%','')
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace(',','.')
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].astype(float)/100
  n=len(data1[0])
  L=[]
  for i in range(len(data1[0])):
    if data1[0]['Maturité'][i]<=365:
      L.append(i)
  indice1=L[-1]+1 
  l=[]
  for i in range(len(data1[0])):
    if data1[0]['Maturité'][i]>=365:
      l.append(i)
  indice2=l[0]-1
  # initialiser les listes de données
  x3_data = []
  x4_data = []
  # boucle for pour remplir les listes
  for i in range(indice2,n):
    x3_data.append(data1[0].iloc[i,2])
    x4_data.append(data1[0].iloc[i,4]) 
  # créer un DataFrame à partir des listes de données
  data3 = pd.DataFrame({'Maturity': x4_data, 'Taux': x3_data})
  # afficher le DataFrame
  b=((1+(data3.iloc[0,1]*(data3.iloc[0,0]/360)))**(365/data3.iloc[0,0]))-1
  data3.iloc[0,1]=b
  data3['Taux'] = data3['Taux'].apply(multiply_by_100)
  return data3

def taux_rendement(date_str): 
  import datetime  
  date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
  u1="https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-secondaire/Taux-de-reference-des-bons-du-tresor?"
  #u2="date=24%2F02%2F2023&"
  u3="block=e1d6b9bbf87f86f8ba53e8518e882982#address-c3367fcefc5f524397748201aee5dab8-e1d6b9bbf87f86f8ba53e8518e882982"
  u21="date="
  u22=date_obj.day
  u23="%2F"
  u24=date_obj.month
  u25="%2F"
  u26=date_obj.year
  u27="&"
  u2=u21+ str(u22) + u23 + str(u24) + u25 + str(u26) + u27
  url=u1+u2+u3
  data1=pd.read_html(url)
  data1[0].drop(data1[0].index[-1], inplace=True)
  data1[0]["Maturité"] = pd.to_datetime(data1[0]["Date d'échéance"],format='%d/%m/%Y') - pd.to_datetime(data1[0]['Date de la valeur'],format='%d/%m/%Y')
  data1[0]["Maturité"] = data1[0]["Maturité"].dt.total_seconds().astype(float)/ (24 * 60 * 60)
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace('%','')
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace(',','.')
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].astype(float)/ (100)
  n=len(data1[0])
  L=[]
  for i in range(len(data1[0])):
    if data1[0]['Maturité'][i]<=365:
      L.append(i)
  indice1=L[-1]+1 
  l=[]
  for i in range(len(data1[0])):
    if data1[0]['Maturité'][i]>=365:
      l.append(i)
  indice2=l[0]-1
  # initialiser les listes de données
  x1_data = []
  x2_data = []
  # boucle for pour remplir les listes
  for i in range(indice1+1):
    x1_data.append(data1[0].iloc[i,2])
    x2_data.append(data1[0].iloc[i,4]) 
  # créer un DataFrame à partir des listes de données
  data2 = pd.DataFrame({'Maturity': x2_data, 'Taux': x1_data})
  # afficher le DataFrame
  a=(360/data2.iloc[indice1,0])*((1+data2.iloc[indice1,1])**(data2.iloc[indice1,0]/365)-1)
  data2.iloc[indice1,1]=a # taux monetaire
  # initialiser les listes de données
  x3_data = []
  x4_data = []
  # boucle for pour remplir les listes
  for i in range(indice2,n):
    x3_data.append(data1[0].iloc[i,2])
    x4_data.append(data1[0].iloc[i,4]) 
  # créer un DataFrame à partir des listes de données
  data3 = pd.DataFrame({'Maturity': x4_data, 'Taux': x3_data})
  # afficher le DataFrame
  b=((1+(data3.iloc[0,1]*(data3.iloc[0,0]/360)))**(365/data3.iloc[0,0]))-1
  data3.iloc[0,1]=b
  # TMP
  u4="https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Marche-monetaire-interbancaire?startDate=&"
  #u5="endDate=26%2F02%2F2023&"
  u6="block=ae14ce1a4ee29af53d5645f51bf0e97d#address-d3239ec6d067cd9381f137545720a6c9-ae14ce1a4ee29af53d5645f51bf0e97d"
  u51="endDate="
  u52=date_obj.day
  u53="%2F"
  u54=date_obj.month
  u55="%2F"
  u56=date_obj.year
  u57="&"
  u5=u51+ str(u52) + u53 + str(u54) + u55 + str(u56) + u57
  url2=u4+u5+u6
  data=pd.read_html(url2)
  data[0].iloc[0,1]
  b=[i for i in data[0].iloc[0,1]]
  c=b[0]+b[2]+b[3]+b[4]
  d=int(c)/100000
  # créer un DataFrame à partir des listes de données
  # créer un DataFrame à partir des listes de données
  TMP = pd.DataFrame({'Maturity': [1], 'Taux': [d]})
  df_concat1 = pd.concat([TMP, data2])
  df_concat1  = df_concat1.reset_index(drop=True) # Réinitialiser l'indexation à partir de 0
  # interpolation linéaire
  def interp(x_value):
      if (0 < x_value < 365) :
          f = interp1d(df_concat1["Maturity"],df_concat1['Taux'],kind="linear")
      elif x_value >= data3["Maturity"].max() : 
          f = interp1d(data3["Maturity"],data3['Taux'], fill_value="extrapolate" ,kind="linear") 
      else :
          f = interp1d(data3["Maturity"],data3['Taux'],kind="linear")
      return f(x_value)
  dt = {'Maturité standard': ["13w", "26w","52w", "1y","2y","3y","4y","5y","6y","7y","8y","9y","10y","11y","12y","13y","14y","15y","16y","17y","18y","19y","20y","21y","22y","23y","24y","25y","26y","27y","28y","29y","30y","31y"],'Maturité en jours':[91,182,364,365,730,1095,1460,1825,2190,2555,2920,3285,3650,4015,4380,4745,5110,5475,5840,6205,6570,6935,7300,7665,8030,8395,8760,9125,9490,9855,10220,10585,10950,11315]}
  data_tenors = pd.DataFrame(data=dt)
  result = np.vectorize(interp)(data_tenors["Maturité en jours"])
  data_tenors['Taux_rendement']= result
  data_tenors['Taux_rendement']=data_tenors['Taux_rendement']
  data_tenors['Taux_rendement'] = data_tenors['Taux_rendement'].apply(multiply_by_100)  
  TMP2 = pd.DataFrame({'Maturité standard':"1d",'Maturité en jours': [1], 'Taux_rendement': [d]})
  TMP2['Taux_rendement'] = TMP2['Taux_rendement'].apply(multiply_by_100)
  df_concat2 = pd.concat([TMP2, data_tenors])
  df_concat2  = df_concat2.reset_index(drop=True) # Réinitialiser l'indexation à partir de 0
  for i in range(len(df_concat2)):
    df_concat2.loc[i,'Fct_act']=(1/(1+(df_concat2.loc[i,'Taux_rendement']/100)*(df_concat2.loc[i,'Maturité en jours']/365)))
    df_concat2.loc[i,'Fct_captl']=(1+(df_concat2.loc[i,'Taux_rendement']/100)*(df_concat2.loc[i,'Maturité en jours']/365))  
  df_concat2['Taux_rendement']=df_concat2['Taux_rendement'].round(3)
  df_concat2['Fct_act']=df_concat2['Fct_act'].round(3)
  df_concat2['Fct_captl']=df_concat2['Fct_captl'].round(3)
  return df_concat2

def ecart(date1,date2):
  data1=taux_rendement(date1)
  data2=taux_rendement(date2)
  data_ecart=pd.DataFrame({'Maturity':data1['Maturité standard'],date1:data1['Taux_rendement'],date2:data2['Taux_rendement']})
  for i in range(len(data1)):
     data_ecart.loc[i,'Ecart']=((data1.loc[i,'Taux_rendement']/100)-(data2.loc[i,'Taux_rendement']/100))
  for i in range(len(data1)):
     data_ecart.loc[i,'Ecart en pd']=data_ecart.loc[i,'Ecart']/0.0001
  return data_ecart

def Interpolation(date_str,valeur): 
  x_value=float(valeur)  
  import datetime  
  date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
  u1="https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-secondaire/Taux-de-reference-des-bons-du-tresor?"
  #u2="date=24%2F02%2F2023&"
  u3="block=e1d6b9bbf87f86f8ba53e8518e882982#address-c3367fcefc5f524397748201aee5dab8-e1d6b9bbf87f86f8ba53e8518e882982"
  u21="date="
  u22=date_obj.day
  u23="%2F"
  u24=date_obj.month
  u25="%2F"
  u26=date_obj.year
  u27="&"
  u2=u21+ str(u22) + u23 + str(u24) + u25 + str(u26) + u27
  url=u1+u2+u3
  data1=pd.read_html(url)
  data1[0].drop(data1[0].index[-1], inplace=True)
  data1[0]["Maturité"] = pd.to_datetime(data1[0]["Date d'échéance"],format='%d/%m/%Y') - pd.to_datetime(data1[0]['Date de la valeur'],format='%d/%m/%Y')
  data1[0]["Maturité"] = data1[0]["Maturité"].dt.total_seconds().astype(float)/ (24 * 60 * 60)
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace('%','')
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace(',','.')
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].astype(float)/ (100)
  n=len(data1[0])
  L=[]
  for i in range(len(data1[0])):
    if data1[0]['Maturité'][i]<=365:
      L.append(i)
  indice1=L[-1]+1 
  l=[]
  for i in range(len(data1[0])):
    if data1[0]['Maturité'][i]>=365:
      l.append(i)
  indice2=l[0]-1
  # initialiser les listes de données
  x1_data = []
  x2_data = []
  # boucle for pour remplir les listes
  for i in range(indice1+1):
    x1_data.append(data1[0].iloc[i,2])
    x2_data.append(data1[0].iloc[i,4]) 
  # créer un DataFrame à partir des listes de données
  data2 = pd.DataFrame({'Maturity': x2_data, 'Taux': x1_data})
  # afficher le DataFrame
  a=(360/data2.iloc[indice1,0])*((1+data2.iloc[indice1,1])**(data2.iloc[indice1,0]/365)-1)
  data2.iloc[indice1,1]=a # taux monetaire
  # initialiser les listes de données
  x3_data = []
  x4_data = []
  # boucle for pour remplir les listes
  for i in range(indice2,n):
    x3_data.append(data1[0].iloc[i,2])
    x4_data.append(data1[0].iloc[i,4]) 
  # créer un DataFrame à partir des listes de données
  data3 = pd.DataFrame({'Maturity': x4_data, 'Taux': x3_data})
  # afficher le DataFrame
  b=((1+(data3.iloc[0,1]*(data3.iloc[0,0]/360)))**(365/data3.iloc[0,0]))-1
  data3.iloc[0,1]=b
  # TMP
  u4="https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Marche-monetaire-interbancaire?startDate=&"
  #u5="endDate=26%2F02%2F2023&"
  u6="block=ae14ce1a4ee29af53d5645f51bf0e97d#address-d3239ec6d067cd9381f137545720a6c9-ae14ce1a4ee29af53d5645f51bf0e97d"
  u51="endDate="
  u52=date_obj.day
  u53="%2F"
  u54=date_obj.month
  u55="%2F"
  u56=date_obj.year
  u57="&"
  u5=u51+ str(u52) + u53 + str(u54) + u55 + str(u56) + u57
  url2=u4+u5+u6
  data=pd.read_html(url2)
  data[0].iloc[0,1]
  b=[i for i in data[0].iloc[0,1]]
  c=b[0]+b[2]+b[3]+b[4]
  d=int(c)/100000
  # créer un DataFrame à partir des listes de données
  # créer un DataFrame à partir des listes de données
  TMP = pd.DataFrame({'Maturity': [1], 'Taux': [d]})
  df_concat1 = pd.concat([TMP, data2])
  df_concat1  = df_concat1.reset_index(drop=True) # Réinitialiser l'indexation à partir de 0
  # interpolation linéaire
  def interp(x_value):
      if (0 < x_value < 365) :
          f = interp1d(df_concat1["Maturity"],df_concat1['Taux'],kind="linear")
      elif x_value >= data3["Maturity"].max() : 
          f = interp1d(data3["Maturity"],data3['Taux'], fill_value="extrapolate" ,kind="linear") 
      else :
          f = interp1d(data3["Maturity"],data3['Taux'],kind="linear")
      return f(x_value)
  a=interp(x_value)
  return a  

def taux_ZC(date_str): 
  import datetime  
  date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
  u1="https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-secondaire/Taux-de-reference-des-bons-du-tresor?"
  #u2="date=24%2F02%2F2023&"
  u3="block=e1d6b9bbf87f86f8ba53e8518e882982#address-c3367fcefc5f524397748201aee5dab8-e1d6b9bbf87f86f8ba53e8518e882982"
  u21="date="
  u22=date_obj.day
  u23="%2F"
  u24=date_obj.month
  u25="%2F"
  u26=date_obj.year
  u27="&"
  u2=u21+ str(u22) + u23 + str(u24) + u25 + str(u26) + u27
  url=u1+u2+u3
  data1=pd.read_html(url)
  data1[0].drop(data1[0].index[-1], inplace=True)
  data1[0]["Maturité"] = pd.to_datetime(data1[0]["Date d'échéance"],format='%d/%m/%Y') - pd.to_datetime(data1[0]['Date de la valeur'],format='%d/%m/%Y')
  data1[0]["Maturité"] = data1[0]["Maturité"].dt.total_seconds().astype(float)/ (24 * 60 * 60)
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace('%','')
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace(',','.')
  data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].astype(float)/ (100)
  n=len(data1[0])
  L=[]
  for i in range(len(data1[0])):
    if data1[0]['Maturité'][i]<=365:
      L.append(i)
  indice1=L[-1]+1 
  l=[]
  for i in range(len(data1[0])):
    if data1[0]['Maturité'][i]>=365:
      l.append(i)
  indice2=l[0]-1
  # initialiser les listes de données
  x1_data = []
  x2_data = []
  # boucle for pour remplir les listes
  for i in range(indice1+1):
    x1_data.append(data1[0].iloc[i,2])
    x2_data.append(data1[0].iloc[i,4]) 
  # créer un DataFrame à partir des listes de données
  data2 = pd.DataFrame({'Maturity': x2_data, 'Taux': x1_data})
  # afficher le DataFrame
  a=(360/data2.iloc[indice1,0])*((1+data2.iloc[indice1,1])**(data2.iloc[indice1,0]/365)-1)
  data2.iloc[indice1,1]=a # taux monetaire
  # initialiser les listes de données
  x3_data = []
  x4_data = []
  # boucle for pour remplir les listes
  for i in range(indice2,n):
    x3_data.append(data1[0].iloc[i,2])
    x4_data.append(data1[0].iloc[i,4]) 
  # créer un DataFrame à partir des listes de données
  data3 = pd.DataFrame({'Maturity': x4_data, 'Taux': x3_data})
  # afficher le DataFrame
  b=((1+(data3.iloc[0,1]*(data3.iloc[0,0]/360)))**(365/data3.iloc[0,0]))-1
  data3.iloc[0,1]=b
  # TMP
  u4="https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Marche-monetaire-interbancaire?startDate=&"
  #u5="endDate=26%2F02%2F2023&"
  u6="block=ae14ce1a4ee29af53d5645f51bf0e97d#address-d3239ec6d067cd9381f137545720a6c9-ae14ce1a4ee29af53d5645f51bf0e97d"
  u51="endDate="
  u52=date_obj.day
  u53="%2F"
  u54=date_obj.month
  u55="%2F"
  u56=date_obj.year
  u57="&"
  u5=u51+ str(u52) + u53 + str(u54) + u55 + str(u56) + u57
  url2=u4+u5+u6
  data=pd.read_html(url2)
  data[0].iloc[0,1]
  b=[i for i in data[0].iloc[0,1]]
  c=b[0]+b[2]+b[3]+b[4]
  d=int(c)/100000
  # créer un DataFrame à partir des listes de données
  # créer un DataFrame à partir des listes de données
  TMP = pd.DataFrame({'Maturity': [1], 'Taux': [d]})
  df_concat1 = pd.concat([TMP, data2])
  df_concat1  = df_concat1.reset_index(drop=True) # Réinitialiser l'indexation à partir de 0
  # interpolation linéaire
  def interp(x_value):
      if (0 < x_value < 365) :
          f = interp1d(df_concat1["Maturity"],df_concat1['Taux'],kind="linear")
      elif x_value >= data3["Maturity"].max() : 
          f = interp1d(data3["Maturity"],data3['Taux'], fill_value="extrapolate" ,kind="linear") 
      else :
          f = interp1d(data3["Maturity"],data3['Taux'],kind="linear")
      return f(x_value)
  dt = {'Maturité_initiale': ["13w", "26w","52w", "1y","2y","3y","4y","5y","6y","7y","8y","9y","10y","11y","12y","13y","14y","15y","16y","17y","18y","19y","20y","21y","22y","23y","24y","25y","26y","27y","28y","29y","30y","31y"],'Maturité':[91,182,364,365,730,1095,1460,1825,2190,2555,2920,3285,3650,4015,4380,4745,5110,5475,5840,6205,6570,6935,7300,7665,8030,8395,8760,9125,9490,9855,10220,10585,10950,11315]}
  data_tenors = pd.DataFrame(data=dt)
  result = np.vectorize(interp)(data_tenors["Maturité"])
  data_tenors['Taux_rendement']= result
  data_tenors['Taux_rendement']=data_tenors['Taux_rendement']
  TMP2 = pd.DataFrame({'Maturité_initiale':"1d",'Maturité': [1], 'Taux_rendement': [d]})
  df_concat2 = pd.concat([TMP2, data_tenors])
  df_concat2  = df_concat2.reset_index(drop=True) # Réinitialiser l'indexation à partir de 0
  # Calcul des Taux ZC - Bootstrap
  for i in range(4):
    df_concat2.loc[i, 'Taux ZC']= ((1+(df_concat2.loc[i, 'Taux_rendement']*(df_concat2.loc[i, 'Maturité']/360)))**(365/df_concat2.loc[i, 'Maturité']))-1
  data_4lignes=df_concat2.head(4)
  #suprimer les 4 premieres lignes
  n = 4
  df_concat2 = df_concat2.drop(range(n))
  #prendere les colonnes qui nous interese dans le calcul
  colonne_nom = df_concat2['Taux_rendement']
  colonne_nom = colonne_nom.reset_index(drop=True)
  colonne_nom2=df_concat2['Maturité']
  colonne_nom2 = colonne_nom2.reset_index(drop=True)
  # calculons le zc par la methode de bootstrap
  def select_taux_ZC(maturite, data):
      # Récupération de l'indice de la maturité
      index = data.loc[data['Maturité'] == maturite].index[0]
    
      # Récupération des taux AC pour toutes les maturités inférieures à la maturité donnée
      taux_ZC = data.loc[:index-1, 'Taux ZC']
      return taux_ZC
  B = { 'Maturité_initiale': ["1y","2y","3y","4y","5y","6y","7y","8y","9y","10y","11y","12y","13y","14y","15y","16y","17y","18y","19y","20y","21y","22y","23y","24y","25y","26y","27y","28y","29y","30y","31y"],'Maturité':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] ,'Taux_rendement':colonne_nom}
  dta = pd.DataFrame(data=B)
  dta["Taux ZC"] = dta["Taux_rendement"]
  def Zc(maturité, Tx, dta):
    deno = 1
    taux_ZC = select_taux_ZC(maturité, dta)
    for i in range(len(taux_ZC)):
        deno = deno - (Tx / ((1 + taux_ZC.iloc[i])) ** (i+1))
    ZC = ((1 + Tx) / deno) ** (1 / maturité) - 1
    return ZC
  for i in range (1,len(dta)) :
    dta.loc[i,'Taux ZC']= Zc(dta.loc[i,'Maturité'],dta.loc[i,'Taux_rendement'],dta) 
  df_new = pd.concat([data_4lignes, dta], ignore_index=True)
  for i in range(4):
    df_new.iloc[i,1]=float(df_new.iloc[i,1])/365
  df_new.insert(loc=2, column="Maturité_jours", value=[1,91,182,364,365,730,1095,1460,1825,2190,2555,2920,3285,3650,4015,4380,4745,5110,5475,5840,6205,6570,6935,7300,7665,8030,8395,8760,9125,9490,9855,10220,10585,10950,11315])
  # La courbe ZC
  dataZC = pd.DataFrame({'Maturité standard': df_new["Maturité_initiale"] ,   'Maturity': df_new["Maturité_jours"], 'Taux ZC': df_new["Taux ZC"]})
  dataZC['Taux ZC'] = dataZC['Taux ZC'].apply(multiply_by_100)
  for i in range(len(dataZC)):
    dataZC.loc[i,'Fct_act']=(1/(1+(dataZC.loc[i,'Taux ZC']/100)*(dataZC.loc[i,'Maturity']/365)))
    dataZC.loc[i,'Fct_captl']=(1+(dataZC.loc[i,'Taux ZC']/100)*(dataZC.loc[i,'Maturity']/365))
  dataZC['Taux ZC']=dataZC['Taux ZC'].round(5)
  dataZC['Fct_act']=dataZC['Fct_act'].round(3)
  dataZC['Fct_captl']=dataZC['Fct_captl'].round(3)
  return dataZC


def ecart_ZC(date1, date2):
    try:
        data1 = taux_ZC(date1)
        data2 = taux_ZC(date2)
        
        if not all(data1['Maturité standard'] == data2['Maturité standard']):
            raise ValueError("Les maturités des deux dates ne correspondent pas")
            
        data_ecart = pd.DataFrame({
            'Maturity': data1['Maturité standard'],
            date1: data1['Taux ZC'],
            date2: data2['Taux ZC']
        })
        
        data_ecart['Ecart'] = data1['Taux ZC'] - data2['Taux ZC']
        data_ecart['Ecart en pd'] = data_ecart['Ecart'] / 0.0001
        
        return data_ecart
        
    except Exception as e:
        raise ValueError(f"Erreur dans ecart_ZC: {str(e)}")
    
def TMP(date_str):
  import datetime  
  date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()    
  u4="https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Marche-monetaire-interbancaire?startDate=&"
  #u5="endDate=26%2F02%2F2023&"
  u6="block=ae14ce1a4ee29af53d5645f51bf0e97d#address-d3239ec6d067cd9381f137545720a6c9-ae14ce1a4ee29af53d5645f51bf0e97d"
  u51="endDate="
  u52=date_obj.day
  u53="%2F"
  u54=date_obj.month
  u55="%2F"
  u56=date_obj.year
  u57="&"
  u5=u51+ str(u52) + u53 + str(u54) + u55 + str(u56) + u57
  url2=u4+u5+u6
  data=pd.read_html(url2)
  data[0].iloc[0,1]
  b=[i for i in data[0].iloc[0,1]]
  c=b[0]+b[2]+b[3]+b[4]
  d=int(c)/100000
  # créer un DataFrame à partir des listes de données
  # créer un DataFrame à partir des listes de données
  data = pd.DataFrame({'Maturity': [1], 'Taux': [d*100]})
  return data


#Historisation
def Telecharger_taux_rendements(date_str):
    import datetime  
    date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
    z=str(date_obj.day)+"_"+str(date_obj.month)+"_"+str(date_obj.year)
    z4="Taux_rendements" + "_"+ z + ".csv"
    data=taux_rendement(date_str)
    data.to_csv(z4, index=False)

#Récupération
def Récupérationr_taux_rendements(date_str):
    import datetime  
    date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
    z=str(date_obj.day)+"_"+str(date_obj.month)+"_"+str(date_obj.year)
    z4="Taux_rendements" + "_"+ z + ".csv"
    data=pd.read_csv(z4)
    return data


def plot_ecart(data, date1, date2):
    """Affiche deux courbes de taux pour deux dates, sans affichage des écarts."""
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick
    import streamlit as st

    # Style moderne
    plt.style.use('seaborn')

    fig, ax = plt.subplots(figsize=(10, 6))

    # Courbe 1
    ax.plot(data['Maturity'], data[date1],
            label=date1,
            linewidth=2,
            color='#1f77b4')

    # Courbe 2
    ax.plot(data['Maturity'], data[date2],
            label=date2,
            linewidth=2,
            color='#ff7f0e')

    # Titre et labels
    ax.set_title("Illustration", fontsize=14, pad=15)
    ax.set_xlabel("Maturity", fontsize=12)
    ax.set_ylabel("Taux en %", fontsize=12)

    # Format Y en pourcentage
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))

    # Grille et rotation
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=0)

    # Légende
    ax.legend(loc='upper left', frameon=True)

    # Mise en page propre
    plt.tight_layout()

    # Affichage dans Streamlit
    st.pyplot(fig)

    # Export optionnel
    if st.checkbox("Exporter ce graphique"):
        fig.savefig(f"courbes_taux_{date1}_{date2}.png", dpi=300, bbox_inches='tight')
        st.success(f"Graphique exporté sous courbes_taux_{date1}_{date2}.png")
    
# Chargement du fichier Excel
#uploaded_file = st.file_uploader("Importer le portefeuille", type=["xlsx"], 
                              #   key="portfolio_uploader",
                               #  help="Sélectionnez le fichier PF DE TRADING.xlsx")

@st.cache_data  # Cache pour éviter de recharger à chaque interaction
def load_portfolio(file_path):
    try:
        # Lecture de toutes les feuilles
        xls = pd.ExcelFile(file_path)
        sheets = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
        return sheets
    except Exception as e:
        st.error(f"Erreur de chargement : {str(e)}")
        return None

# Solution 1 : Chargement direct si chemin connu
portfolio_path = r"C:\Users\lenovo\Desktop\INTERFACE CDM\PF DE TRADING.xlsx"

from datetime import date

def diffdate(date1,date2):
  diff1 = date1-date2
  diffdate = int(diff1.days)
  return diffdate

def Date_coupon1(date_echeance, date_jouissance):
    nb2 = int(date_jouissance.year + (date_echeance.year - date_jouissance.year - 1))  # Ensure nb2 is an integer
    return date(nb2, date_echeance.month, date_echeance.day)

from numpy.core.multiarray import datetime_data
#return date jouissance
from numpy.core.multiarray import datetime_data
#return date jouissance
def date_jouissance(date_echeance,date_emission):
  date_jouissance=datetime.date(date_emission.year,date_echeance.month,date_echeance.day)
  return date_jouissance 

def Bond_price(date_emission, date_valeur, date_echeance, date_jouissance, Nominal, taux_facial, Spread):
    # Ensure all date inputs are datetime.date objects
    if not all(isinstance(d, date) for d in [date_emission, date_valeur, date_echeance, date_jouissance]):
        raise TypeError("All date inputs must be of type datetime.date")
    # Ensure numeric inputs are valid
    try:
        Nominal = float(Nominal)
        taux_facial = float(taux_facial)
        Spread = float(Spread)
    except ValueError:
        raise TypeError("Nominal, taux_facial, and Spread must be numeric")
    maturite_initiale = diffdate(date_echeance, date_emission)
    maturite_residuelle  = diffdate(date_echeance, date_valeur)
    taux_rendement = Interpolation(date_valeur.strftime("%d/%m/%Y"),maturite_residuelle) + Spread
    prochain_coupon = 0
    i = 1 # nb de coupon restants
    while date_echeance.replace(year=date_echeance.year - i) > date_valeur and date_echeance.replace(year=date_echeance.year - i) > date_jouissance:
        i = i + 1   
    from datetime import timedelta
    prochain_coupon = date_echeance.replace(year=date_echeance.year + 1- i)
    if date_valeur.year % 4 == 0 and (date_valeur.year % 100 != 0 or date_valeur.year % 400 == 0):
       A = 366
    else:
       A = 365   
    atypique = (date_emission != date_jouissance)
    if not atypique:
      if maturite_initiale <= 365:
        Bond_price = Nominal * ((1 + taux_facial * maturite_initiale / 360) / (1 + taux_rendement * maturite_residuelle / 360))
      elif maturite_residuelle <= 365:
        Bond_price = Nominal * ((1 + taux_facial) / (1 + taux_rendement * maturite_residuelle / 360))
      else:
        flux = 0
        for j in range(1, i+1):
           flux = flux + taux_facial / ((1 + taux_rendement) ** (j - 1))
        nj = diffdate(prochain_coupon, date_valeur)
        Bond_price = (Nominal * (flux + 1 / ((1 + taux_rendement) ** (i - 1)))) / ((1 + taux_rendement) ** (nj / A))
    else:
      ncoupon = date_echeance.year - date_jouissance.year
      if ncoupon == 1:
        if maturite_residuelle <= 365:
          Bond_price = (Nominal * (1 + taux_facial * maturite_initiale / A)) / (1 + taux_rendement * maturite_residuelle / 360)
        else:
          Bond_price = (Nominal * (1 + taux_facial * maturite_initiale / A)) / (1 + taux_rendement) ** (maturite_residuelle / A)
      else:
        prcoupon=Date_coupon1(date_echeance, date_jouissance)
        if date_valeur < prcoupon:
          flux = 0
          for j in range(2, i+1):
            flux = flux + taux_facial / ((1 + taux_rendement) ** (j - 1))
          nj = diffdate(prochain_coupon, date_valeur) / A
          Bond_price = flux + 1 / (1 + taux_rendement) ** (i - 1) + taux_facial * (diffdate(prcoupon,date_emission)) / A
          Bond_price = (Nominal * Bond_price) / (1 + taux_rendement)**nj
        else:
          flux = 0
          for j in range(1, i+1):
             flux += taux_facial / (1 + taux_rendement) ** (j - 1)
          flux += (1 / (1 + taux_rendement) ** (i - 1))
          nj = diffdate(prochain_coupon,date_valeur)
          Bond_price = Nominal * flux / ((1 + taux_rendement) ** (nj / A))
    return Bond_price

def Bond_price_Effet_niveau(date_emission , date_valeur , date_echeance , date_jouissance , Nominal , taux_facial, Spread ):
  import datetime
  date_emission = date_emission.to_pydatetime().date()
  date_echeance = date_echeance.to_pydatetime().date()
  date_jouissance = date_jouissance.to_pydatetime().date()
  #import datetime
  #date_emission = datetime.datetime.strptime(date_emission, "%d/%m/%Y").date()
  #date_valeur = datetime.datetime.strptime(date_valeur, "%d/%m/%Y").date()
  #date_echeance = datetime.datetime.strptime(date_echeance, "%d/%m/%Y").date()
  #date_jouissance = datetime.datetime.strptime(date_jouissance, "%d/%m/%Y").date()
  maturite_initiale = diffdate(date_echeance,date_emission)
  maturite_residuelle  = diffdate(date_echeance,date_valeur)
  taux_rendement = Interpolation("18/05/2023",maturite_residuelle) + Spread+0.00042002334994894726
  prochain_coupon = 0
  i = 1 # nb de coupon restants
  while date_echeance.replace(year=date_echeance.year - i) > date_valeur and date_echeance.replace(year=date_echeance.year - i) > date_jouissance:
      i = i + 1   
  from datetime import timedelta
  prochain_coupon = date_echeance.replace(year=date_echeance.year + 1- i)
  #print(prochain_coupon)
  #print(date_valeur)
  if date_valeur.year % 4 == 0 and (date_valeur.year % 100 != 0 or date_valeur.year % 400 == 0):
     A = 366
  else:
     A = 365   
  atypique = (date_emission != date_jouissance)
  if not atypique:
    if maturite_initiale <= 365:
    # Les maturités en jours
      Bond_price = Nominal * ((1 + taux_facial * maturite_initiale / 360) / (1 + taux_rendement * maturite_residuelle / 360))
    elif maturite_residuelle <= 365:
    # Cas normal
      Bond_price = Nominal * ((1 + taux_facial) / (1 + taux_rendement * maturite_residuelle / 360))
    else:
    # cas normal avec les deux maturités (initiale et residuelle) superieures à 1an
      flux = 0
      for j in range(1, i+1):
         flux = flux + taux_facial / ((1 + taux_rendement) ** (j - 1))
      nj = diffdate(prochain_coupon, date_valeur)
      Bond_price = (Nominal * (flux + 1 / ((1 + taux_rendement) ** (i - 1)))) / ((1 + taux_rendement) ** (nj / A))
  else:
    ncoupon = date_echeance.year - date_jouissance.year
    if ncoupon == 1:
      if maturite_residuelle <= 365:
        # Ligne posterieure à un seul flux
        Bond_price = (Nominal * (1 + taux_facial * maturite_initiale / A)) / (1 + taux_rendement * maturite_residuelle / 360)
      else:
        # Ca correspond à 1an + la duree qui s'est ecoulee entre l'emission et la date valeur
        Bond_price = (Nominal * (1 + taux_facial * maturite_initiale / A)) / (1 + taux_rendement) ** (maturite_residuelle / A)
    else:
      prcoupon=Date_coupon1(date_echeance, date_jouissance)
      if date_valeur < prcoupon:
        # on évalue avant le 1er coupon atypique
        flux = 0
        for j in range(2, i+1):
          flux = flux + taux_facial / ((1 + taux_rendement) ** (j - 1))
        nj = diffdate(prochain_coupon, date_valeur) / A
        Bond_price = flux + 1 / (1 + taux_rendement) ** (i - 1) + taux_facial * (diffdate(prcoupon,date_emission)) / A
        Bond_price = (Nominal * Bond_price) / (1 + taux_rendement)**nj
      else:
        # Initialisation des variables
        flux = 0
        # Boucle For
        for j in range(1, i+1):
           flux += taux_facial / (1 + taux_rendement) ** (j - 1)
        flux += (1 / (1 + taux_rendement) ** (i - 1))
        nj = diffdate(prochain_coupon,date_valeur)
        Bond_price = Nominal * flux / ((1 + taux_rendement) ** (nj / A))
        #print(nj)
  return Bond_price

def coupon_couru_unitaire(date_emission , date_valeur , date_echeance , date_jouissance , Nominal , taux_facial):
  import datetime
  date_emission = date_emission.to_pydatetime().date()
  date_echeance = date_echeance.to_pydatetime().date()
  date_jouissance = date_jouissance.to_pydatetime().date()  
  maturite_initiale = diffdate(date_echeance,date_emission)
  maturite_residuelle  = diffdate(date_echeance,date_valeur)
  prochain_coupon = 0
  i = 1 # nb de coupon restants
  while date_echeance.replace(year=date_echeance.year - i) > date_valeur and date_echeance.replace(year=date_echeance.year - i) > date_jouissance:
      i = i + 1   
  from datetime import timedelta
  prochain_coupon = date_echeance.replace(year=date_echeance.year + 1- i)
  #print(prochain_coupon)
  #print(date_valeur)
  if date_valeur.year % 4 == 0 and (date_valeur.year % 100 != 0 or date_valeur.year % 400 == 0):
     A = 366
  else:
     A = 365   
  atypique = (date_emission != date_jouissance)
  if not atypique:
    if maturite_initiale <= 365:
      ccu=taux_facial*Nominal*(maturite_initiale-maturite_residuelle)/360
    else:
      if maturite_residuelle < 365:
        ccu=taux_facial*Nominal*diffdate(date_valeur,prochain_coupon.replace(year=prochain_coupon.year - 1))/A
      else:
        if date_valeur <= Date_coupon1(date_echeance, date_jouissance):
          ccu=taux_facial*Nominal*(diffdate(date_valeur,date_emission)/A)
        else: 
          ccu=taux_facial*Nominal*diffdate(date_valeur,prochain_coupon.replace(year=prochain_coupon.year - 1))/A
  else:
    if maturite_initiale <= 365:
      if date_valeur <= date_jouissance:
         ccu=taux_facial*Nominal*(maturite_initiale-maturite_residuelle)/A
      else:
        ccu=taux_facial*Nominal*((diffdate(date_jouissance,date_emission)/A)+(diffdate(date_valeur,date_jouissance)/A))
    else:
      if maturite_residuelle<365:
        if i==1:
          ccu=taux_facial*Nominal*((diffdate(date_jouissance,date_emission)/A)+(diffdate(date_valeur,date_jouissance)/A))
        elif date_valeur >  Date_coupon1(date_echeance, date_jouissance):
           ccu=taux_facial*Nominal*diffdate(date_valeur,prochain_coupon.replace(year=prochain_coupon.year - 1))/A
      else:
        if date_valeur <= prochain_coupon:
          if date_valeur<= date_jouissance:
            ccu=taux_facial*Nominal*(diffdate(date_valeur,date_emission)/A)
          else:
            ccu=taux_facial*Nominal*((diffdate(date_jouissance,date_emission)/A)+(diffdate(date_valeur,date_jouissance)/A))
        else:
            ccu=taux_facial*Nominal*diffdate(date_valeur,prochain_coupon.replace(year=prochain_coupon.year - 1))/A 
  return ccu

def Bond_price_Effet_amortissement(date_emission , date_valeur , date_echeance , date_jouissance , Nominal , taux_facial, Spread ):
  import datetime
  date_emission = date_emission.to_pydatetime().date()
  date_echeance = date_echeance.to_pydatetime().date()
  date_jouissance = date_jouissance.to_pydatetime().date()
  #import datetime
  #date_emission = datetime.datetime.strptime(date_emission, "%d/%m/%Y").date()
  #date_valeur = datetime.datetime.strptime(date_valeur, "%d/%m/%Y").date()
  #date_echeance = datetime.datetime.strptime(date_echeance, "%d/%m/%Y").date()
  #date_jouissance = datetime.datetime.strptime(date_jouissance, "%d/%m/%Y").date()
  maturite_initiale = diffdate(date_echeance,date_emission)
  maturite_residuelle  = diffdate(date_echeance,date_valeur)
  taux_rendement = Interpolation("18/05/2023",maturite_residuelle) + Spread
  prochain_coupon = 0
  i = 1 # nb de coupon restants
  while date_echeance.replace(year=date_echeance.year - i) > date_valeur and date_echeance.replace(year=date_echeance.year - i) > date_jouissance:
      i = i + 1   
  from datetime import timedelta
  prochain_coupon = date_echeance.replace(year=date_echeance.year + 1- i)
  #print(prochain_coupon)
  #print(date_valeur)
  if date_valeur.year % 4 == 0 and (date_valeur.year % 100 != 0 or date_valeur.year % 400 == 0):
     A = 366
  else:
     A = 365   
  atypique = (date_emission != date_jouissance)
  if not atypique:
    if maturite_initiale <= 365:
    # Les maturités en jours
      Bond_price = Nominal * ((1 + taux_facial * maturite_initiale / 360) / (1 + taux_rendement * maturite_residuelle / 360))
    elif maturite_residuelle <= 365:
    # Cas normal
      Bond_price = Nominal * ((1 + taux_facial) / (1 + taux_rendement * maturite_residuelle / 360))
    else:
    # cas normal avec les deux maturités (initiale et residuelle) superieures à 1an
      flux = 0
      for j in range(1, i+1):
         flux = flux + taux_facial / ((1 + taux_rendement) ** (j - 1))
      nj = diffdate(prochain_coupon, date_valeur)
      Bond_price = (Nominal * (flux + 1 / ((1 + taux_rendement) ** (i - 1)))) / ((1 + taux_rendement) ** (nj / A))
  else:
    ncoupon = date_echeance.year - date_jouissance.year
    if ncoupon == 1:
      if maturite_residuelle <= 365:
        # Ligne posterieure à un seul flux
        Bond_price = (Nominal * (1 + taux_facial * maturite_initiale / A)) / (1 + taux_rendement * maturite_residuelle / 360)
      else:
        # Ca correspond à 1an + la duree qui s'est ecoulee entre l'emission et la date valeur
        Bond_price = (Nominal * (1 + taux_facial * maturite_initiale / A)) / (1 + taux_rendement) ** (maturite_residuelle / A)
    else:
      prcoupon=Date_coupon1(date_echeance, date_jouissance)
      if date_valeur < prcoupon:
        # on évalue avant le 1er coupon atypique
        flux = 0
        for j in range(2, i+1):
          flux = flux + taux_facial / ((1 + taux_rendement) ** (j - 1))
        nj = diffdate(prochain_coupon, date_valeur) / A
        Bond_price = flux + 1 / (1 + taux_rendement) ** (i - 1) + taux_facial * (diffdate(prcoupon,date_emission)) / A
        Bond_price = (Nominal * Bond_price) / (1 + taux_rendement)**nj
      else:
        # Initialisation des variables
        flux = 0
        # Boucle For
        for j in range(1, i+1):
           flux += taux_facial / (1 + taux_rendement) ** (j - 1)
        flux += (1 / (1 + taux_rendement) ** (i - 1))
        nj = diffdate(prochain_coupon,date_valeur)
        Bond_price = Nominal * flux / ((1 + taux_rendement) ** (nj / A))
        #print(nj)
  return Bond_price


import streamlit as st
from datetime import datetime, date
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy.interpolate import interp1d
import math

# Titre principal
#st.title("My Application")
#st.markdown("---")

# Sidebar pour la navigation
#page = st.sidebar.radio("Navigation", ["Courbe", "Pricer","P&L"])

import streamlit as st
from PIL import Image
import os

# Chemin vers votre logo
logo_path = "credit-du-maroc-seeklogo.png"
# Vérification que le fichier existeg
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    
    # Création d'une mise en page avec colonnes
    col1, col2 = st.columns([4, 4])
    
    with col1:
        st.image(logo, width=200)  # Ajustez la largeur selon vos besoins
    
    with col2:
        st.title("My Application")
    
    st.markdown("---")
else:
    st.warning("Logo non trouvé au chemin spécifié")
    st.title("My Application")
    st.markdown("---")

# Sidebar pour la navigation
page = st.sidebar.radio("Navigation", ["Courbe", "Pricer", "P&L"])


# Page Courbe
if page == "Courbe":
    st.header("La courbe")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_date = st.date_input("Entrer la date J/M/A", datetime.now(), key="selected_date")
        maturite = st.number_input("Maturité", value=1, key="maturite")
        
        if st.button("Importer la courbe de la BAM"):
            data = data1(selected_date.strftime('%d/%m/%Y'))
            st.dataframe(data)
            
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            if st.button("Afficher CT"):
                st.dataframe(court_terme(selected_date.strftime('%d/%m/%Y')))
            if st.button("Afficher LT"):
                st.dataframe(long_terme(selected_date.strftime('%d/%m/%Y')))
            if st.button("Afficher TMP"):
                st.dataframe(TMP(selected_date.strftime('%d/%m/%Y')))
                
        with col1_2:
            if st.button("Télécharger CT"):
                data = court_terme(selected_date.strftime('%d/%m/%Y'))
                data.to_csv(f"Court_terme_{selected_date.day}_{selected_date.month}_{selected_date.year}.csv")
                st.success("Fichier téléchargé!")
            if st.button("Télécharger LT"):
                data = long_terme(selected_date.strftime('%d/%m/%Y'))
                data.to_csv(f"Long_terme_{selected_date.day}_{selected_date.month}_{selected_date.year}.csv")
                st.success("Fichier téléchargé!")
            if st.button("Télécharger TMP"):
                data = TMP(selected_date.strftime('%d/%m/%Y'))
                data.to_csv(f"TMP_{selected_date.day}_{selected_date.month}_{selected_date.year}.csv")
                st.success("Fichier téléchargé!")
    
    with col2:
        if st.button("Afficher courbe de rendement"):
            st.dataframe(taux_rendement(selected_date.strftime('%d/%m/%Y')))
            
        if st.button("Télécharger Taux rendement"):
            data = taux_rendement(selected_date.strftime('%d/%m/%Y'))
            data.to_csv(f"Taux_rendements_{selected_date.day}_{selected_date.month}_{selected_date.year}.csv")
            st.success("Fichier téléchargé!")
            
        if st.button("Afficher courbe zéro coupon"):
            st.dataframe(taux_ZC(selected_date.strftime('%d/%m/%Y')))
            
        if st.button("Télécharger Taux ZC"):
            data = taux_ZC(selected_date.strftime('%d/%m/%Y'))
            data.to_csv(f"ZC_{selected_date.day}_{selected_date.month}_{selected_date.year}.csv")
            st.success("Fichier téléchargé!")
            
        if st.button("Interpolation"):
            taux = Interpolation(selected_date.strftime('%d/%m/%Y'), maturite)
            st.write(f"Date de valeur :{selected_date}")
            st.write(f"maturité :{maturite}")
            st.write(f"Taux interpolé: {taux:.4%}")
    
    # Visualisation graphique
    if st.button("Visualisation graphiques"):
        fig, ax = plt.subplots()
        data_zc = taux_ZC(selected_date.strftime('%d/%m/%Y')).iloc[[0,5,10,15,20,25,30]]
        data_rend = taux_rendement(selected_date.strftime('%d/%m/%Y')).iloc[[0,5,10,15,20,25,30]]
        
        ax.plot(data_zc["Maturité standard"], data_zc['Taux ZC'], label='Taux ZC')
        ax.plot(data_rend["Maturité standard"], data_rend['Taux_rendement'], label='Taux de rendements')
        ax.set_title("Taux ZC et taux de rendements")
        ax.set_xlabel("Maturité")
        ax.set_ylabel("Taux (%)")
        ax.legend()
        st.pyplot(fig)
    
    # Graphe comparatif
    # Graphe comparatif
    if st.button("Graphe comparatif"):
      st.session_state.show_comparison = True

    if st.session_state.get('show_comparison', False):
     date1 = st.date_input("Date 1", datetime.now(), key="date1")
     date2 = st.date_input("Date 2", datetime.now(), key="date2")
    
    if st.button("Afficher", key="afficher"):
        fig, ax = plt.subplots()
        data1 = taux_rendement(date1.strftime('%d/%m/%Y')).iloc[[0,5,10,15,20,25,30]]
        data2 = taux_rendement(date2.strftime('%d/%m/%Y')).iloc[[0,5,10,15,20,25,30]]
        
        ax.plot(data1["Maturité standard"], data1['Taux_rendement'], label=date1.strftime('%d/%m/%Y'))
        ax.plot(data2["Maturité standard"], data2['Taux_rendement'], label=date2.strftime('%d/%m/%Y'))
        ax.set_title("Graphe comparatif des taux de rendements")
        ax.set_xlabel("Maturité")
        ax.set_ylabel("Taux (%)")
        ax.legend()
        st.pyplot(fig)
            
        if st.button("Ecart"):
                st.dataframe(ecart(date1.strftime('%d/%m/%Y'), date2.strftime('%d/%m/%Y')))

# Page Pricer
elif page == "Pricer":
    st.header("Valorisation")
    
    # Caractéristiques de l'obligation
    st.subheader("Caractéristique de l'obligation")
    
    date_valeur = st.date_input("Date de valeur", datetime.now(), key="date_valeur")
    date_jouissance = st.date_input("Date de jouissance", datetime.now(), key="date_jouissance")
    date_emission = st.date_input("Date d'émission", datetime.now(), key="date_emission")
    date_echeance = st.date_input("Date d'échéance", datetime.now(), key="date_echeance")
    
    nominal = st.number_input("Nominal", value=100000.0, key="nominal")
    taux_facial = st.number_input("Taux facial", value=0.000,format="%.4f",step=0.0001, key="taux_facial")
    spread = st.number_input("Spread", value=0.0, key="spread")
    
    # Type d'obligation
    option = st.radio("Type d'obligation", 
                     ["In fine à taux fixe", 
                      "Amortissement constant", 
                      "Annuité constante", 
                      "Taux variable", 
                      "Taux révisable"], key="obligation_type")
    
    
       
    import datetime
    def diffdate(date1,date2):
         diff1 = date1-date2
         diffdate = int(diff1.days)
         return diffdate
     
    def Date_coupon1(date_echeance, date_jouissance):
       nbcoupon= date_echeance.year-date_jouissance.year
       nb2= date_echeance.year + (1-nbcoupon)
       Date_coupon1=datetime.date(nb2,date_echeance.month,date_echeance.day)
       return Date_coupon1
    
    # Rename the date_jouissance function to avoid conflict
    def calculate_date_jouissance(date_echeance, date_emission):
        return datetime.date(date_emission.year, date_echeance.month, date_echeance.day)
  
  
    def prix_Dirty(date_valeur, date_emission, date_echeance, date_jouissance, nominal, taux_facial, spread):
      # Remove redundant imports
      import pandas as pd
      import math 
      import numpy as np 
      from datetime import date, timedelta, datetime
      import matplotlib.pyplot as plt 
      import matplotlib.dates as mdates
      from scipy.interpolate import interp1d

      date_str = date_valeur.strftime('%d/%m/%Y')
      date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()
      # Autres calculs à effectuer
      u1="https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-obligataire/Marche-des-bons-de-tresor/Marche-secondaire/Taux-de-reference-des-bons-du-tresor?"
      #u2="date=24%2F02%2F2023&"
      u3="block=e1d6b9bbf87f86f8ba53e8518e882982#address-c3367fcefc5f524397748201aee5dab8-e1d6b9bbf87f86f8ba53e8518e882982"
      u21="date="
      u22=date_obj.day
      u23="%2F"
      u24=date_obj.month
      u25="%2F"
      u26=date_obj.year
      u27="&"
      u2=u21+ str(u22) + u23 + str(u24) + u25 + str(u26) + u27
      url=u1+u2+u3
      data1=pd.read_html(url)
      data1[0].drop(data1[0].index[-1], inplace=True)
      data1[0]["Maturité"] = pd.to_datetime(data1[0]["Date d'échéance"],format='%d/%m/%Y') - pd.to_datetime(data1[0]['Date de la valeur'],format='%d/%m/%Y')
      data1[0]["Maturité"] = data1[0]["Maturité"].dt.total_seconds().astype(float)/ (24 * 60 * 60)
      data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace('%','')
      data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].str.replace(',','.')
      data1[0]["Taux moyen pondéré"] = data1[0]["Taux moyen pondéré"].astype(float)/ (100)
      n=len(data1[0])
      L=[]
      for i in range(len(data1[0])):
        if data1[0]['Maturité'][i]<=365:
          L.append(i)
      indice1=L[-1]+1 
      l=[]
      for i in range(len(data1[0])):
        if data1[0]['Maturité'][i]>=365:
          l.append(i)
      indice2=l[0]-1
      # initialiser les listes de données
      x1_data = []
      x2_data = []
      # boucle for pour remplir les listes
      for i in range(indice1+1):
        x1_data.append(data1[0].iloc[i,2])
        x2_data.append(data1[0].iloc[i,4]) 
      # créer un DataFrame à partir des listes de données
      data2 = pd.DataFrame({'Maturity': x2_data, 'Taux': x1_data})
      # afficher le DataFrame
      a=(360/data2.iloc[indice1,0])*((1+data2.iloc[indice1,1])**(data2.iloc[indice1,0]/365)-1)
      data2.iloc[indice1,1]=a # taux monetaire
      # initialiser les listes de données
      x3_data = []
      x4_data = []
      # boucle for pour remplir les listes
      for i in range(indice2,n):
        x3_data.append(data1[0].iloc[i,2])
        x4_data.append(data1[0].iloc[i,4]) 
      # créer un DataFrame à partir des listes de données
      data3 = pd.DataFrame({'Maturity': x4_data, 'Taux': x3_data})
      # afficher le DataFrame
      b=((1+(data3.iloc[0,1]*(data3.iloc[0,0]/360)))**(365/data3.iloc[0,0]))-1
      data3.iloc[0,1]=b
      # TMP
      u4="https://www.bkam.ma/Marches/Principaux-indicateurs/Marche-monetaire/Marche-monetaire-interbancaire?startDate=&"
      #u5="endDate=26%2F02%2F2023&"
      u6="block=ae14ce1a4ee29af53d5645f51bf0e97d#address-d3239ec6d067cd9381f137545720a6c9-ae14ce1a4ee29af53d5645f51bf0e97d"
      u51="endDate="
      u52=date_obj.day
      u53="%2F"
      u54=date_obj.month
      u55="%2F"
      u56=date_obj.year
      u57="&"
      u5=u51+ str(u52) + u53 + str(u54) + u55 + str(u56) + u57
      url2=u4+u5+u6
      data=pd.read_html(url2)
      data[0].iloc[0,1]
      b=[i for i in data[0].iloc[0,1]]
      c=b[0]+b[2]+b[3]+b[4]
      d=int(c)/100000
      # créer un DataFrame à partir des listes de données
      # créer un DataFrame à partir des listes de données
      TMP = pd.DataFrame({'Maturity': [1], 'Taux': [d]})
      df_concat1 = pd.concat([TMP, data2])
      df_concat1  = df_concat1.reset_index(drop=True) # Réinitialiser l'indexation à partir de 0
      
      def interp(x_value):
          if (0 < x_value < 365) :
              f = interp1d(df_concat1["Maturity"],df_concat1['Taux'],kind="linear")
          elif x_value >= data3["Maturity"].max() : 
              f = interp1d(data3["Maturity"],data3['Taux'], fill_value="extrapolate" ,kind="linear") 
          else :
              f = interp1d(data3["Maturity"],data3['Taux'],kind="linear")
          return f(x_value)
      
      dt = {'Maturité_initiale': ["13w", "26w","52w", "1y","2y","3y","4y","5y","6y","7y","8y","9y","10y","11y","12y","13y","14y","15y","16y","17y","18y","19y","20y","21y","22y","23y","24y","25y","26y","27y","28y","29y","30y","31y"],'Maturité':[91,182,364,365,730,1095,1460,1825,2190,2555,2920,3285,3650,4015,4380,4745,5110,5475,5840,6205,6570,6935,7300,7665,8030,8395,8760,9125,9490,9855,10220,10585,10950,11315]}
      data_tenors = pd.DataFrame(data=dt)
      result = np.vectorize(interp)(data_tenors["Maturité"])
      data_tenors['Taux_rendement']= result
      data_tenors['Taux_rendement']=data_tenors['Taux_rendement']
      TMP2 = pd.DataFrame({'Maturité_initiale':"1d",'Maturité': [1], 'Taux_rendement': [d]})
      df_concat2 = pd.concat([TMP2, data_tenors])
      df_concat2  = df_concat2.reset_index(drop=True) # Réinitialiser l'indexation à partir de 0
      # Calcul des Taux ZC - Bootstrap
      for i in range(4):
        df_concat2.loc[i, 'Taux ZC']= ((1+(df_concat2.loc[i, 'Taux_rendement']*(df_concat2.loc[i, 'Maturité']/360)))**(365/df_concat2.loc[i, 'Maturité']))-1
      data_4lignes=df_concat2.head(4)
      #suprimer les 4 premieres lignes
      n = 4
      df_concat2 = df_concat2.drop(range(n))
      #prendere les colonnes qui nous interese dans le calcul
      colonne_nom = df_concat2['Taux_rendement']
      colonne_nom = colonne_nom.reset_index(drop=True)
      colonne_nom2=df_concat2['Maturité']
      colonne_nom2 = colonne_nom2.reset_index(drop=True)
      # calculons le zc par la methode de bootstrap
      def select_taux_ZC(maturite, data):
          # Récupération de l'indice de la maturité
          index = data.loc[data['Maturité'] == maturite].index[0]
          # Récupération des taux AC pour toutes les maturités inférieures à la maturité donnée
          taux_ZC = data.loc[:index-1, 'Taux ZC']
          return taux_ZC
      B = { 'Maturité_initiale': ["1y","2y","3y","4y","5y","6y","7y","8y","9y","10y","11y","12y","13y","14y","15y","16y","17y","18y","19y","20y","21y","22y","23y","24y","25y","26y","27y","28y","29y","30y","31y"],'Maturité':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] ,'Taux_rendement':colonne_nom}
      dta = pd.DataFrame(data=B)
      dta["Taux ZC"] = dta["Taux_rendement"]
      def Zc(maturité, Tx, dta):
        deno = 1
        taux_ZC = select_taux_ZC(maturité, dta)
        for i in range(len(taux_ZC)):
            deno = deno - (Tx / ((1 + taux_ZC.iloc[i])) ** (i+1))
        ZC = ((1 + Tx) / deno) ** (1 / maturité) - 1
        return ZC
      for i in range (1,len(dta)) :
        dta.loc[i,'Taux ZC']= Zc(dta.loc[i,'Maturité'],dta.loc[i,'Taux_rendement'],dta)
      df_new = pd.concat([data_4lignes, dta], ignore_index=True)
      for i in range(4):
        df_new.iloc[i,1]=float(df_new.iloc[i,1])/365
      df_new
      df_new.insert(loc=2, column="Maturité_jours", value=[1,91,182,364,365,730,1095,1460,1825,2190,2555,2920,3285,3650,4015,4380,4745,5110,5475,5840,6205,6570,6935,7300,7665,8030,8395,8760,9125,9490,9855,10220,10585,10950,11315])
      dataZC = pd.DataFrame({'Maturité_initiale': df_new["Maturité_initiale"] ,   'Maturity': df_new["Maturité_jours"], 'TauxZC': df_new["Taux ZC"]})
      
      # Interpolation ZC
      def interpZC(x_value):
          f = interp1d(dataZC["Maturity"],dataZC['TauxZC'],kind="linear")
          return f(x_value) 
      
      def Bond_price(date_emission , date_echeance , date_jouissance,date_valeur , Nominal , taux_facial, Spread, point_base ):
        maturite_initiale = diffdate(date_echeance,date_emission)
        maturite_residuelle  = diffdate(date_echeance,date_valeur)
        taux_rendement = interp(maturite_residuelle)+point_base + Spread
        prochain_coupon = 0
        if not isinstance(date_valeur, date):
          raise TypeError("date_valeur doit être un objet datetime.date")
    
   
        i = 1 # nb de coupon restants
        while date_echeance.replace(year=date_echeance.year - i) > date_valeur and date_echeance.replace(year=date_echeance.year - i) > date_jouissance:
            i = i + 1    
        from datetime import timedelta
        prochain_coupon = date_echeance.replace(year=date_echeance.year + 1- i)
        #print(prochain_coupon)
        #print(date_valeur)
        if date_valeur.year % 4 == 0 and (date_valeur.year % 100 != 0 or date_valeur.year % 400 == 0):
           A = 366
        else:
           A = 365   
        atypique = (date_emission != date_jouissance)
        if not atypique:
          if maturite_initiale <= 365:
          # Les maturités en jours
            Bond_price = Nominal * ((1 + taux_facial * maturite_initiale / 360) / (1 + taux_rendement * maturite_residuelle / 360))
          elif maturite_residuelle <= 365:
          # Cas normal
            Bond_price = Nominal * ((1 + taux_facial) / (1 + taux_rendement * maturite_residuelle / 360))
          else:
          # cas normal avec les deux maturités (initiale et residuelle) superieures à 1an
            flux = 0
            for j in range(1, i+1):
               flux = flux + taux_facial / ((1 + taux_rendement) ** (j - 1))
            nj = diffdate(prochain_coupon, date_valeur)
            Bond_price = (Nominal * (flux + 1 / ((1 + taux_rendement) ** (i - 1)))) / ((1 + taux_rendement) ** (nj / A))
        else:
          ncoupon = date_echeance.year - calculate_date_jouissance(date_echeance, date_emission).year
          if ncoupon == 1:
            if maturite_residuelle <= 365:
              # Ligne posterieure à un seul flux
              Bond_price = (Nominal * (1 + taux_facial * maturite_initiale / A)) / (1 + taux_rendement * maturite_residuelle / 360)
            else:
              # Ca correspond à 1an + la duree qui s'est ecoulee entre l'emission et la date valeur
              Bond_price = (Nominal * (1 + taux_facial * maturite_initiale / A)) / (1 + taux_rendement) ** (maturite_residuelle / A)
          else:
            prcoupon=Date_coupon1(date_echeance, calculate_date_jouissance(date_echeance, date_emission))
            if date_valeur < prcoupon:
              # on évalue avant le 1er coupon atypique
              flux = 0
              for j in range(2, i+1):
                flux = flux + taux_facial / ((1 + taux_rendement) ** (j - 1))
              nj = diffdate(prochain_coupon, date_valeur) / A
              Bond_price = flux + 1 / (1 + taux_rendement) ** (i - 1) + taux_facial * (diffdate(prcoupon,date_emission)) / A
              Bond_price = (Nominal * Bond_price) / (1 + taux_rendement)**nj
            else:
              # Initialisation des variables
              flux = 0
              # Boucle For
              for j in range(1, i+1):
                 flux += taux_facial / (1 + taux_rendement) ** (j - 1)
              flux += (1 / (1 + taux_rendement) ** (i - 1))
              nj = diffdate(prochain_coupon,date_valeur)
              Bond_price = Nominal * flux / ((1 + taux_rendement) ** (nj / A))
              #print(nj)
        return Bond_price
      def coupon_couru_unitaire(date_emission , date_valeur , date_echeance , date_jouissance , Nominal , taux_facial):
        maturite_initiale = diffdate(date_echeance,date_emission)
        maturite_residuelle  = diffdate(date_echeance,date_valeur)
        prochain_coupon = 0
        i = 1 # nb de coupon restants
        while date_echeance.replace(year=date_echeance.year - i) > date_valeur and date_echeance.replace(year=date_echeance.year - i) > date_jouissance:
            i = i + 1   
        from datetime import timedelta
        prochain_coupon = date_echeance.replace(year=date_echeance.year + 1- i)
        #print(prochain_coupon)
        #print(date_valeur)
        if date_valeur.year % 4 == 0 and (date_valeur.year % 100 != 0 or date_valeur.year % 400 == 0):
           A = 366
        else:
           A = 365   
        atypique = (date_emission != date_jouissance)
        if not atypique:
          if maturite_initiale <= 365:
            ccu=taux_facial*Nominal*(maturite_initiale-maturite_residuelle)/360
          else:
            if maturite_residuelle < 365:
              ccu=taux_facial*Nominal*diffdate(date_valeur,prochain_coupon.replace(year=prochain_coupon.year - 1))/A
            else:
              if date_valeur <= Date_coupon1(date_echeance, calculate_date_jouissance(date_echeance, date_emission)):
                ccu=taux_facial*Nominal*(diffdate(date_valeur,date_emission)/A)
              else: 
                ccu=taux_facial*Nominal*diffdate(date_valeur,prochain_coupon.replace(year=prochain_coupon.year - 1))/A
        else:
          if maturite_initiale <= 365:
            if date_valeur <= date_jouissance:
               ccu=taux_facial*Nominal*(maturite_initiale-maturite_residuelle)/A
            else:
              ccu=taux_facial*Nominal*((diffdate(date_jouissance,date_emission)/A)+(diffdate(date_valeur,date_jouissance)/A))
          else:
            if maturite_residuelle<365:
              if i==1:
                ccu=taux_facial*Nominal*((diffdate(date_jouissance,date_emission)/A)+(diffdate(date_valeur,date_jouissance)/A))
              elif date_valeur >  Date_coupon1(date_echeance, calculate_date_jouissance(date_echeance, date_emission)):
                 ccu=taux_facial*Nominal*diffdate(date_valeur,prochain_coupon.replace(year=prochain_coupon.year - 1))/A
            else:
              if date_valeur <= prochain_coupon:
                if date_valeur<= date_jouissance:
                  ccu=taux_facial*Nominal*(diffdate(date_valeur,date_emission)/A)
                else:
                  ccu=taux_facial*Nominal*((diffdate(date_jouissance,date_emission)/A)+(diffdate(date_valeur,date_jouissance)/A))
              else:
                  ccu=taux_facial*Nominal*diffdate(date_valeur,prochain_coupon.replace(year=prochain_coupon.year - 1))/A 
        return ccu

      def Duration_in_fine(date_emission , date_valeur , date_echeance , date_jouissance , Nominal , taux_facial, Spread ):
        i = 1 # nb de coupon restants
        while date_echeance.replace(year=date_echeance.year - i) > date_valeur and date_echeance.replace(year=date_echeance.year - i) > date_jouissance:
            i = i + 1 
        k = 0 # nb de coupon passé
        while calculate_date_jouissance(date_echeance, date_emission).replace(year=calculate_date_jouissance(date_echeance, date_emission).year + k) < date_valeur:
          k += 1
        Nc = i
        from datetime import timedelta
        Dp = date_echeance.replace(year=date_echeance.year + 1- i)
        Da = Dp.replace(year=Dp.year -1)
        n = Nominal
        Tn = taux_facial
        Sp = Spread
        Dem = date_emission
        Dj = calculate_date_jouissance(date_echeance, date_emission)
        Dec = date_echeance
        Dv = date_valeur
        Mr =diffdate(Dec,Dv)
        taux_rendement=interp(Mr)
        Ta = taux_rendement
        M =diffdate(Dec,Dem)
        Ma = M / 365
        Cp = n * Tn
        f = diffdate(Dp,Dv) / diffdate(Dp,Da)
        #Cas de la maturité initiale inférieure à un an
        if M <= 365:
          p = (n * ((1 + Tn) * M / 360)) / (1 + (Ta * (Mr / 360)))
          D = (n * ((1 + Tn) * M / 360)) / (1 + (Ta * (Mr / 360))) * (Mr / 360)
        # Cas de la maturité initiale supérieure à un an
        if M > 365:
          if Mr <= 365:
              Cp = n * Tn * (M / 365)
              p = (n + Cp) / (1 + (Ta * (Mr / 360)))
              D = (n + Cp) / (1 + (Ta * (Mr / 360))) * (Mr / 360)

          # Cas de la maturité résiduelle supérieure à un an
          if Mr > 365:

              # Cas des lignes atypiques
              if Dem != Dj:
                  if Ma - Nc < 2:
                      Cp = n * Tn * (diffdate( Dj.replace(year=Dj.year + 1) , Dem) / 365)

              v = 0
              p=0
              D=0
              while v <= Nc - 2:
                  p = p + (Cp / ((1 + Ta + Sp) ** (f + v)))
                  D = D + (f + v) * ((Cp / ((1 + Ta + Sp) ** (f + v))))
                  v = v + 1
                  Cp = n * Tn

              p = p + (n * (1 + Tn)) / ((1 + Ta + Sp) ** (f + (Nc - 1)))
              D = D + (f + (Nc - 1)) * (n * (1 + Tn)) / ((1 + Ta + Sp) ** (f + (Nc - 1)))
        return D/p 

      def Bond_price_Amortissable(date_emission , date_valeur , date_echeance , date_jouissance , Nominal , taux_facial, Spread ):
            maturite_initiale = diffdate(date_echeance,date_emission)
            maturite_residuelle  = diffdate(date_echeance,date_valeur)
            prochain_coupon = 0
            i = 1 # nb de coupon restants
            while date_echeance.replace(year=date_echeance.year - i) > date_valeur and date_echeance.replace(year=date_echeance.year - i) > date_jouissance:
                i = i + 1   
            from datetime import timedelta
            prochain_coupon = date_echeance.replace(year=date_echeance.year + 1- i)
            ncoupon = (date_echeance.year - calculate_date_jouissance(date_echeance, date_emission).year)
            N=Nominal
            tf=taux_facial
            if date_valeur.year % 4 == 0 and (date_valeur.year % 100 != 0 or date_valeur.year % 400 == 0):
               A = 366
            else:
               A = 365
            Amortissement=[]  
            for j in range(ncoupon):
              Amortissement.append(N/ncoupon)
            Reste_a_rembourser=[]
            for j in range(ncoupon):
              Reste_a_rembourser.append(N - j*Amortissement[j])
            Interets=[]   
            for j in range(ncoupon):
              Interets.append(Reste_a_rembourser[j]*tf)
            flux=[]   
            for j in range(ncoupon):   
              flux.append(Interets[j]+Amortissement[j])
            M=[]
            for j in range(ncoupon):
               M_j= diffdate(calculate_date_jouissance(date_echeance, date_emission).replace(year=calculate_date_jouissance(date_echeance, date_emission).year +j+1),date_valeur)
               M.append(M_j)
            ZC=[] 
            for j in range(ncoupon):
              if M[j]<1:
                ZC.append("NaN")
              else:
                ZC_j= interpZC(M[j])
                ZC.append(ZC_j)  
            Date_coupon=[]
            for j in range(ncoupon): 
              Date_coupon.append(calculate_date_jouissance(date_echeance, date_emission).replace(year=calculate_date_jouissance(date_echeance, date_emission).year +j+1))
            facteur_actualisation=[]
            for j in range(ncoupon):
              if M[j]<1:
                facteur_actualisation.append("NaN")
              else:
                facteur_actualisation.append((1+ZC[j]+Spread)**(-M[j]/A))
            flux_actualiser=[]
            for j in range(ncoupon):
              if M[j]<1:
                flux_actualiser.append("NaN")
              else:
                flux_actualiser.append(flux[j]*facteur_actualisation[j])
            s=0
            for j in range(ncoupon):
              if flux_actualiser[j] != "NaN": 
                s+=flux_actualiser[j]

            Duration_Amortissable=0   
            for j in range(ncoupon):
              if flux_actualiser[j] != "NaN": 
                Duration_Amortissable+=flux_actualiser[j]*(M[j]/A) 
            Prix_Dirty=[]
            Duration=[]
            Prix_Dirty.append(s)
            Duration.append(Duration_Amortissable/s)
            for j in range(1,ncoupon):
                Prix_Dirty.append("NaN")
                Duration.append("NaN")
            sensibilite=[]                
            sensb=-(Duration[0]/(1+interpZC(diffdate(date_echeance,date_valeur))+Spread))
            sensibilite.append(sensb)
            for j in range(1,ncoupon):
                sensibilite.append("NaN")  
            Tableau_amortissement = pd.DataFrame({'Date_coupon':Date_coupon,'Reste_a_rembourser':Reste_a_rembourser,'Interets':Interets,'Amortissement':Amortissement,'flux':flux,'Maturite':M,'Taux_Zero_coupon':ZC,"Facteur_d'actualisation":facteur_actualisation,'Flux_Actualiser':flux_actualiser,'Prix_Dirty':Prix_Dirty,'Duration':Duration,"Sensibilité":sensibilite})
            return Tableau_amortissement

      def annuites_constantes(date_emission , date_valeur , date_echeance , date_jouissance , Nominal , taux_facial, Spread ):
        maturite_initiale = diffdate(date_echeance,date_emission)
        maturite_residuelle  = diffdate(date_echeance,date_valeur)
        prochain_coupon = 0
        i = 1 # nb de coupon restants
        while date_echeance.replace(year=date_echeance.year - i) > date_valeur and date_echeance.replace(year=date_echeance.year - i) > date_jouissance:
            i = i + 1   
        from datetime import timedelta
        prochain_coupon = date_echeance.replace(year=date_echeance.year + 1- i)
        ncoupon = (date_echeance.year - calculate_date_jouissance(date_echeance, date_emission).year)
        N=Nominal
        tf=taux_facial
        if date_valeur.year % 4 == 0 and (date_valeur.year % 100 != 0 or date_valeur.year % 400 == 0):
           A = 366
        else:
           A = 365
        flux=[]
        for j in range(ncoupon):
          flux_j= (N*tf )/(1-(1+tf)**(-ncoupon))  
          flux.append(flux_j)      
        Amortissement=[]
        Reste_a_rembourser=[]
        Reste_a_rembourser.append(N)
        Amortissement.append(flux[0]-N*tf)
        reste=N
        Amorti=flux[0]-N*tf
        for j in range(1,ncoupon):
          reste=reste-Amorti
          Reste_a_rembourser.append(reste)
          Amorti=flux[0]-reste*tf
          Amortissement.append(Amorti)
        Interets=[]  
        for j in range(ncoupon):
          Inter=Reste_a_rembourser[j]*tf
          Interets.append(Inter)
        M=[]
        for j in range(ncoupon):
           M_j= diffdate(calculate_date_jouissance(date_echeance, date_emission).replace(year=calculate_date_jouissance(date_echeance, date_emission).year +j+1),date_valeur)
           M.append(M_j)
        ZC=[] 
        for j in range(ncoupon):
          if M[j]<1:
            ZC.append("NaN")
          else:
            ZC_j= interpZC(M[j])
            ZC.append(ZC_j)  
        Date_coupon=[]
        for j in range(ncoupon): 
          Date_coupon.append(calculate_date_jouissance(date_echeance, date_emission).replace(year=calculate_date_jouissance(date_echeance, date_emission).year +j+1))
        facteur_actualisation=[]
        for j in range(ncoupon):
          if M[j]<1:
            facteur_actualisation.append("NaN")
          else:
            facteur_actualisation.append((1+ZC[j]+Spread)**(-M[j]/A))
        flux_actualiser=[]
        for j in range(ncoupon):
          if M[j]<1:
            flux_actualiser.append("NaN")
          else:
            flux_actualiser.append(flux[j]*facteur_actualisation[j])
        s=0
        for j in range(ncoupon):
          if flux_actualiser[j] != "NaN": 
            s+=flux_actualiser[j]
        Duration_annuites_constantes=0   
        for j in range(ncoupon):
          if flux_actualiser[j] != "NaN": 
            Duration_annuites_constantes+=flux_actualiser[j]*(M[j]/A)                
        Prix_Dirty=[]
        Duration=[]
        Prix_Dirty.append(s)
        Duration.append(Duration_annuites_constantes/s)
        for j in range(1,ncoupon):
            Prix_Dirty.append("NaN")
            Duration.append("NaN")            
        sensibilite=[]                
        sensb=-(Duration[0]/(1+interpZC(diffdate(date_echeance,date_valeur))+Spread))
        sensibilite.append(sensb)
        for j in range(1,ncoupon):
            sensibilite.append("NaN")
        Tableau_amortissement = pd.DataFrame({'Date_coupon':Date_coupon,'Reste_a_rembourser':Reste_a_rembourser,'Interets':Interets,'Amortissement':Amortissement,'flux':flux,'Maturite':M,'Taux_Zero_coupon':ZC,"Facteur_d'actualisation":facteur_actualisation,'Flux_Actualiser':flux_actualiser,'Prix_Dirty':Prix_Dirty,'Duration':Duration,"Sensibilité":sensibilite})
        return Tableau_amortissement

      def Bond_price_variable(date_emission , date_valeur , date_echeance , date_jouissance , Nominal, Spread ):
        maturite_initiale = diffdate(date_echeance,date_emission)
        maturite_residuelle = diffdate(date_echeance,date_valeur)
        prochain_coupon = 0
        if date_valeur.year % 4 == 0 and (date_valeur.year % 100 != 0 or date_valeur.year % 400 == 0):
           base = 366
        else:
           base = 365
        i = 1 # nb de coupon restants
        while date_echeance.replace(year=date_echeance.year - i) > date_valeur and date_echeance.replace(year=date_echeance.year - i) > date_jouissance:
            i = i + 1 
        k = 0 # nb de coupon passé
        while calculate_date_jouissance(date_echeance, date_emission).replace(year=calculate_date_jouissance(date_echeance, date_emission).year + k) < date_valeur:
          k += 1
        Nombre_de_flux_restant = i
        Nombre_de_flux_passé = k - 1
        Nombre_de_flux = Nombre_de_flux_restant + Nombre_de_flux_passé
        CRD = Nominal - (Nominal / Nombre_de_flux) * Nombre_de_flux_passé 
        prochain_coupon = date_echeance.replace(year=date_echeance.year + 1- i)
        precedent_coupon = prochain_coupon.replace(year=prochain_coupon.year -1)
        Mint = diffdate(prochain_coupon,date_valeur)
        Taux_ZC = interpZC(Mint)
        f = diffdate(prochain_coupon,date_valeur) / diffdate(prochain_coupon,precedent_coupon)
        Bond_price_variable=0
        for j in range(Nombre_de_flux_restant):
          if j==0:
            for j in range(Nombre_de_flux_restant):
              if Mint < 365:
                taux_forward = interp(1)
              else:
                taux_forward = interpZC(365)
          else:      
            taux_forward = ((((1 + Taux_ZC) ** (Mint / base)) / ((1 + taux_ZCant) ** (Mintant / base))) ** (base / (Mint - Mintant))) - 1
          flux = (CRD * taux_forward) + (Nominal / Nombre_de_flux)
          Bond_price_variable = Bond_price_variable + ((flux) / ((1 + Taux_ZC + Spread) ** (f + j)))
          CRD = CRD - (Nominal / Nombre_de_flux)
          prochain_coupon = date_echeance.replace(year=prochain_coupon.year + 1)
          Mintant = Mint
          Mint = diffdate(prochain_coupon,date_valeur) 
          taux_ZCant = Taux_ZC
          Taux_ZC = interpZC(Mint)
        return Bond_price_variable

      def Duration_variable(date_emission , date_valeur , date_echeance , date_jouissance , Nominal , Spread ):
        maturite_initiale =diffdate(date_echeance , date_emission) 
        maturite_residuelle =diffdate(date_echeance , date_valeur) 
        prochain_coupon = 0
        if date_valeur.year % 4 == 0 and (date_valeur.year % 100 != 0 or date_valeur.year % 400 == 0):
           base = 366
        else:
           base = 365
        i = 1 # nb de coupon restants
        while date_echeance.replace(year=date_echeance.year - i) > date_valeur and date_echeance.replace(year=date_echeance.year - i) > date_jouissance:
            i = i + 1    
        prochain_coupon = date_echeance.replace(year=date_echeance.year + 1- i)
        k = 0 # nb de coupon passé
        while calculate_date_jouissance(date_echeance, date_emission).replace(year=calculate_date_jouissance(date_echeance, date_emission).year + k) < date_valeur:
          k += 1
        Nombre_de_flux_restant = i
        Nombre_de_flux_passé = k - 1
        Nombre_de_flux = Nombre_de_flux_restant + Nombre_de_flux_passé
        CRD = Nominal - (Nominal / Nombre_de_flux) * Nombre_de_flux_passé
        prochain_coupon = date_echeance.replace(year=date_echeance.year + 1- i)
        precedent_coupon = prochain_coupon.replace(year=prochain_coupon.year -1)
        Mint = diffdate(prochain_coupon,date_valeur)
        Taux_ZC = interpZC(Mint)
        f = diffdate(prochain_coupon,date_valeur) / diffdate(prochain_coupon,precedent_coupon)
        Bond_price_variable=0
        Duration_variable=0
        for j in range(Nombre_de_flux_restant):
          if j==0:
            for j in range(Nombre_de_flux_restant):
              if Mint < 365:
                taux_forward = interp(1)
              else:
                taux_forward = interpZC(365)
          else:      
            taux_forward = ((((1 + Taux_ZC) ** (Mint / base)) / ((1 + taux_ZCant) ** (Mintant / base))) ** (base / (Mint - Mintant))) - 1
          flux = (CRD * taux_forward) + (Nominal / Nombre_de_flux)
          Bond_price_variable = Bond_price_variable + ((flux) / ((1 + Taux_ZC + Spread) ** (f + j)))
          Duration_variable = Duration_variable + ((((flux) / ((1 + Taux_ZC + Spread) ** (f + j)))) * (f + j))
          CRD = CRD - (Nominal / Nombre_de_flux)
          prochain_coupon = date_echeance.replace(year=prochain_coupon.year + 1)
          Mintant = Mint
          Mint = diffdate(prochain_coupon,date_valeur) 
          taux_ZCant = Taux_ZC
          Taux_ZC = interpZC(Mint)
        return Duration_variable/Bond_price_variable

      def Bond_price_Revisable(date_emission, date_valeur, date_echeance, date_jouissance, Nominal, taux_facial, Spread, point_base):
        maturite_initiale = diffdate(date_echeance,date_emission) 
        maturite_residuelle = diffdate(date_echeance,date_valeur) 
        prochain_coupon = 0
        if date_valeur.year % 4 == 0 and (date_valeur.year % 100 != 0 or date_valeur.year % 400 == 0):
           A = 366
        else:
           A = 365
        i = 1 # nb de coupon restants
        while date_echeance.replace(year=date_echeance.year - i) > date_valeur and date_echeance.replace(year=date_echeance.year - i) > date_jouissance:
            i = i + 1    
        prochain_coupon = date_echeance.replace(year=date_echeance.year + 1- i)
        Nje = diffdate(prochain_coupon,date_valeur)
        Taux_rendement = interp(Nje)+point_base+Spread
        if maturite_residuelle > 364:
          Bond_price_Revisable = (1 + taux_facial + Spread) / ((1 + Taux_rendement + Spread) ** (Nje / A))
        else:
          Bond_price_Revisable = (1 + taux_facial + Spread) / (1 + (Taux_rendement + Spread) * (Nje / 360))
        return Bond_price_Revisable * Nominal

      def DRevisable(date_emission, date_valeur, date_echeance , date_jouissance , Nominal , taux_facial , Spread ):
        maturite_initiale =diffdate (date_echeance , date_emission)
        maturite_residuelle =diffdate (date_echeance , date_valeur)
        prochain_coupon = 0
        if date_valeur.year % 4 == 0 and (date_valeur.year % 100 != 0 or date_valeur.year % 400 == 0):
           A = 366
        else:
           A = 365
        i = 1 # nb de coupon restants
        while date_echeance.replace(year=date_echeance.year - i) > date_valeur and date_echeance.replace(year=date_echeance.year - i) > date_jouissance:
            i = i + 1    
        prochain_coupon = date_echeance.replace(year=date_echeance.year + 1- i)
        Nje =diffdate(prochain_coupon , date_valeur) 
        Taux_rendement = interp(Nje)
        if maturite_residuelle > 364 :
          Bond_price_Revisable = (1 + taux_facial + Spread) / ((1 + Taux_rendement + Spread) ** (Nje / A))
          DRevisable = Bond_price_Revisable * (Nje / A) * Nominal
        else:
          Bond_price_Revisable = (1 + taux_facial + Spread) / (1 + (Taux_rendement + Spread) * (Nje / 360))
          DRevisable = Bond_price_Revisable * (Nje / 360) * Nominal  
        Bond_price_Revisable = Bond_price_Revisable * Nominal
        return DRevisable / Bond_price_Revisable
      
      #date_emission = st.date_input("Date d'émission", datetime.now(), key="date_emission_pricer")
      #date_echeance = st.date_input("Date d'échéance", datetime.now(), key="date_echeance_pricer")
      #date_jouissance = st.date_input("Date de jouissance", datetime.now(), key="date_jouissance_pricer")
      #nominal = st.number_input("Nominal", value=100000.0, key="nominal_pricer")
      #taux_facial = st.number_input("Taux facial", value=0.0, key="taux_facial_pricer")
      #spread = st.number_input("Spread", value=0.0, key="spread_pricer")
      
      # Convert date objects to strings before parsing
      #date_emission = date_emission.strftime('%d/%m/%Y')
      #date_echeance = date_echeance.strftime('%d/%m/%Y')
      #date_jouissance = date_jouissance.strftime('%d/%m/%Y')

      # Parse the strings back to datetime.date objects
      #date_emission = datetime.strptime(date_emission, '%d/%m/%Y').date()
      #date_echeance = datetime.strptime(date_echeance, '%d/%m/%Y').date()
      #date_jouissance = datetime.strptime(date_jouissance, '%d/%m/%Y').date()

      #nominal=float(nominal)
      #taux_facial=float(taux_facial)
      #spread=float(spread)
      
      if option == "In fine à taux fixe":
          value1 = Bond_price(date_emission, date_echeance, date_jouissance, date_valeur, nominal, taux_facial, spread, 0)
          value2 = coupon_couru_unitaire(date_emission, date_valeur, date_echeance, date_jouissance, nominal, taux_facial)
          value3 = value1 - value2
          value4 = diffdate(date_echeance, date_valeur)
          value5 = interp(value4)
          value6 = Duration_in_fine(date_emission, date_valeur, date_echeance, date_jouissance, nominal, taux_facial, spread)
          value7 = -(value6 / (1 + value5 + spread))

          # Convexité
          p_plus = Bond_price(date_emission, date_echeance, date_jouissance, date_valeur, nominal, taux_facial, spread, -0.0001)
          p_moins = Bond_price(date_emission, date_echeance, date_jouissance, date_valeur, nominal, taux_facial, spread, 0.0001)
          convx = (10**6) * (1 / value1) * (p_plus + p_moins - (2 * value1))

          data = {
              'Prix Dirty': [value1],
              'Coupon couru': [value2],
              'Prix Clean': [value3],
              'Maturité résiduelle': [value4],
              'Taux de rendement': [value5],
              'Duration': [value6],
              'Sensibilité': [value7],
              'Convexité': [convx]
          }
          df = pd.DataFrame(data)
          st.write(df)

      elif option == "Amortissement constant":
          tableau = Bond_price_Amortissable(date_emission, date_valeur, date_echeance, date_jouissance, nominal, taux_facial, spread)
          st.write(tableau)

      elif option == "Annuité constante":
          tableau = annuites_constantes(date_emission, date_valeur, date_echeance, date_jouissance, nominal, taux_facial, spread)
          st.write(tableau)

      elif option == "Taux variable":
          value1 = Bond_price_variable(date_emission, date_valeur, date_echeance, date_jouissance, nominal, spread)
          value2 = Duration_variable(date_emission, date_valeur, date_echeance, date_jouissance, nominal, spread)
          value3 = diffdate(date_echeance, date_valeur)
          value4 = interpZC(value3)
          value5 = -(value2 / (1 + value4 + spread))

          data = {
              'Prix Dirty': [value1],
              'Duration': [value2],
              'Sensibilité': [value5]
          }
          df = pd.DataFrame(data)
          st.write(df)

      elif option == "Taux révisable":
          value1 = Bond_price_Revisable(date_emission, date_valeur, date_echeance, date_jouissance, nominal, taux_facial, spread, 0)
          value2 = DRevisable(date_emission, date_valeur, date_echeance, date_jouissance, nominal, taux_facial, spread)
          value3 = diffdate(date_echeance, date_valeur)
          value4 = interp(value3)
          value5 = -(value2 / (1 + value4 + spread))

          p_plus = Bond_price_Revisable(date_emission, date_valeur, date_echeance, date_jouissance, nominal, taux_facial, spread, -0.0001)
          p_moins = Bond_price_Revisable(date_emission, date_valeur, date_echeance, date_jouissance, nominal, taux_facial, spread, 0.0001)
          convx = (10**6) * (1 / value1) * (p_plus + p_moins - (2 * value1))

          data = {
              'Prix Dirty': [value1],
              'Duration': [value2],
              'Sensibilité': [value5],
              'Convexité': [convx]
          }
          df = pd.DataFrame(data)
          st.write(df)
    
    
    if st.button("Afficher les résultat"):
       
     resultats = prix_Dirty(
        date_valeur=date_valeur,  # Utilise les dates saisies dans l'interface
        date_emission=date_emission,
        date_echeance=date_echeance,
        date_jouissance=date_jouissance,
        nominal=nominal,
        taux_facial=taux_facial,
        spread=spread
    )
     st.write(resultats)



elif page == "P&L":

    st.header("Profit & Loss Analysis")
    st.subheader("Calcule du shift")
    
    # Création de deux colonnes pour la sélection des dates
    col1, col2 = st.columns(2)
    
    with col1:
        date1 = st.date_input("Sélectionnez la première date", datetime.now(),key="date1_pnl")
        
    with col2:
        date2 = st.date_input("Sélectionnez la seconde date", datetime.now() - timedelta(days=1),key="date2_pnl")
    
    # Formatage des dates en string pour la fonction ecart_ZC
    date1_str = date1.strftime("%d/%m/%Y")
    date2_str = date2.strftime("%d/%m/%Y")
    
    if st.button("Calculer l'écart ZC"):
        try:
        # Calcul de l'écart
         data_ecart_ZC = ecart_ZC(date1_str, date2_str)
        
        # Stockage des résultats dans session_state
         st.session_state['ecart_data'] = data_ecart_ZC
         st.session_state['dates'] = (date1_str, date2_str)
        
        # Affichage des résultats
         st.write("Résultats de l'écart ZC :")
         st.dataframe(data_ecart_ZC)
        
        # Calcul de la moyenne quadratique
         valeurs = data_ecart_ZC["Ecart"]
         moyenne_quadratique = np.sqrt(np.mean(np.square(valeurs)))
        
         st.metric("Moyenne quadratique des écarts (Shift)", f"{moyenne_quadratique:.10f}")
        
        except Exception as e:
         st.error(f"Une erreur est survenue : {str(e)}")

# Bouton d'affichage graphique indépendant
    if 'ecart_data' in st.session_state:
        if st.button("📈 Afficher le graphique"):
         plot_ecart(
            st.session_state['ecart_data'],
            st.session_state['dates'][0],
            st.session_state['dates'][1]
         )
    st.subheader("calcul des différentes contributions")
    if st.button("chargé les données du portfeuille"):
         if os.path.exists(portfolio_path):
            portfolio_data = load_portfolio(portfolio_path)
        
            if portfolio_data:
             st.success("Portefeuille chargé avec succès !")
            
            # Affichage des onglets disponibles
             selected_sheet = st.selectbox("Sélectionner une feuille", 
                                        options=list(portfolio_data.keys()))
            
            # Affichage du dataframe avec options
             st.dataframe(portfolio_data[selected_sheet],
                         height=400,
                         use_container_width=True,
                         hide_index=True)
            
            # Téléchargement optionnel
            import io  # Add this import for in-memory buffer

            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                portfolio_data[selected_sheet].to_excel(writer, index=False)

            st.download_button(
                label="Exporter les données",
                data=buffer.getvalue(),
                file_name=f"export_{selected_sheet}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
         else:
             st.warning("Fichier introuvable au chemin spécifié. Veuillez utiliser l'uploader.")
    
    
    if st.button("Pricing des 2 dates "):
        # Load portfolio as a DataFrame
        try:
            portfolio_df = pd.read_excel(portfolio_path)
        except Exception as e:
            st.error(f"Error loading portfolio: {e}")
            st.stop()

        # Initialize an empty list to collect errors
        errors = []

        for i in range(len(portfolio_df)):
            try:
                # Ensure all required columns exist
                required_columns = ["Emission", "Échéance", "Jouissance", "Nominal", "Taux facial"]
                for col in required_columns:
                    if col not in portfolio_df.columns:
                        raise KeyError(f"Missing required column: {col}")

                # Convert inputs to the correct types
                emission_date = pd.to_datetime(portfolio_df.loc[i, "Emission"]).date()
                echeance_date = pd.to_datetime(portfolio_df.loc[i, "Échéance"]).date()
                jouissance_date = pd.to_datetime(portfolio_df.loc[i, "Jouissance"]).date()
                nominal = float(portfolio_df.loc[i, "Nominal"])
                taux_facial = float(portfolio_df.loc[i, "Taux facial"])

                # Calculate bond prices for the two dates
                portfolio_df.loc[i, "Prix_date_1"] = Bond_price(
                    emission_date,
                    date(2023, 5, 18),
                    echeance_date,
                    jouissance_date,
                    nominal,
                    taux_facial,
                    0
                )
                portfolio_df.loc[i, "Prix_date_2"] = Bond_price(
                    emission_date,
                    date(2023, 5, 19),
                    echeance_date,
                    jouissance_date,
                    nominal,
                    taux_facial,
                    0
                )
            except Exception as e:
                # Log errors for each row
                errors.append(f"Row {i}: {e}")
                portfolio_df.loc[i, "Prix_date_1"] = None
                portfolio_df.loc[i, "Prix_date_2"] = None

        # Store the DataFrame in session_state
        st.session_state["portfolio_df"] = portfolio_df

        # Display errors if any
        if errors:
            st.error("Some rows could not be processed:")
            for error in errors:
                st.error(error)

        # Display the updated portfolio
        st.write(portfolio_df)

    if st.button("Calcul des différentes contributions"):
        # Check if portfolio_df exists in session_state
        if "portfolio_df" not in st.session_state:
            st.error("Veuillez d'abord exécuter le bouton 'Pricing des 2 dates'.")
        else:
            portfolio_df = st.session_state["portfolio_df"]
            
            # Initialisation des colonnes pour les prix globaux et gains
            for i in range(len(portfolio_df)):
                portfolio_df.loc[i, "Prix_Glo_date1"] = portfolio_df.loc[i, "Prix_date_1"] * portfolio_df.loc[i, "Quantité"]
                portfolio_df.loc[i, "Prix_Glo_date2"] = portfolio_df.loc[i, "Prix_date_2"] * portfolio_df.loc[i, "Quantité"]

            for i in range(len(portfolio_df)):
                portfolio_df.loc[i, "Gain_Glo_date1"] = portfolio_df.loc[i, "Prix_Glo_date1"] - portfolio_df.loc[i, "Prix Achat Glo"]
                portfolio_df.loc[i, "Gain_Glo_date2"] = portfolio_df.loc[i, "Prix_Glo_date2"] - portfolio_df.loc[i, "Prix Achat Glo"]

            # Calcul du PnL
            for i in range(len(portfolio_df)):
                portfolio_df.loc[i, "PnL"] = portfolio_df.loc[i, "Prix_date_2"] - portfolio_df.loc[i, "Prix_date_1"]

            # Calcul des différents effets
            # 1. Effet coupon
            couru_date1 = []
            couru_date2 = []
            effet_coupon = []
            
            for i in range(len(portfolio_df)):
                couru_date1.append(coupon_couru_unitaire(
                    portfolio_df.loc[i, "Emission"], 
                    date(2023, 5, 18),  # Ensure correct usage of datetime.date
                    portfolio_df.loc[i, "Échéance"], 
                    portfolio_df.loc[i, "Jouissance"], 
                    portfolio_df.loc[i, "Nominal"], 
                    portfolio_df.loc[i, "Taux facial"]
                ))
                
                couru_date2.append(coupon_couru_unitaire(
                    portfolio_df.loc[i, "Emission"], 
                    date(2023, 5, 19),  # Ensure correct usage of datetime.date
                    portfolio_df.loc[i, "Échéance"], 
                    portfolio_df.loc[i, "Jouissance"], 
                    portfolio_df.loc[i, "Nominal"], 
                    portfolio_df.loc[i, "Taux facial"]
                ))
                
                effet_coupon.append(couru_date2[i] - couru_date1[i])
            
            portfolio_df["Effet_coupon"] = effet_coupon
            
            # 2. Effet amortissement
            prix_date2_courbe_date1 = []
            effet_amortissement = []
            
            for i in range(len(portfolio_df)):
                prix = Bond_price_Effet_amortissement(
                    portfolio_df.loc[i, "Emission"], 
                    date(2023, 5, 19),  # Ensure correct usage of datetime.date
                    portfolio_df.loc[i, "Échéance"], 
                    portfolio_df.loc[i, "Jouissance"], 
                    portfolio_df.loc[i, "Nominal"], 
                    portfolio_df.loc[i, "Taux facial"],
                    0
                )
                prix_date2_courbe_date1.append(prix)
                effet_amortissement.append(prix - portfolio_df.loc[i, "Prix_date_1"])
            
            portfolio_df["Effet_amortissement"] = effet_amortissement
            
            # 3. Effet niveau
            prix_date2_courbe_date1_shift = []
            effet_niveau = []
            
            for i in range(len(portfolio_df)):
                prix = Bond_price_Effet_niveau(
                    portfolio_df.loc[i, "Emission"], 
                    date(2023, 5, 19),  # Ensure correct usage of datetime.date
                    portfolio_df.loc[i, "Échéance"], 
                    portfolio_df.loc[i, "Jouissance"], 
                    portfolio_df.loc[i, "Nominal"], 
                    portfolio_df.loc[i, "Taux facial"],
                    0
                )
                prix_date2_courbe_date1_shift.append(prix)
                effet_niveau.append(prix - prix_date2_courbe_date1[i])
            
            portfolio_df["Effet_niveau"] = effet_niveau
            
            # 4. Effet courbe
            effet_courbe = []
            
            for i in range(len(portfolio_df)):
                effet_courbe.append(portfolio_df.loc[i, "Prix_date_2"] - prix_date2_courbe_date1_shift[i])
            
            portfolio_df["Effet_courbe"] = effet_courbe
            
            # Affichage du tableau avec toutes les colonnes
            st.write(portfolio_df[["AMC", "Prix_date_1", "Prix_date_2", "PnL", 
                                 "Effet_coupon", "Effet_amortissement", 
                                 "Effet_niveau", "Effet_courbe"]])






