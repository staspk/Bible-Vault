from models.IBibleChapterSet import IBibleChapterSet


class abnormal_verse_count_Chapters(IBibleChapterSet):
    """
    NOTE: 8 chapters added manually into `bible_txt` without tranformation (standardizing missing verses). See fossil record below for which ones...
    NOTE: We manually standardized/forced in the NIV chapters...need to add to this set!
    """
    KJV = {1166}
    NASB = {1026, 964, 966, 1062, 1033, 1002, 972, 1042, 947, 946, 1046, 952}
    RSV = {1026, 387, 1033, 1042, 1046, 1062, 941, 946, 947, 950, 952, 964, 966, 968, 72, 972, 990, 995, 996, 997, 1002, 1147}
    RUSV = {1166}
    NKJV = {1166}
    ESV = {1026, 996, 964, 1062, 966, 968, 1033, 1002, 972, 941, 1042, 947, 946, 1046, 952, 990}
    NRSV = {1026, 1033, 1042, 1046, 1179, 1062, 946, 947, 952, 1091, 964, 966, 968, 972, 990, 996, 231, 1002, 1147}
    NRT = {1091}
    NIV = set()
    NET = {1026, 1091, 964, 996, 1062, 966, 968, 1033, 1002, 972, 946, 947, 1046, 952, 1179, 990}







# ----------------------------------------------------------
#   FOSSIL RECORD - necessary, see above docstring for why
# ----------------------------------------------------------
# if self.book.name == '2 Corinthians' and self.chapter == 13 and self.translation in ('NRSV', 'NRT', 'NET'): return 13   # usually: 14
# if self.book.name == '3 John' and self.chapter == 1 and self.translation in ('KJV', 'NKJV', 'RUSV'): return 14   # usually: 15
# if self.book.name == 'Revelation' and self.chapter == 12 and self.translation in ('NRSV', 'NET'): return 18   # usually: 17

# ---------------------------------------------------------------------------------------

# Expanded_Chapters_abnormal_verse_count = BibleChapterSets.From()
# for PTR in Chapters_abnormal_verse_count.Chapters().iterate():
#     Expanded_Chapters_abnormal_verse_count.mark(PTR)

# Print.red(Expanded_Chapters_abnormal_verse_count.total_marked)

# for translation in ['NRSV', 'NRT', 'NET']:
#     Expanded_Chapters_abnormal_verse_count.mark(Chapter(BIBLE.SECOND_CORINTHIANS, 13, translation=translation))

# for translation in ['KJV', 'NKJV', 'RUSV']:
#     Expanded_Chapters_abnormal_verse_count.mark(Chapter(BIBLE.THIRD_JOHN, 1, translation=translation))

# for translation in ['NRSV', 'NET']:
#     Expanded_Chapters_abnormal_verse_count.mark(Chapter(BIBLE.REVELATION, 12, translation=translation))

# Print.red(Expanded_Chapters_abnormal_verse_count.total_marked)

# Expanded_Chapters_abnormal_verse_count.Save_Report('Chapters_with_abnormal_verse_count')

