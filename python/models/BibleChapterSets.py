import random
from typing import Iterator, Self
from kozubenko.os import File
from kozubenko.random import random_pop
from kozubenko.print import Print
from models.Bible import BIBLE, Book, Chapter
from definitions import ALL_TRANSLATIONS, BIBLE_TXT_NEW, PYTHON_TESTS_DIRECTORY


translation = str
chapter_index = int
BibleChapterSet = dict[translation, set[chapter_index]]

def Protestant_Set() -> set[int]:
    """ **Returns:** `set[chapter_index]` : {1-1189} """
    return set(range(1, BIBLE.TOTAL_CHAPTERS+1))


class BibleChapterSets:
    """
    `BibleChapterSets(set)` -> Init with pre-existing `BibleChapterSet`

    `BibleChapterSets.From(list[translation:str]])` -> Init full set {1-1189} for every `translation`
    
    **Intended For:**
    - Build a map, set of sets of the Bible by `Chapter.index`, with intent to randomly iterate/mark.
    - Mark ability does NOT depend on `self.set` - init with: `{}`
    """
    @property
    def total(self) -> int: return sum(len(set) for set in self.set.values())
    @property
    def total_marked(self) -> int: return sum(len(set) for set in self.marked.values())

    def __init__(self, chapter_set:dict[translation, set[chapter_index]]):
        self.set = chapter_set
        self.marked:dict[str, set[int]] = {}
        for translation in chapter_set.keys():
            self.marked[translation] = set()

    def From(translations:list[str]=ALL_TRANSLATIONS) -> BibleChapterSets:
        """ static constructor """
        return BibleChapterSets({translation:Protestant_Set() for translation in translations})
    
    def mark(self, chapter:Chapter):
        """ """
        translation = chapter.translation
        chapter_index = chapter.index

        if translation in self.marked.keys(): self.marked[translation].add(chapter_index)
        else:                                 self.marked[translation] = set([chapter_index])

    def iterate(self, alternate_set:BibleChapterSet=None) -> Iterator[Chapter]:
        """
        **Yields:**
            Pops a random "chapter_index" from `self.set`, yielding corresponding `Chapter` including `translation`.
        
        **How to Use:**
        ```python
        Chapters = StandardForm.Inverse()
        for PTR in Chapters.iterate():
        ```
        """
        set_to_iterate = self.set
        if alternate_set is not None:
            set_to_iterate = alternate_set

        sets = {key:value.copy() for key,value in set_to_iterate.items() if len(value) > 0}
        left = sum(len(set) for set in sets.values())

        while left > 0:
            translation = random.choice(tuple(sets.keys()))
            chapter_index = random_pop(sets[translation])
            PTR:Chapter = BIBLE.Chapter(chapter_index)
            yield Chapter(PTR.book, PTR.chapter, PTR.index, translation)

            left -= 1
            if sets[translation].__len__() == 0:
                del sets[translation]

    def ratio(self) -> str:
        """
        `marked / total_chapters`
        
        total_chapters = `BIBLE.TOTAL_CHAPTERS` * `len(marked.values())`
        """
        marked = 0; total_chapters = 0
        for chapters in self.marked.values():
            marked += len(chapters)
        for chapters in self.set.values():
            total_chapters += len(chapters)
            
        return f'{marked}/{total_chapters}'

    def Save_Report(self, file_name:str) -> Self:
        """ Saves `self.marked` """
        report = ""
        for translation,marked_chapters in self.set.items():
            report += f'{translation} = {str(marked_chapters)}\n'
        report += f'Ratio: {self.total_marked}/{self.total}'

        File(PYTHON_TESTS_DIRECTORY, f'{file_name}').save(report, encoding='UTF-8')
        Print.yellow(f'{file_name}: {self.total_marked}')

        return self

    def Subtract(
        A:dict[translation, set[chapter_index]],
        B:dict[translation, set[chapter_index]]
    ) -> BibleChapterSets:
        sets = {key:value.copy() for key,value in A.items()}

        for translation in B.keys():
            if translation in sets:
                sets[translation] = sets[translation] - B[translation]

        return BibleChapterSets(sets)
