import os
import re

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


def parse_simple_html(book:Book, target_translation, one_pass=False):
    for chapter in range(1, book.chapters + 1):
        IN_HTML = File(BIBLE_HTML, target_translation, book.name, file=f'{chapter}.html')
        OUT_TXT = File(BIBLE_TXT, target_translation, book.name, file=f'{chapter}.txt')

        if not os.path.exists(IN_HTML):
            raise Exception(f'parse_simple_html(): IN_HTML path does not exist: {IN_HTML}')
        
        with open(IN_HTML, 'r', encoding='utf-8') as file:
            html = file.read()

        soup = BeautifulSoup(html, 'html.parser')
        lines = soup.get_text().splitlines()
        text = ''
        for line in lines:
            if(line):
                text += line

        with open(OUT_TXT, 'w', encoding='utf-8') as out:
            split_text = re.split(f'1\xa0', text, maxsplit=1)[1]

            max_verse = find_max_verse(BIBLE(chapter), chapter)
            for x_verse in range(1, max_verse+1):
                array = re.split(f' {x_verse + 1}\xa0', split_text, maxsplit=1)
                out.write(array[0].strip())

                if(x_verse < max_verse):
                    out.write('\n')
                    split_text = array[1]
        
        if(one_pass):
            return
        


