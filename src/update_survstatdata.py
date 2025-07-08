from utils import *
from survstat_collecting.survstat_scraper import scrape_survstat_data
from survstat_collecting.casedata_processing import preprocess_survstat_data
from datetime import datetime

def main():
    """
    The main function with which to download and then preprocess the survstat data.
    Using current functionality, the function downloads the data for the current year,
    and then updates the currently existing merged file, with the just now installed year again.
    The survstat data is updated online each week, so this script could be run each week.

    Do note that by default, all diseases in log.txt are downloaded and preprocessed. This is quite a lot,
    so you can also manually specific diseases_dict here.
    """

    current_year = datetime.now().year
    diseases_dict = read_log()

    if len(diseases_dict) == 0:
        raise ValueError(f'no diseases found! Check the log.')

    all_years = range(2001, current_year + 1)

    diseases_dict = {'RSV':'rsv'}

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
