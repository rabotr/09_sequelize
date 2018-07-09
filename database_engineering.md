
## Step 2 - Database Engineering

-- Use SQLAlchemy to model your table schemas and create a sqlite database for your tables. You will need one table for measurements and one for stations.

-- Create a Jupyter Notebook called `database_engineering.ipynb` and use this to complete all of your Database Engineering work.

-- Use Pandas to read your cleaned measurements and stations CSV data.

-- Use the `engine` and connection string to create a database called `hawaii.sqlite`.

-- Use `declarative_base` and create ORM classes for each table.

-- You will need a class for `Measurement` and for `Station`.

-- Make sure to define your primary keys.

-- Once you have your ORM classes defined, create the tables in the database using `create_all`.


```python
#Import dependencies
import pandas as pd

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
```


```python
# read in cleaned csvs
measurements_df = pd.read_csv("Homework/Instructions/Resources/clean_hawaii_measurements.csv", index_col=0)
stations_df = pd.read_csv("Homework/Instructions/Resources/clean_hawaii_stations.csv", index_col=0)
```


```python
measurements_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>date</th>
      <th>prcp</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USC00519397</td>
      <td>2010-01-01</td>
      <td>0.08</td>
      <td>65</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00519397</td>
      <td>2010-01-02</td>
      <td>0.00</td>
      <td>63</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00519397</td>
      <td>2010-01-03</td>
      <td>0.00</td>
      <td>74</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00519397</td>
      <td>2010-01-04</td>
      <td>0.00</td>
      <td>76</td>
    </tr>
    <tr>
      <th>5</th>
      <td>USC00519397</td>
      <td>2010-01-07</td>
      <td>0.06</td>
      <td>70</td>
    </tr>
  </tbody>
</table>
</div>




```python
stations_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>elevation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USC00519397</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.2716</td>
      <td>-157.8168</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00513117</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.4234</td>
      <td>-157.8015</td>
      <td>14.6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00514830</td>
      <td>KUALOA RANCH HEADQUARTERS 886.9, HI US</td>
      <td>21.5213</td>
      <td>-157.8374</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00517948</td>
      <td>PEARL CITY, HI US</td>
      <td>21.3934</td>
      <td>-157.9751</td>
      <td>11.9</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00518838</td>
      <td>UPPER WAHIAWA 874.3, HI US</td>
      <td>21.4992</td>
      <td>-158.0111</td>
      <td>306.6</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Use the engine and connection string to create a database called hawaii.sqlite
engine = create_engine("sqlite:///Homework/Instructions/Resources/hawaii.sqlite")
```


```python
# Use declarative_base and create ORM classes for each table
Base = declarative_base()
```


```python
# You will need a class for Measurement and for Station
class Measurement(Base):
    __tablename__ = 'Measurement'
    id = Column(Integer, primary_key=True)
    station = Column(String(255))
    date = Column(String(255))
    prcp = Column(Integer)
    tobs = Column(Integer)

class Station(Base):
    __tablename__ = 'Station'
    id = Column(Integer, primary_key=True)
    station = Column(String(255))
    name = Column(String(255))
    latitude = Column(Integer)
    longitude = Column(Integer)
    elevation = Column(Integer)
```


```python
# Once you have your ORM classes defined, create the tables in the database using create_all.
Base.metadata.create_all(engine)

```


```python
engine.table_names()
```




    ['Measurement', 'Station']




```python
 # Populate a table from a Pandas DataFrame
def populate_table(engine, table, csvfile):
   
    # connect to the database
    conn = engine.connect()
    
    # Load the CSV file into a pandas dataframe 
    df_of_data_to_insert = pd.read_csv(csvfile)
    
    # Orient='records' creates a list of data to write
    # http://pandas-docs.github.io/pandas-docs-travis/io.html#orient-options
    data = df_of_data_to_insert.to_dict(orient='records')

    # Optional: Delete all rows in the table 
    conn.execute(table.delete())

    # Insert the dataframe into the database in one bulk insert
    conn.execute(table.insert(), data)
    
populate_table(engine, Station.__table__, "Homework/Instructions/Resources/clean_hawaii_stations.csv")

populate_table(engine, Measurement.__table__, "Homework/Instructions/Resources/clean_hawaii_measurements.csv")
```
