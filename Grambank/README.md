
# Accessing Grambank data

The [Grambank](http://grambank.clld.org) data is archived with [ZENODO](https://zenodo.org) as CLDF structure dataset.
Below we describe methods to access this data from various computing environments. For all methods we assume an
unzipped download of the CLDF dataset to be available on a local disk, i.e. a directory `Grambank` with the following contents:
- `StructureDataset-metadata.json`: The machine readable description of the dataset
- `values.csv`: The main data file, containing all codings
- `languages.csv`
- `parameters.csv`
- `sources.bib`


These files can be accessed in various ways:
- [Using off-the-shelf CSV tools](#csvkit)
- [`pycldf`](#pycldf)
- [SQLite](#sqlite)


<a id="csvkit"> </a>
## Using off-the-shelve CSV tools

A CLDF dataset is - basically - just a set of CSV files. Thus, it can be accessed using off-the-shelf
tools to handle CSV data (e.g. spreadsheet processors). One such tool which can be particularly useful as
"pre-processor" for CLDF data is [`csvkit`](https://csvkit.readthedocs.io/). In particular the 
[`csvjoin`](https://csvkit.readthedocs.io/en/1.0.2/scripts/csvjoin.html) command, installed with `csvkit` can
be used to merge the data from the various constituent CSV files of a CLDF dataset into a single file for
easier processing, e.g. in statistical analysis tools like [R](https://www.r-project.org/) or [Pandas](http://pandas.pydata.org/).

The typical usage with the Grambank data - a [CLDF structure dataset](https://github.com/glottobank/cldf/tree/master/modules/StructureDataset) - looks as follows:
1. We join the language metadata to each value row
2. then join the feature metadata
3. and finally pipe the result to a new CSV file.

```bash
$ csvjoin -c Language_ID,ID values.csv languages.csv \
| csvjoin -c Parameter_ID,ID - parameters.csv > grambank.csv
```

The merged file can then be inspected, e.g. using `csvstat` (although this may max out the resources of
some machines):
```bash
$ csvstat grambank.csv 
  1. "ID"
	Type of data:          Text
	Contains null values:  False
	Unique values:         144683
	...
  2. "Language_ID"
	Type of data:          Text
	Contains null values:  False
	Unique values:         993
	...
  3. "Parameter_ID"
	Type of data:          Text
	Contains null values:  False
	Unique values:         202
	...
  4. "Value"
	Type of data:          Text
	Contains null values:  False
	Unique values:         5
	Longest value:         1 characters
	Most common values:    0 (79277x)
	                       1 (41828x)
	                       ? (20929x)
	                       2 (2027x)
	                       3 (622x)
  5. "Comment"
	Type of data:          Text
	...
  6. "Source"
	Type of data:          Text
  7. "Name"
	Type of data:          Text
	Contains null values:  False
	Unique values:         993
	Longest value:         37 characters
	Most common values:    Javanese (199x)
	                       Sundanese (199x)
  8. "Latitude"
	Type of data:          Number
	Contains null values:  True (excluded from calculations)
	Smallest value:        -54
	Largest value:         70,669
	Mean:                  4,666
	Median:                5,383
	StDev:                 17,976
	Most common values:    None (4056x)
  9. "Longitude"
	Type of data:          Number
	Contains null values:  True (excluded from calculations)
	Smallest value:        -178,137
	Largest value:         179,198
	Mean:                  47,185
	Median:                31,205
	StDev:                 81,143
	Most common values:    None (4056x)
 10. "glottocode"
	Type of data:          Text
	Contains null values:  False
	Unique values:         993
	...
 11. "iso639P3code"
	Type of data:          Text
	Contains null values:  True (excluded from calculations)
	Unique values:         949
	Longest value:         3 characters
	...
 12. "macroarea"
	Type of data:          Text
	Contains null values:  True (excluded from calculations)
	Unique values:         7
	Most common values:    africa (54848x)
	                       pacific (34424x)
	                       eurasia (18560x)
	                       southamerica (14489x)
	                       australia (12672x)
 13. "family"
	Type of data:          Text
	Contains null values:  True (excluded from calculations)
	Unique values:         133
	Longest value:         24 characters
	Most common values:    Atlantic-Congo (24375x)
	                       Austronesian (21435x)
	                       Afro-Asiatic (12610x)
	                       Pama-Nyungan (7453x)
	                       None (5752x)
 14. "Name2"
	Type of data:          Text
	Contains null values:  False
	Unique values:         202
  ...
 15. "Domain"
	Type of data:          Text
	Contains null values:  False
	Most common values:    1:present;0:absent;?:Not known (139770x)
	                       1:Dem-N;2:N-Dem;3:both.;?:Not known (915x)
	                       1:Num-N;2:N-Num;3:both.;?:Not known (913x)
	                       1:SV;2:VS;3:both;?:Not known (910x)
	                       1:Possessor-Possessed;2:Possessed-Possessor;3:both;?:Not known (884x)

Row count: 144683
```

<a id="pycldf"> </a>
## Using `pycldf` programmatically from Python scripts

The script [`values_per_area.py`](values_per_area.py) gives an example how the [`pycldf` package](https://github.com/glottobank/pycldf)
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

<a id="sqlite"> </a>
## Accessing Grambank data in SQLite

The `pycldf` package comes with a command to load a CLDF dataset into a SQLite database,
facilitating further analysis and manipulation via SQL:

```bash
$ time cldf createdb StructureDataset-metadata.json grambank.sqlite
INFO    <cldf:v1.0:StructureDataset at .> loaded in grambank.sqlite

real	0m12.584s
```

While loading the dataset into SQLite isn't particularly quick, querying the database may make
be a lot quicker than the equivalent operations using Python. So the SQL query in 
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
