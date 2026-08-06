# Setting up a MYSQL database

## Create user, database and table 
Replace 'wh1080pwd' with the real password wherever it appears. 
``` bash
create user 'wh1080'@'%' identified by 'wh1080pwd';
create user 'wh1080'@'127.0.0.1' identified by 'wh1080pwd';
create user 'wh1080'@'localhost' identified by 'wh1080pwd';
create schema weather;
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES, CREATE TEMPORARY TABLES, CREATE VIEW ON weather.* TO 'wh1080'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES, CREATE TEMPORARY TABLES, CREATE VIEW ON weather.* TO 'wh1080'@'127.0.0.1';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES, CREATE TEMPORARY TABLES, CREATE VIEW ON weather.* TO 'wh1080'@'localhost';
```

## migrating to a new DB:
- create the new DB
- login to the DB as root and run the above commands
- run mysqldump on the old server: `mysqldump weather > weather.sql`
- copy the file to the new server 
- edit the file to add 'use weather' before the first drop statement, save and import it: `mysql < weather.sql`


## Using it
* install sqlalchemy 
* install pymysql 

 copy the parquet tables to MySQL
``` python
from sqlalchemy import create_engine
import pandas as pd

cnx = create_engine('mysql+pymysql://wh1080:wh1080pwd@localhost:3306/weather')
df = pd.read_parquet('somefile')
df.to_sql('wh1080data',cnx,schema='weather',if_exists='append', method='multi')
```

it may take some time...

writing data - easier with pymysql


reading data:
``` python
import sqlalchemy
import pandas as pd
cnx = sqlalchemy.create_engine('mysql+pymysql://wh1080:wh1080pwd@wordpresssite:3306/weather')
df = pd.read_sql('select * from wh1080data limit 2', cnx)
```