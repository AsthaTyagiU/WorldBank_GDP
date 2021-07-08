# WorldBank_GDP
using Python and Postgres to import data from api and csv into database for GDP calculations

Attached files and description (in order to execute):
1. **create_table_view.sql** : This sql file has commands to create required tables and view in database
2. **load_data.py**: This file loads data from api and csv to earlier created tables, view. 
3. **Calculation_query**: This file has queries to provide diferent caluculationsin database based on table values.
4. API_NY.GDP.MKTP.CD_DS2_en_csv_v2_2593330.csv: to be loaded into database

Detailed description:
1. **create_table_view.sql**: creates following tables: (country, region, income, worldbank, gdp), and view: (v_worldbank)
3. **load_data.py**: loads World Bank data from : <UL>- api (https://datahelpdesk.worldbank.org/knowledgebase/articles/898590-api-country-queries), and</UL> <UL>- csv file (API_NY.GDP.MKTP.CD_DS2_en_csv_v2_2593330)</UL>
<ul>The api data is used to load 4 tables: country, region, income, worldbank (to relate country, region, income), and a view: v_worldbank (all the data, with other related columsn like ISOcode, etc., after joining these tables). </ul>
  <p>The attached csv file loads table: gdp </p>
  <ul> Run this file from pyhton cmd prompt: exec(open("load_data.py").read())</ul>
</br>

Assumptions/ Points to note: 
1. You have psycopg2 and Pandas installed, if not, please run below commands:
<br/>pip install psycopg2
<br/> pip install pandas
2. **Connection string**: Please edit/modify postgres database connection details in load_data.py.
3. Copy downloaded CSV file to woring directory.
