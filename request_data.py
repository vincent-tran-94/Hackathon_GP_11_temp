import cdsapi

"""
Script qui permet de requêter les données sur le site de Copernicus pour télécharger notre dataset 
cdaspi est une librairie python pour obtenir la clé de l'API sur le portail CDS à l'addresse https://cds.climate.copernicus.eu/user 
Lien du projet: https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=form
"""
#key="UID:key"
c = cdsapi.Client(url="https://cds.climate.copernicus.eu/api/v2",key="274155:ebedc1f8-1607-4482-a3e4-923272ff604a")

c.retrieve(
    'reanalysis-era5-pressure-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': 'temperature',
        'pressure_level': [
            '500', '1000',
        ],
        'month': [
            '06', '07', '08',
        ],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
        'time': [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
        'area': [
            51.75, 9.75, 43.75,
            -5.75,
        ],
        'year': ['1940','1999','2023']
    },
    'download.nc')