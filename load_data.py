print('importing packaages and setting up variables')
#importing packages
import requests
from xml.etree import ElementTree as ET
import psycopg2
#import csv
import pandas as pd
import os
import psycopg2.extras as extras

#setting up variables
var_host="localhost"        #connection: host
var_database="worldbank"    #database
var_user="postgres"         #user
var_password="postgres"     #password
var_url="http://api.worldbank.org/v2/country/?per_page=299" #api
var_csv="API_NY.GDP.MKTP.CD_DS2_en_csv_v2_2593330.csv" #csv file to be loaded

#setting up connection
print('Setting up postgres database connection')
conn = psycopg2.connect(
    host=var_host,
    database=var_database,
    user=var_user,
    password=var_password,
	)
connection.autocommit = True


print('Gathering data from api and populating into database')

response=requests.get(var_url)
tree = ET.fromstring(response.content)

for C,j in zip(tree.findall('{http://www.worldbank.org}country'), range(0,299)):
    id=C.get('id')
    iso2code=tree[j][0].text
    name=tree[j][1].text
    region=tree[j][2].text
    incomeLevel=tree[j][4].text
    for R in C.findall('{http://www.worldbank.org}region'):
        regionID=R.get('id')
        regionISO=R.get('iso2code')
    for I in C.findall('{http://www.worldbank.org}incomeLevel'):
        incomeID=I.get('id')
        incomeISO=I.get('iso2code')
    
    data_country="INSERT INTO country(countryID,iso2code,name) VALUES(%s,%s,%s)"
    data_region="INSERT INTO region(regionID,regionISO,region) VALUES(%s,%s,%s) ON CONFLICT (regionID) DO NOTHING"
    data_income="INSERT INTO income(incomeID,incomeISO,incomeLevel) VALUES(%s,%s,%s) ON CONFLICT (incomeID) DO NOTHING"
    data_worldbank="INSERT INTO worldbank(countryID, regionID,incomeID) VALUES(%s,%s,%s)"
    
    cur = conn.cursor()
    
    cur.execute(data_country, (id, iso2code,name))
    cur.execute(data_region, (regionID, regionISO, region))
    cur.execute(data_income, (incomeID, incomeISO,incomeLevel))
    cur.execute(data_worldbank, (id, regionID, incomeID))
    
    conn.commit()
    

print('Reading .csv files to insert into database')
df_gdp=pd.read_csv(var_csv, skiprows=4)
df_gdp=df_gdp.drop(['Country Name','Indicator Name','Indicator Code'],axis=1)
# gdp_file.melt(['Country Name','Country Code'],var_name='Year', value_name='GDP')
 
df_gdp= (df_gdp.set_index(['Country Code'])
   .stack()
   .rename_axis(['countryID', 'year'])
   .reset_index(name='GDP')
)

tuples = [tuple(x) for x in df_gdp.to_numpy()]
cols = ','.join(list(df_gdp.columns))

query  = "INSERT INTO %s(%s) VALUES %%s" % ('GDP', cols)
cursor = conn.cursor()

extras.execute_values(cursor, query, tuples)
conn.commit()    

print('Data loaded in database')