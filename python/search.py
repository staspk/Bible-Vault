""" 
Minor Text Corruptions (spacing, transpose errors, etc.)
files corrupted: 2375
files tested:    9016

Error Rate: 26%

"""

import os, re
from definitions import BIBLE_TXT as BIBLE_TXT_DIRECTORY
from kozubenko.print import Print


corrupted_files = {}
files = {}

def check_file(path, pattern) -> str|False:
    if path not in files: files[path]=True
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            for lineno, line in enumerate(file, 1):
                if pattern.search(line):
                    return path
    return False

def check_error(pattern):
    for root, dirs, files in os.walk(BIBLE_TXT_DIRECTORY):
        for name in files:
            path = os.path.join(root, name)
            if(check_file(path, pattern)):
                if(path not in corrupted_files):
                    corrupted_files[path] = True


check_error(re.compile(r',[A-Za-z]'))
Print.green(len(corrupted_files))

check_error(re.compile(r'\.[A-Za-z]'))
Print.green(len(corrupted_files))
Print.green(len(files))


# pattern = re.compile(r'.[A-Za-z]')

# for root, dirs, files in os.walk(BIBLE_TXT_DIRECTORY):
#     for name in files:
#         if name.lower().endswith('.txt'):
#             path = os.path.join(root, name)
#             with open(path, 'r', encoding='utf-8', errors='ignore') as f:
#                 for lineno, line in enumerate(f, 1):
#                     if pattern.search(line):
#                         print(f"{path}:{lineno}: {line.rstrip()}")