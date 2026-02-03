import os
from kozubenko.os import Parent


DEFINITIONS_PY                =  os.path.abspath(__file__)

PYTHON_ROOT_DIRECTORY         =  Parent(DEFINITIONS_PY)
PROJECT_ROOT_DIRECTORY        =  Parent(PYTHON_ROOT_DIRECTORY)

PYTHON_TESTS_DIRECTORY        =  os.path.join(PYTHON_ROOT_DIRECTORY, 'tests')

BIBLE_HTML                    =  os.path.join(PROJECT_ROOT_DIRECTORY, 'bible_html')
BIBLE_TXT                     =  os.path.join(PROJECT_ROOT_DIRECTORY, 'bible_txt')
BIBLE_TXT_NEW                 =  os.path.join(PYTHON_ROOT_DIRECTORY, 'bible_txt')
BIBLE_TXT_PARTIAL             =  os.path.join(PYTHON_ROOT_DIRECTORY, 'bible_txt_partial')
BIBLE_TXT_TO_MOVE             =  os.path.join(PYTHON_ROOT_DIRECTORY, 'bible_txt_to_move')

TEMP_DIR    =  os.path.join(PYTHON_ROOT_DIRECTORY, 'temp')
TEMP_OUTPUT =  os.path.join(PYTHON_ROOT_DIRECTORY, 'output.txt')


ALL_TRANSLATIONS = ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT', 'NIV', 'NET']


# ENV                   =  os.path.join(PROJECT_ROOT_DIRECTORY, '.env', '.env')