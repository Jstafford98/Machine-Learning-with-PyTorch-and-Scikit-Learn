''' utility script for moving images from the machine-learning book folder to my Obsidian folder for note taking '''

import shutil
from pathlib import Path
from loguru import logger

def copy_file(current_location : Path, new_location : Path, check_exists : bool = True) -> None :
    ''' If the new_location does not exist, copy file from current_location to there '''
    
    if check_exists and new_location.is_file():
        logger.warning(f'{new_location} exists. Skipping.')
        return
    
    logger.info(f'{new_location} does not exist, copying file.')
    shutil.copyfile(current_location, new_location)
    
def parse_filename(filename : str) -> tuple[int, int, int | None] | None :
    ''' 
        extracts the chapter, section, and subsection from a filename where applicable
        and returns them as integers
    '''
    
    parts = file.name.rstrip('.png').split('_')
    total_parts = len(parts)
    
    if total_parts not in range(2, 4):
        logger.warning(f'Skipping {file}')
        return None
    
    parts = map(int, parts)
    return tuple(parts) if total_parts == 3 else (*parts, None)

def build_new_filename(
    chapter : int, 
    section : int, 
    subsection : int | None = None
) -> str :
    ''' 
        Takes in the chapter, section, and subsection annotations for a PNG file name,
        cleans and standardizes them, and returns a new filename following standard
        file naming conventions
    '''
    
    new_file = f'{str(chapter).rjust(2, "0")}_{str(section).rjust(2, "0")}'
    if subsection is not None:
        new_file += f'_{str(subsection).rjust(2, "0")}'
    return f'{new_file}.png'

def parse_and_move_file(current_location : Path, new_directory : Path) -> None :
    
    if not current_location.is_file() or not new_directory.is_dir():
        logger.exception("Current location must be an existing file and new_directory must be an existing directory.")
    
    parts = parse_filename(current_location)
    if parts is None:
        return
    
    new_file = build_new_filename(*parts)
    
    new_file = new_directory / new_file
    
    copy_file(current_location, new_file, check_exists=True)

if __name__ == '__main__':
    
    root = Path('machine-learning-book-main')
    move_dir = Path(r'..\..\..\Documents\Obsidian Notes\Images\Machine Learning with PyTorch and Sklearn Images')

    assert root.is_dir()
    assert move_dir.is_dir()

    for file in root.rglob('figures/*.png'):
        try:
            parse_and_move_file(file, move_dir)        
        except Exception as e:
            print(f'Unexpected error while parsing {file}: {e}. Skipping for now.')
        
