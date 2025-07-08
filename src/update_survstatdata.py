from utils import *
from survstat_collecting.survstat_scraper import scrape_survstat_data
from survstat_collecting.casedata_processing import preprocess_survstat_data
from datetime import datetime

def main():
    """
    This function calls all necessary functions to do the actual legwork.
    By default, the data for current year is downloaded, and the already
    existing disease data csv's are updated with this new file.

    The diseases for which data is downloaded and processed are, by default,
    extracted from log.txt. Given the shear number of diseases in here, you
    can adjust the diseases by changing the variables here, or by adjusting
    log.txt. Do note that by default log.txt is updated depending on the
    diseases listed.
    """

    current_year = datetime.now().year
    diseases_dict = read_log()

    if len(diseases_dict) == 0:
        raise ValueError(f'no diseases found! Check the log.')

    all_years = range(2001, current_year + 1)

    scrape_survstat_data(disease_names=diseases_dict, 
                         years=str(current_year), 
                         output_directory=directories_dict['dir_data_raw'], 
                         downloads_directory=directories_dict['dir_downloads'])

    preprocess_survstat_data(bugs=list(diseases_dict.values()), 
                             years = str(current_year),
                             raw_data_dir=directories_dict['dir_data_raw'], 
                             processed_data_dir=directories_dict['dir_data_preprocessed'],
                             how='update')

    

    log_script_run(diseases_dict, all_years)

if __name__ == "__main__":
    main()
