from pathlib import Path
import os

def get_downloads_folder():
    """
    Get the user's default downloads folder dynamically across different operating systems.
    This is the folder in which the downloads are found.
    """
    home = Path.home()
    
    possible_downloads = [
        home / "Downloads",
        home / "Download", 
        home / "downloads",
        home / "Desktop"  # Fallback
    ]
    
    for downloads_path in possible_downloads:
        if downloads_path.exists():
            return downloads_path
    
    # If none found, create Downloads folder in home directory
    downloads_path = home / "Downloads"
    downloads_path.mkdir(exist_ok=True)

    return downloads_path

project_root = Path(__file__).parent.parent.parent  # Go up from src/ to project root

directories_dict = {
    'project_root'          :   project_root,
    'dir_downloads'         :   get_downloads_folder(),
    'dir_data'              :   project_root / 'data',
    # data > raw 
    'dir_data_raw'                              :   str(project_root / 'data' / 'raw'),
    'dir_data_preprocessed'                     :   str(project_root / 'data' / 'preprocessed'),   
    'dir_data_harmonization'                    :   str(project_root / 'data' / 'harmonization'),
}