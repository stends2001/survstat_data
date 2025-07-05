from dataprocessor import DataProcessingOrchestrator
from .dirs import directories_dict


harmfile_germany_geography = DataProcessingOrchestrator(name='german_harmfile').import_data(
    filename="harmfile_germany.tsv", separator = "\t",
    directory=directories_dict['dir_data_harmonization']
)