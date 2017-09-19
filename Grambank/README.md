
# Accessing Grambank data


## Using `pycldf` programmatically from Python scripts

The script [`values_per_area.py`](values_per_area.py) gives an example how the `pycldf` package
can be used to read the Grambank data from within a Python program.


### Requirements

To run the script, you need 
- Python 2.7 or 3.4+
- with `pycldf>=1.0`
- an unzipped local download of the Grambank CLDF data.


### Usage

The script requires two arguments:
- the path to the JSON metadata file of the CLDF dataset
- a Grambank feature ID

```bash
$ python cldf_example.py StructureDataset-metadata.json GB020

GB020: Are there definite or specific articles?

africa
  Not known: 6.96%
  absent: 40.51%
  present: 52.53%
australia
  Not known: 9.01%
  absent: 82.88%
  present: 8.11%
eurasia
  Not known: 4.72%
  absent: 68.87%
  present: 26.42%
northamerica
  Not known: 6.45%
  absent: 38.71%
  present: 54.84%
pacific
  Not known: 2.33%
  absent: 58.14%
  present: 39.53%
southamerica
  Not known: 17.86%
  absent: 64.29%
  present: 17.86%
```


## Accessing Grambank data in SQLite

The `pycldf` package comes with a command to load a CLDF dataset into a SQLite database,
facilitating further analysis and manipulation via SQL:

```bash
$ time cldf createdb StructureDataset-metadata.json grambank.sqlite
INFO    <cldf:v1.0:StructureDataset at .> loaded in grambank.sqlite

real	0m12.584s
```

While loading the dataset into SQLite isn't particularly quick, querying the database may make
be a lot more performant than the equivalent operations using Python. So the SQL query in 
[`values_per_area.sql`](values_per_area.sql), which is roughly equivalent to the example above, runs in
less than 0.1 secs:
```bash
$ time cat values_per_area.sql | sqlite3 grambank.sqlite 
africa|0|40.5063291139241
africa|1|52.5316455696203
africa|?|6.9620253164557
australia|0|82.8828828828829
australia|1|8.10810810810811
australia|?|9.00900900900901
eurasia|0|68.8679245283019
eurasia|1|26.4150943396226
eurasia|?|4.71698113207547
northamerica|0|38.7096774193548
northamerica|1|54.8387096774194
northamerica|?|6.45161290322581
pacific|0|58.1395348837209
pacific|1|39.5348837209302
pacific|?|2.32558139534884
southamerica|0|64.2857142857143
southamerica|1|17.8571428571429
southamerica|?|17.8571428571429

real	0m0.066s
```
