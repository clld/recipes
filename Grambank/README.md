
# Accessing Grambank data

The [Grambank](http://grambank.clld.org) data is archived with [ZENODO](https://zenodo.org) as CLDF structure dataset.
Below we describe methods to access this data from various computing environments. For all methods we assume an
unzipped download of the CLDF dataset to be available on a local disk, i.e. a directory `Grambank` with the following contents:
- `StructureDataset-metadata.json`: The machine readable description of the dataset
- `values.csv`: The main data file, containing all codings
- `languages.csv`
- `parameters.csv`
- `codes.csv`
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

Africa
  Not known: 8.78%
  absent: 41.95%
  present: 49.27%
Australia
  Not known: 12.95%
  absent: 79.14%
  present: 7.91%
Eurasia
  Not known: 2.36%
  absent: 75.59%
  present: 22.05%
North America
  Not known: 8.97%
  absent: 38.46%
  present: 52.56%
Papunesia
  Not known: 5.17%
  absent: 55.17%
  present: 39.67%
South America
  Not known: 22.60%
  absent: 61.02%
  present: 16.38%
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

While loading the dataset into SQLite isn't particularly quick, querying the database may be a lot quicker than the equivalent operations using Python. So the SQL query in 
[`values_per_area.sql`](values_per_area.sql), which is roughly equivalent to the example above, runs in
less than 0.1 secs:
```bash
$ time cat values_per_area.sql | sqlite3 grambank.sqlite 
Africa|0|41.9512195121951
Africa|1|49.2682926829268
Africa|?|8.78048780487805
Australia|0|79.136690647482
Australia|1|7.9136690647482
Australia|?|12.9496402877698
Eurasia|0|75.5905511811024
Eurasia|1|22.0472440944882
Eurasia|?|2.36220472440945
North America|0|38.4615384615385
North America|1|52.5641025641026
North America|?|8.97435897435897
Papunesia|0|55.1652892561983
Papunesia|1|39.6694214876033
Papunesia|?|5.16528925619835
South America|0|61.0169491525424
South America|1|16.3841807909604
South America|?|22.5988700564972

real	0m0.110s
```

<a id="r"> </a>
## Accessing Grambank data in R

Assuming that `languages.csv` and `values.csv` are in your current working directory, launch an `R` session and execute:

```R
l <- read.csv("languages.csv")
v <- read.csv("values.csv")

parameter <- "GB020"
param.filtered <- v[v$Parameter_ID == parameter,]

lang.param.subset <- l[l$ID %in% param.filtered$Language_ID & l$Macroarea != "",]
colnames(lang.param.subset)[1] <- "Language_ID"
merged <- merge(lang.param.subset, v[v$Parameter_ID == parameter,], by = "Language_ID", all = TRUE)

merged.df <- as.data.frame(table(merged$Value, merged$Macroarea))
merged.transformed <- transform(merged.df, Totals = ave(merged.df$Freq, merged.df$Var2, FUN=sum))
merged.transformed <- transform(merged.transformed, perc = paste0(sprintf("%.2f", 100 * Freq/Totals),"%"))
merged.transformed[merged.transformed$Freq != 0,]
```

The output should be as follows:

```bash
   Values   Macroarea Freq Totals   Perc
1     ?        Africa   36    410  8.78%
2     0        Africa  172    410 41.95%
3     1        Africa  202    410 49.27%
6     ?     Australia   18    139 12.95%
7     0     Australia  110    139 79.14%
8     1     Australia   11    139  7.91%
11    ?       Eurasia    6    254  2.36%
12    0       Eurasia  192    254 75.59%
13    1       Eurasia   56    254 22.05%
16    ? North America   14    156  8.97%
17    0 North America   60    156 38.46%
18    1 North America   82    156 52.56%
21    ?     Papunesia   25    484  5.17%
22    0     Papunesia  267    484 55.17%
23    1     Papunesia  192    484 39.67%
26    ? South America   40    177 22.60%
27    0 South America  108    177 61.02%
28    1 South America   29    177 16.38%
```

A simple plot that illustrates the individual distributions can be achieved by using the external library `lattice` (the following snippet assumes that you are still in the same `R` session as when the table above was created):

```R
library(lattice)
merged.transformed <- transform(merged.transformed, perc = 100 * Freq/Totals)
plot.this <- merged.transformed[merged.transformed$Freq != 0,]
barchart(plot.this$Var1 ~ plot.this$perc | plot.this$Var2, xlab="Are there definite or specific articles? (1 = present/0 = absent/? = not known)")
```

The output should be as follows:

![Barchart Feature Distribution](https://raw.githubusercontent.com/clld/recipes/master/Grambank/RPlotExample.png)
