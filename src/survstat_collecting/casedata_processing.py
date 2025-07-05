from utils.dirs import directories_dict
from utils.mappings import map_countynames_germany_eng_de, map_countynames_tokens_germany
from dataprocessor import DataProcessingOrchestrator
from tqdm import tqdm
import os
import pandas as pd
from typing import Optional, Union, List
from pathlib import Path

def preprocess_survstat_data(bugs:  Union[List[str], str], 
                             years: Union[List[str], range, str],
                             raw_data_dir: Union[str, Path],
                             processed_data_dir: Union[str, Path],
                             ):
    """
    Processes downloaded survstat data. Each yearly dataset for the specific disease is merged into one dataset.

    Parameters:
    ----------
    bugs: list[str]
        List of diseases to process.
    years: list[int]
        List of years to process.

    Example:
    -------
    >>> process_survstat_data(downloaded_diseases, [2001, 2026])
    """

    if not isinstance(bugs, list):
        bugs = [bugs]

    if isinstance(years, str):
        years = [years]

    if isinstance(years, range):
        years = [str(yy) for yy in years]

    for bug in bugs:
        merged_dataset      = DataProcessingOrchestrator(name = f"{bug}_merged")
        raw_datafolder      = os.path.join(str(raw_data_dir), bug)
        processed_datafolder= os.path.join(str(processed_data_dir), bug)

        for year in tqdm(years, desc=f"processing {bug}"):
            filename            = f"{bug}_{year}.csv"
            yearfile = (
            DataProcessingOrchestrator()
            .import_data(filename = filename, directory = raw_datafolder, encoding= 'utf-16', separator="\t", colnames_row=1)
            .rename_cols({"Unnamed: 0": 'week'})
            .pivot_longer(index = 'week', levels_from= list(map_countynames_germany_eng_de.keys()).remove('City of Berlin'), value_colname= 'cases', levels_colname= "county")
            .mutate(new_colname='year', value=year)
            .change_dtype({'year': 'str'})
            .impute(colnames = 'cases', method ='zero')
            .replace(colname = "county", mapping_dict = map_countynames_germany_eng_de)
            .replace(colname = "county", mapping_dict = map_countynames_tokens_germany)
            .rename_cols({"county": 'kz_kreis'}) 
            .mutate(new_colname = "kz_kreis",       operation = "lambda row: str(row['kz_kreis']).zfill(5)") 
            )

            yearfile.df['timestamp'] = pd.to_datetime(yearfile.df['year'].astype(str) + yearfile.df['week'].astype(str) + '1', format='%G%V%u')

            if merged_dataset.status == 0:
                merged_dataset = yearfile
            else:
                merged_dataset = DataProcessingOrchestrator(pd.concat([merged_dataset.df, yearfile.df]))

        if merged_dataset.status and processed_datafolder is not None:
            os.makedirs(processed_datafolder, exist_ok=True)
            merged_dataset.save_data(filename = f"{bug}.csv", directory = processed_datafolder)
    print("✅ all data has been (pre)processed")