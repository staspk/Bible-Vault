import os
from kozubenko.os import Parent


DEFINITIONS_PY                =  os.path.abspath(__file__)

PYTHON_ROOT_DIRECTORY         =  Parent(DEFINITIONS_PY)
PROJECT_ROOT_DIRECTORY        =  Parent(PYTHON_ROOT_DIRECTORY)

REPORTS_DIRECTORY             =  os.path.join(PYTHON_ROOT_DIRECTORY, 'reports')

TEMP_DIRECTORY                =  os.path.join(PROJECT_ROOT_DIRECTORY, 'temp')
JSONS_DIRECTORY               =  os.path.join(PROJECT_ROOT_DIRECTORY, 'jsons')

BIBLE_JSON                    =  os.path.join(JSONS_DIRECTORY, 'bible.json')

TEMPORARY_HTML                =  os.path.join(PYTHON_ROOT_DIRECTORY, 'temporary.html')

BIBLE_HTML                    =  os.path.join(PROJECT_ROOT_DIRECTORY, 'bible_html')
BIBLE_TXT                     =  os.path.join(PROJECT_ROOT_DIRECTORY, 'bible_txt')
BIBLE_TXT_NEW                 =  os.path.join(PYTHON_ROOT_DIRECTORY, 'bible_txt')

BIBLE_NUMERICAL_MAP           =  os.path.join(PROJECT_ROOT_DIRECTORY, 'bible_numerical_map')

TEMP_OUTPUT                   =  os.path.join(PYTHON_ROOT_DIRECTORY, 'output.txt')


# ENV                   =  os.path.join(PROJECT_ROOT_DIRECTORY, '.env', '.env')
# TEMP_DIR              =  os.path.join(PROJECT_ROOT_DIRECTORY, 'temp')