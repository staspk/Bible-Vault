from kozubenko.cls import class_attributes
from models.BibleChapters import Protestant_Set


class ScrapeFail:
    NASB = {1026, 964, 1062, 966, 1033, 1002, 972, 1042, 947, 946, 1046, 952}
    RSV = {1026, 387, 1033, 1042, 1046, 1062, 941, 946, 947, 950, 952, 964, 966, 72, 968, 972, 990, 995, 996, 997, 1002, 1147}
    ESV = {1026, 964, 996, 1062, 966, 968, 1033, 1002, 972, 941, 1042, 947, 946, 1046, 952, 990}
    NRSV = {1026, 964, 996, 1062, 966, 968, 1033, 1002, 231, 972, 1042, 947, 946, 1046, 952, 1147, 990}
    NET = {1026, 964, 996, 1062, 966, 968, 1033, 1002, 972, 946, 947, 1046, 952, 990}

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