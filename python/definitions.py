import os


DEFINITIONS_PY_ABSOLUTE_PATH  =  os.path.abspath(__file__)

PYTHON_ROOT_DIRECTORY         =  os.path.dirname(DEFINITIONS_PY_ABSOLUTE_PATH)      # os.path.dirname(abs_path) => Go up one level
PROJECT_ROOT_DIRECTORY        =  os.path.dirname(PYTHON_ROOT_DIRECTORY)

JSONS_DIRECTORY               =  os.path.join(PROJECT_ROOT_DIRECTORY, 'jsons')



# ENV                   =  os.path.join(PROJECT_ROOT_DIRECTORY, '.env', '.env')
# TEMP_DIR              =  os.path.join(PROJECT_ROOT_DIRECTORY, 'temp')