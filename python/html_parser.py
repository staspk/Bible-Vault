import os
import re
from typing import Union

from bs4 import BeautifulSoup
from definitions import BIBLE_HTML, BIBLE_TXT
from kozubenko.os import File
from kozubenko.print import print_red
from models.Bible import BIBLE, Book, find_max_verse


class HTML:
    """
    The format the html arrives in when using simple get calls with Requests & BeautifulSoup target class: 'passage-text' 
    each next list includes all the elements of the lists preceding it
    """

    simple_html = ['KJV', 'RUSV']
    footnotes = ['RSV', 'NRT']
    references = ['NKJV', 'NASB', 'ESV', 'NRSV', 'NIV', 'NET', 'NRT']

def parse_html(book:Book, target_translations:Union[str, list[str]]):
    if type(target_translations) is str:
        target_translations = [target_translations]

    for translation in target_translations:
        if translation in HTML.simple_html:
            parse_simple_html(book, translation)
        if translation in HTML.footnotes:
            parse_footnotes_html(book, translation, one_pass=True)

def parse_footnotes_html(book:Book, target_translation:str, one_pass=False):
    for chapter in range(1, book.chapters + 1):
        IN_HTML = File(BIBLE_HTML, target_translation, book.name, file=f'{chapter}.html')
        OUT_TXT = File(BIBLE_TXT, target_translation, book.name, file=f'{chapter}.txt')

        if not os.path.exists(IN_HTML):
            raise Exception(f'parse_footnotes_html(): html file to parse does not exist. IN_HTML: {IN_HTML}')
        
        raise Exception('not implemented yet')

def parse_simple_html(book:Book, target_translation:str, one_pass=False):
    for chapter in range(1, book.chapters + 1):
        IN_HTML = File(BIBLE_HTML, target_translation, book.name, file=f'{chapter}.html')
        OUT_TXT = File(BIBLE_TXT, target_translation, book.name, file=f'{chapter}.txt')

        if not os.path.exists(IN_HTML):
            raise Exception(f'parse_simple_html(): html file to parse does not exist. IN_HTML: {IN_HTML}')
        
        with open(IN_HTML, 'r', encoding='utf-8') as file:
            html = file.read()

        soup = BeautifulSoup(html, 'html.parser')
        lines = soup.get_text().splitlines()
        text = ''
        for line in lines:
            if(line):
                text += line

        with open(OUT_TXT, 'w', encoding='utf-8') as out:
            split_text = re.split(f'{chapter}\xa0', text, maxsplit=1)[1]

            max_verse = find_max_verse(book, chapter)
            for x_verse in range(1, max_verse+1):
                array = re.split(f' {x_verse + 1}\xa0', split_text, maxsplit=1)
                out.write(array[0].strip())

                if(x_verse < max_verse):
                    out.write('\n')
                    split_text = array[1]
        
        if(one_pass):
            return
        


