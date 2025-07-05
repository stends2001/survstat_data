from utils import *
from survstat_collecting.survstat_scraper import scrape_survstat_data
from survstat_collecting.casedata_processing import preprocess_survstat_data
from datetime import datetime

def main():
    current_year = datetime.now().year
    diseases_dict = read_log()

    if len(diseases_dict) == 0:
        raise ValueError(f'no diseases found! Check the log.')

    all_years = range(2001, current_year + 1)

    scrape_survstat_data(disease_names=diseases_dict, 
                         years=str(current_year), 
                         output_directory=directories_dict['dir_data_raw'], 
                         downloads_path=directories_dict['dir_downloads'])

    preprocess_survstat_data(bugs=list(diseases_dict.values()), 
                             years=all_years,
                             raw_data_dir=directories_dict['dir_data_raw'], 
                             processed_data_dir=directories_dict['dir_data_preprocessed'])

    log_script_run(diseases_dict, all_years)

if __name__ == "__main__":
    main()
