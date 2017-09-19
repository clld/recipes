
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
$ python cldf_example.py Grambank/cldf/StructureDataset-metadata.json GB020

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
facilitating further analysis and manipulation via SQL.

