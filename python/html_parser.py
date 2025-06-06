import os
import re
from typing import Union

from bs4 import BeautifulSoup
from definitions import BIBLE_HTML, BIBLE_TXT
from kozubenko.os import File
from kozubenko.print import print_green, print_red, print_yellow
from models.Bible import BIBLE, Book, find_max_verse


class HTML:
    """
    The format the html arrives in when using simple get calls with Requests & BeautifulSoup target class: 'passage-text' 
    each next list includes all the elements of the lists preceding it
    """

    simple_html = ['KJV', 'RUSV']
    footnotes = ['RSV', 'NRT']
    references = ['NKJV', 'NASB', 'ESV', 'NRSV', 'NIV', 'NET', 'NRT']

def parse_html(book:Book, target_translations:Union[str, list[str]], one_pass = False):
    if type(target_translations) is str:
        target_translations = [target_translations]
    if type(target_translations) is not list:
        raise Exception(f'parse_html(): type(target_translations) must be of type str or list[str]. type(target_translations): {type(target_translations)}')
    
    for translation in target_translations:
        for chapter in range(2, book.chapters + 1):
            IN_HTML = File(BIBLE_HTML, translation, book.name, file=f'{chapter}.html')
            OUT_TXT = File(BIBLE_TXT, translation, book.name, file=f'{chapter}.txt')

            if not os.path.exists(IN_HTML):
                print_red(f'parse_html(): html file to parse does not exist. Skipping {book.name}:{chapter}. IN_HTML: {IN_HTML}')
            else:
                with open(IN_HTML, 'r', encoding='utf-8') as file:
                    html = file.read()
                html_array = re.split(r'(?=<div class="footnotes">)', html, maxsplit=1)         # note: using ?= is essentially: split before, and do not consume
                
                with open('./temporary.html', 'w', encoding='utf-8') as temp_file:
                    temp_file.write(html)

                print_yellow(html_array[0])
                
                pass

            if(one_pass):
                exit()


def just_parse_simple_html(book, chapter, html) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    lines = soup.get_text().splitlines()
    text = ''
    for line in lines:
        if(line != ''):
            text += line

    out_text = ''
    split_text = re.split(f'{chapter}\xa0', text, maxsplit=1)[1]

    max_verse = find_max_verse(book, chapter)
    for x_verse in range(1, max_verse+1):
        array = re.split(f' {x_verse + 1}\xa0', split_text, maxsplit=1)
        out_text += (array[0].strip())

        if(x_verse < max_verse):
            out_text += '\n'
            split_text = array[1]

    return out_text

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

def parse_footnotes_html(book:Book, target_translation:str, one_pass=False):
    for chapter in range(2, book.chapters + 1):
        IN_HTML = File(BIBLE_HTML, target_translation, book.name, file=f'{chapter}.html')
        OUT_TXT = File(BIBLE_TXT, target_translation, book.name, file=f'{chapter}.txt')

        if not os.path.exists(IN_HTML):
            raise Exception(f'parse_footnotes_html(): html file to parse does not exist. IN_HTML: {IN_HTML}')
        
        with open(IN_HTML, 'r', encoding='UTF-8') as file:
            html = file.read()

        split_html = html.split('<h4>Footnotes</h4>', 1)
        chapter_text = just_parse_simple_html(book, chapter, split_html[0])
        if(split_html.__len__ == 2):                                              # Footnotes section exists
            print_red(split_html[1])

        # soup = BeautifulSoup(html, 'html.parser')

        

        exit()

        lines = soup.get_text().splitlines()
        text = ''
        for line in lines:
            if(line):
                text += line

        print_green(text)

        if(one_pass):
            exit()

