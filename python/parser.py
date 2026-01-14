
"""
"Standard Form" (#3) [see: ./models/biblegateway/jeremiah-41-esv.txt]
    5996 chapters / 11890 total
    50.43%

"Poetry Form" (#2) [see: ./models/biblegateway/hosea-9-esv.txt]



Oddities:
    " " aka: 6/MSP, John 15 NRT, 2 occurences

"""
import re
from definitions import BIBLE_TXT_NEW
from kozubenko.os import File
from kozubenko.print import Print
from models import BibleChapters
from models.Bible import BIBLE
from models.text_forms.standard import StandardForm





def identify_psalm_form():
    translations = ['KJV', 'NASB', 'RSV', 'NKJV', 'NRSV']

    Bible = BibleChapters()
    for PTR in Bible.iterate_Bible():
        if PTR.book.name == BIBLE.PSALMS.name:
            continue
        for translation in translations:
            file = File(BIBLE_TXT_NEW, translation, PTR.book.name, f'{PTR.chapter}.txt')
            if file.exists():
                text = file.contents(encoding='UTF-8')

                left = text.split(str(PTR.chapter), 1)[0]
                if(left):
                    Print.yellow(f'{PTR.book} {PTR.chapter} [{translation}]')

def identify_standard_form(translations:list) -> BibleChapters:
    """standard_form (#3). Operation: ~3mins"""
    Chapters = BibleChapters(translations)
    for PTR in Chapters.iterate_Bible():
        expected_total_verses = PTR.book.total_verses(PTR.chapter)
        for translation in translations:
            file = File(BIBLE_TXT_NEW, translation, PTR.book.name, f'{PTR.chapter}.txt')
            if file.exists():
                text = file.contents(encoding='UTF-8')

                lines = re.findall(r'.+', text)     # any single character (except newline), one or more repetitions
                if lines.__len__() == expected_total_verses:
                    Chapters.mark(translation, PTR.index)
    return Chapters

def identify_poetry_form(translations:list) -> BibleChapters:
    """poetry_form (#2)"""
    StandardChapters:dict[str,set] = StandardForm.Chapters()





