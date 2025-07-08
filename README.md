# SurvStat loading and processing
SurvStat is this interactive platform by the RKI, from which disease-data can be downloaded. Using some functionality from the *Selenium*-library, I've written scripts that select and download data for a given disease and a given year, per week and per district of Germany (Kreis).

In **update_survstatdata.py**, you will find how to run the actual datascraping (function: **scrape_survstat_data**) and how to process these seperate yearly files into nicely standardized merged files (**preprocess_survstat_data**). Based on a harmonization-file, the Kreise-names that the RKI webpage uses in English by default are translated into the correct regional Kennziffern (*kz_kreis*) which is a five digit code of which the first correspond to the bundeslaender in which this Kreis is located.

Note that the scraping of data is relatively slow, because at some point, the script is waiting for data to be downloaded from the website, before moving the datafile in terms of location.

### Directories
To change the storage of directories, please adjust them accordingly in src/utils/dirs.

By default, the raw-data is downloaded into the respective disease folder in:
- data / raw
Then, these yearly files are collected and (pre)processed and stored into the respective disease folder in:
- data / preprocessed