import os
from kozubenko.os import File, Parent


DEFINITIONS_PY                =  os.path.abspath(__file__)

PYTHON_ROOT_DIRECTORY         =  Parent(DEFINITIONS_PY)
PROJECT_ROOT_DIRECTORY        =  Parent(PYTHON_ROOT_DIRECTORY)

PYTHON_DATA_DIRECTORY         =  os.path.join(PYTHON_ROOT_DIRECTORY, 'data')
PYTHON_TESTS_DIRECTORY        =  os.path.join(PYTHON_ROOT_DIRECTORY, 'tests')

BIBLE_HTML                    =  os.path.join(PROJECT_ROOT_DIRECTORY, 'bible_html')
BIBLE_TXT                     =  os.path.join(PROJECT_ROOT_DIRECTORY, 'bible_txt')
BIBLE_TXT_NEW                 =  os.path.join(PYTHON_ROOT_DIRECTORY, 'bible_txt')
BIBLE_TXT_PARTIAL             =  os.path.join(PYTHON_ROOT_DIRECTORY, 'bible_txt_partial')
BIBLE_TXT_CURRENT             =  os.path.join(PYTHON_ROOT_DIRECTORY, 'bible_txt_current')
BIBLE_TXT_POSTPONED           =  os.path.join(PYTHON_ROOT_DIRECTORY, 'bible_txt_postponed')

TEMP_DIR    =  os.path.join(PYTHON_ROOT_DIRECTORY, 'temp')
TEMP_OUTPUT =  os.path.join(PYTHON_ROOT_DIRECTORY, 'output.txt')


ALL_TRANSLATIONS = ['KJV', 'NASB', 'RSV', 'RUSV', 'NKJV', 'ESV', 'NRSV', 'NRT', 'NIV', 'NET']

BIBLE = File(PYTHON_DATA_DIRECTORY, "bible.bin")   # bible text as binary file. See: ./factory.py -> construct_Bible()