from typing import Iterator
from kozubenko.cls import class_attributes
from kozubenko.random import random_pop
from models.Bible import Chapter
from models.BibleChapters import Protestant_Set


translation = str
chapter_index = int

class MissingVerses:
    """ 189 chapters """
    KJV = set()
    NASB = {1026, 964, 1062, 966, 1033, 1002, 972, 1042, 947, 946, 1046, 952}
    RSV = {1026, 387, 1033, 1042, 1046, 1062, 941, 946, 947, 950, 952, 964, 966, 72, 968, 972, 990, 995, 996, 997, 1002, 1147}
    RUSV = set()
    NKJV = set()
    ESV = {1026, 964, 996, 966, 1062, 968, 1033, 1002, 972, 941, 1042, 946, 947, 1046, 952, 990}
    NRSV = {1026, 515, 1033, 1042, 1046, 1062, 946, 947, 952, 1091, 964, 966, 968, 972, 990, 481, 483, 996, 486, 231, 487, 1002, 500, 1147}
    NRT = {513, 515, 516, 518, 519, 520, 522, 523, 524, 1037, 528, 529, 530, 533, 534, 537, 538, 544, 547, 549, 551, 552, 556, 558, 559, 561, 564, 567, 568, 570, 572, 574, 575, 577, 1089, 1091, 580, 584, 585, 587, 590, 593, 594, 597, 600, 602, 604, 608, 610, 614, 615, 104, 617, 618, 619, 623, 625, 129, 146, 664, 672, 677, 682, 193, 259, 854, 875, 890, 477, 488, 490, 492, 496, 497, 500, 503, 505, 509}
    NIV = {1026, 515, 1033, 1046, 1062, 946, 947, 952, 964, 966, 968, 972, 597, 990, 481, 483, 484, 996, 485, 487, 496, 500}
    NET = {1026, 1091, 964, 996, 966, 1062, 968, 1033, 1002, 972, 946, 947, 1046, 952, 990}

    @classmethod
    def Chapters(cls) -> dict[str,set]:
        """ **Returns:** `dict[translation, chapters]` """
        dict:dict[str,set] = {}
        for key,value in class_attributes(cls):
            if value.__len__() > 0:
                dict[key] = value
        return dict
    
    @classmethod
    def Inverse(cls) -> dict[str,set]:
        """ **Returns:** `dict[translation, chapters]` """
        remaining = {}
        StandardChapters:dict[str,set] = cls.Chapters()
        for translation in StandardChapters.keys():
            remaining[translation] = Protestant_Set() - StandardChapters[translation]
        return remaining
    
    @classmethod
    def iterate(cls) -> Iterator[tuple[list[translation], Chapter]]:
        """  """
        dict:dict[chapter_index,list[translation]] = {}

        for translation,set in cls.Chapters().items():
            for i in range(set.__len__()):
                chapter_index = set.pop()
                if chapter_index in dict: dict[chapter_index].append(translation)
                else: dict[chapter_index] = [translation]
        
        for chapter_index,translation in dict.items():
            yield (translation, Chapter.From(chapter_index))