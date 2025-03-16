import json
import re
from kozubenko.utils import print_red

def load_json(file:str) -> any:
    """
    `print(json.dumps(data, indent=4))`
    """
    try:
        with open(file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print_red(f'Error in kozubenko.io.load_json(file:str):\n{e}')
        raise e
    
def load_file(file:str) -> str:
    try:
        with open(file, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print_red(f'Error in kozubenko.io.load_file(file:str):\n{e}')
        raise e
    

def remove_html_tags(text):
    # The regular expression '<.*?>' matches any substring that starts with '<' and ends with '>',
    # using a non-greedy match, i.e. the least amount of chars between < > is the goal
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text