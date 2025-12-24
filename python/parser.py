
"""
Question #1:
    Are there any non-Psalm chapters in form #4?


Observations:
    All chapters have

"""
import random
from typing import Generator
from definitions import BIBLE_TXT_NEW
from kozubenko.os import File
from kozubenko.print import Print
from models.Bible import BIBLE, ChapterPtr, Iterate_Bible_Chapters


class BibleChapters:  
    def __init__(self):
        self.set = set(range(1, 1190))
        self.marked = set()

    def mark(self, ptr:ChapterPtr):
        self.marked(ptr.index)

    def next_random(self) -> Generator[ChapterPtr]:
        """
        **How to Use:**
        ```python
        for PTR in BibleChapters().next_random():
        ```
        """
        while self.set.__len__() > 0:
            chapter:int = random.choice(tuple(self.set))
            self.set.remove(chapter)
            yield BIBLE.ChaptersMap(chapter)
        

translations = ['KJV', 'NASB', 'RSV', 'NKJV', 'NRSV']

def identify_psalm_form():
    Bible = BibleChapters()
    for PTR in Bible.next_random():
        if PTR.book.name == BIBLE.PSALMS.name:
            continue
        for translation in translations:
            file = File(BIBLE_TXT_NEW, translation, PTR.book.name, f'{PTR.chapter}.txt')
            if file.exists():
                text = file.contents(encoding='UTF-8')

                left = text.split(str(PTR.chapter), 1)[0]
                if(left):
                    Print.yellow(f'{PTR.book} {PTR.chapter} [{translation}]')
