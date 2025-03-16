import os


DEFINITIONS_PY                =  os.path.abspath(__file__)                              # absolute path:  ...\Bible-Vault\python\definitions.py

PYTHON_ROOT_DIRECTORY         =  os.path.dirname(DEFINITIONS_PY)                        # absolute path:  ...\Bible-Vault\python
PROJECT_ROOT_DIRECTORY        =  os.path.dirname(PYTHON_ROOT_DIRECTORY)                 # absolute path:  ...\Bible-Vault

TEMP_DIRECTORY                =  os.path.join(PROJECT_ROOT_DIRECTORY, 'temp')
JSONS_DIRECTORY               =  os.path.join(PROJECT_ROOT_DIRECTORY, 'jsons')

BIBLE_JSON                    =  os.path.join(JSONS_DIRECTORY, 'bible.json')

TEMPORARY_HTML                =  os.path.join(PYTHON_ROOT_DIRECTORY, 'temporary.html')

BIBLE_HTML                    =  os.path.join(PROJECT_ROOT_DIRECTORY, 'bible_html')
BIBLE_TXT                     =  os.path.join(PROJECT_ROOT_DIRECTORY, 'bible_txt')



# ENV                   =  os.path.join(PROJECT_ROOT_DIRECTORY, '.env', '.env')
# TEMP_DIR              =  os.path.join(PROJECT_ROOT_DIRECTORY, 'temp')