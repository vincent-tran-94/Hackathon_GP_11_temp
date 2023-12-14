from netCDF4 import Dataset
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np  
import os
import datetime
import csv

"""
Installation de la librairie à requérir: 
pip install netCDF4
Test pour la France pour les 3 années à relever pour l'année 2021 à 2023 entre le mois juin à Aout 

Coordinates France: 
North = 51.75
West = -5.75 
East = 9.75
South = 43.75
"""

#Points latittude et longitude à relever pour une zone géographique
point_lat = np.arange(28, -19.75, -0.25)
point_long = np.arange(19.25, 364, 0.25)

# Chemin des fichiers
chemin_fichier_nc = 'data/France.nc'
path_to_csv = "./data" 
filename_csv = "temp_france.csv"
fichier_lat_long_csv = 'data/coordonnees_france.csv'

# Lecture du dataset NetCDF
data = Dataset(chemin_fichier_nc, 'r')

#Import des variables de données 
times = data.variables['time'][:]
lat = data.variables['latitude'][:]
lon = data.variables['longitude'][:]
times_unit = data.variables['time'].units
unitt = data.variables['t'].units
temp = data.variables['t']

#Import les coordonnées de latitude et longitude 
latitude = data['latitude'][:]
longitude = data['longitude'][:]

#Données sur les datetime à inialiser 
ref_date = datetime.datetime(int(times_unit[12:16]),int(times_unit[17:19]),int(times_unit[20:22]))
date_range = list() #Définir l'invervalle des dates de début et fin 

#Données sur les températures en Kelvin 
temp_data_500 = list()
temp_data_1000 = list()

#Calcul de distance entre le point de station vers l'observation de température  
diff_lat = np.around((latitude - point_lat[:, None])**2,decimals=2) 
diff_long = np.around((longitude - point_long[:, None])**2,decimals=2) 

#Valeurs minimales des latitudes et de longitudes
min_index_lat = diff_lat.argmin()
min_index_lon = diff_long.argmin()

#Fonction qui génère un dataframe
def generate_dataframe(ref_date,date_range,temp_data_500,temp_data_1000):
    for index, time, in enumerate(times):
        date_time = ref_date + datetime.timedelta(hours=int(time))
        date_range.append(date_time) 
        temp_data_500.append(temp[index,0,min_index_lat,min_index_lon])
        temp_data_1000.append(temp[index,1,min_index_lat,min_index_lon])
    
    df = pd.DataFrame(date_range,columns = ["Date-Time"])
    df["Date-Time"] = date_range
    df = df.set_index(["Date-Time"])
    df["Température à 500hPa ({})".format(unitt)] = temp_data_500
    df["Température à 1000hPa ({})".format(unitt)] = temp_data_1000
    return df

def temperature_moy_500():
    df = generate_dataframe(ref_date,date_range,temp_data_500,temp_data_1000)
    mean_temp_500 = df["Température à 500hPa (K)"].mean()
    return f"Temperature moyenne sur 500 hPa: {round(mean_temp_500,2)} K"

def temperature_moy_1000():
    df = generate_dataframe(ref_date,date_range,temp_data_500,temp_data_1000)
    mean_temp_1000 = df["Température à 1000hPa (K)"].mean()
    return f"Temperature moyenne sur 1000 hPa: {round(mean_temp_1000,2)} K"


def write_lat_long_to_csv(path_to_csv): 
    # Écriture des données de latitude et de longitude dans un même fichier CSV
    with open(path_to_csv, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Latitude', 'Longitude'])
        for lat, lon in zip(latitude, longitude):
            csv_writer.writerow([lat, lon])

#Fonction de conversion du dataframe vers le CSV 
def convert_dataframe_to_csv(path,filename):
    df = generate_dataframe(ref_date,date_range,temp_data_500,temp_data_1000)
    df.to_csv(os.path.join(path,filename),index=True)

#Fonction de visualisation des données sur la température de l'atsmophère en fonction du temps
def visualize_temp():
    df = generate_dataframe(ref_date,date_range,temp_data_500,temp_data_1000)
    temp_500 = temperature_moy_500()
    temp_1000 = temperature_moy_1000()
    Title = f"Analyse des températures [K] atmosphériques en France"
    fig, ax = plt.subplots(figsize=(11.69,8.27))
    plt.grid(linestyle="-",linewidth=1.0)
    fig.suptitle(Title,fontsize=20,weight='bold')
    ax.plot(df.index,df["{}".format(df.columns[0])],color="blue",label='Pression atmosphérique= 500hPa')
    ax.plot(df.index,df["{}".format(df.columns[1])],color="red",label='Pression atmosphérique= 1000hPa')
    ax.plot([], [],color="blue",label=f"{temp_500}")
    ax.plot([], [],color="red",label=f"{temp_1000}")
    ax.set_xlabel("Timezone: Eu", fontsize = 16) 
    ax.set_ylabel(f"Temperature [{unitt}]",fontsize = 16)
    ax.xaxis.set_tick_params(labelsize=12) 
    ax.yaxis.set_tick_params(labelsize=14) 
    fig.tight_layout()
    plt.legend()
    plt.savefig(f"visualisation/France_temperature.png")

def show_visualise():
    plt.show()

#print(generate_dataframe(ref_date,date_range,temp_data_500,temp_data_1000)) 
#write_lat_long_to_csv(fichier_lat_long_csv)
#convert_dataframe_to_csv(path_to_csv,filename_csv)
#print(temperature_moy_500())
visualize_temp()
#show_visualise()

