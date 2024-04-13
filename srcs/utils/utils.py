import os
import shutil

def clear_directories(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def color_text(text, color):
    """
    Takes a text string and applies ANSI escape codes to color it magenta.

    Parameters:
    text (str): The text to color.
    color (str): The color to apply.
    
    Returns:
    str: The colored text.
    """
    if color == "magenta":
        return f"\x1B[35m{text}\x1B[0m"
    elif color == "green":
        return f"\x1B[32m{text}\x1B[0m"
    elif color == "red":
        return f"\x1B[31m{text}\x1B[0m"
    elif color == "blue":
        return f"\x1B[34m{text}\x1B[0m"
    elif color == "yellow":
        return f"\x1B[33m{text}\x1B[0m"
    elif color == "cyan":
        return f"\x1B[36m{text}\x1B[0m"
    elif color == "white":
        return f"\x1B[37m{text}\x1B[0m"
    elif color == "black":
        return f"\x1B[30m{text}\x1B[0m"
    else:
        return text

# Function to clear the terminal screen
def clear_screen():
    if os.name == 'nt': # For Windows
        os.system('cls')
    else:
        os.system('clear')

def print_banner():
    CUSTOMGPT_ASCII_ART = """
            ,o888888o.    8 8888      88    d888888o. 8888888 8888888888 ,o888888o.           ,8.       ,8.           ,o888888o.    8 888888888o 8888888 8888888888 
           8888     `88.  8 8888      88  .`8888:' `88.     8 8888    . 8888     `88.        ,888.     ,888.         8888     `88.  8 8888    `88.     8 8888       
        ,8 8888       `8. 8 8888      88  8.`8888.   Y8     8 8888   ,8 8888       `8b      .`8888.   .`8888.     ,8 8888       `8. 8 8888     `88     8 8888       
        88 8888           8 8888      88  `8.`8888.         8 8888   88 8888        `8b    ,8.`8888. ,8.`8888.    88 8888           8 8888     ,88     8 8888       
        88 8888           8 8888      88   `8.`8888.        8 8888   88 8888         88   ,8'8.`8888,8^8.`8888.   88 8888           8 8888.   ,88'     8 8888       
        88 8888           8 8888      88    `8.`8888.       8 8888   88 8888         88  ,8' `8.`8888' `8.`8888.  88 8888           8 888888888P'      8 8888       
        88 8888           8 8888      88     `8.`8888.      8 8888   88 8888        ,8P ,8'   `8.`88'   `8.`8888. 88 8888   8888888 8 8888             8 8888       
        `8 8888       .8' ` 8888     ,8P 8b   `8.`8888.     8 8888   `8 8888       ,8P ,8'     `8.`'     `8.`8888.`8 8888       .8' 8 8888             8 8888       
           8888     ,88'    8888   ,d8P  `8b.  ;8.`8888     8 8888    ` 8888     ,88' ,8'       `8        `8.`8888.  8888     ,88'  8 8888             8 8888       
            `8888888P'       `Y88888P'    `Y8888P ,88P'     8 8888       `8888888P'  ,8'         `         `8.`8888.  `8888888P'    8 8888             8 8888                

    """
    print(CUSTOMGPT_ASCII_ART)