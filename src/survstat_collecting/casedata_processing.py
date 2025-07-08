from utils.dirs import directories_dict
from utils.mappings import map_countynames_germany_eng_de, map_countynames_tokens_germany
from dataprocessor import DataProcessingOrchestrator
from tqdm import tqdm
import os
import pandas as pd
from typing import Optional, Union, List
from pathlib import Path
import warnings

def preprocess_survstat_data(bugs:  Union[List[str], str], 
                             years: Union[List[str], range, str],
                             raw_data_dir: Union[str, Path],
                             processed_data_dir: Union[str, Path],
                             how: str
                             ):
    """
    Processes downloaded survstat data. Each yearly dataset for the specific disease is merged into one dataset.

    Parameters:
    ----------
    bugs: Union[list[str], str]
        List of diseases to process.
    years: Union[list[int], range, str]
        List of years to process.
    raw_data_dir: str or Path
        Directory containing raw yearly data files.
    processed_data_dir: str or Path
        Directory where processed data will be saved.
    how: str
        Processing mode: 'reconstruct' (start fresh) or 'update' (append to existing).

    Example:
    -------
    >>> preprocess_survstat_data(bugs=list(diseases_dict.values()), 
    >>>                          years = all_years,
    >>>                          raw_data_dir=directories_dict['dir_data_raw'], 
    >>>                          processed_data_dir=directories_dict['dir_data_preprocessed'],
    >>>                          how='reconstruct')

    See also:
    ---------
    preprocess_yearfile
    """

    # input validation
    if not isinstance(bugs, list):
        bugs = [bugs]

    if isinstance(years, (str, int)):
        years = [str(years)]

    if isinstance(years, (range, list)):
        years = [str(yy) for yy in years]

    for bug in bugs:
        raw_datafolder      = os.path.join(str(raw_data_dir), bug)
        processed_datafolder= os.path.join(str(processed_data_dir), bug)
        
        # Initialize merged_dataset based on mode
        if how == 'update':
            years_int = [int(yy) for yy in years]
            merged_dataset = DataProcessingOrchestrator().import_data(filename = f"{bug}.csv", directory = processed_datafolder).filter([('year',years_int,'!in')])

        elif how == 'reconstruct':  # reconstruct mode
            merged_dataset = DataProcessingOrchestrator(name = f"{bug}_merged")

        else:
            raise ValueError(f"Invalid value for 'how': {how}. Please choose from ['reconstruct', 'update'].")

        for year in tqdm(years, desc=f"processing {bug}"):
            filename = f"{bug}_{year}.csv"
            yearfile = DataProcessingOrchestrator().import_data(filename = filename, directory = raw_datafolder, encoding= 'utf-16', separator="\t", colnames_row=1)
            yearfile_preprocessed = preprocess_yearfile(yearfile, year)

            # Concatenate data regardless of mode
            if merged_dataset.status == 0:
                # First iteration - use the preprocessed data directly
                merged_dataset = yearfile_preprocessed
            else:
                # Subsequent iterations - concatenate with existing data
                # Extract DataFrames from DataProcessingOrchestrator objects
                existing_df = merged_dataset.df
                new_df = yearfile_preprocessed.df
                # Type assertion to help the type checker
                if isinstance(existing_df, pd.DataFrame) and isinstance(new_df, pd.DataFrame):
                    with warnings.catch_warnings():
                        warnings.filterwarnings("ignore", category=FutureWarning, message=".*DataFrame concatenation with empty or all-NA entries.*")
                        concatenated_df = pd.concat([existing_df, new_df], ignore_index=True)                                  
                    
                    merged_dataset = DataProcessingOrchestrator(concatenated_df, name=f"{bug}_merged")
                else:
                    raise TypeError("Expected pandas DataFrames for concatenation")

        if merged_dataset.status and processed_datafolder is not None:
            os.makedirs(processed_datafolder, exist_ok=True)
            merged_dataset.save_data(filename = f"{bug}.csv", directory = processed_datafolder)
    print("✅ all data has been (pre)processed")

def preprocess_yearfile(yearfile: DataProcessingOrchestrator, year: str) -> DataProcessingOrchestrator:
    """
    preprocesses a single yearfile which is properly returned.
    """
    yearfile = (
        yearfile
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

    yearfile.df['timestamp'] = pd.to_datetime(yearfile.df['year'].astype(str) + yearfile.df['week'].astype(str) + '1', format='%G%V%u').dt.date
    return yearfile
