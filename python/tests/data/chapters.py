from abc import ABC, abstractmethod
from typing import Iterator
from models.Bible import BIBLE
from models.IChapter import IChapter


type verse_num = int
type verse_text = str

class IVerseIterator(ABC):
    @abstractmethod
    def iterate_verses() -> Iterator[verse_num, verse_text]:
        pass

class IVerseTextIterator(ABC):
    @abstractmethod
    def iterate_verse_text() -> Iterator[verse_text]:
        pass

class Test_Chapters:
    """
    Hard-coded Bible Chapters that have passed a meticulous eye-test, for testing functions that load in chapter text.
    """
    @staticmethod
    def All() -> list[IVerseTextIterator]:
        return [
            NET_Psalms_42,
            NRT_1Chronicles_3
        ]
    
    @staticmethod
    def verse_order_edge_case_Chapter() -> IVerseIterator:
        return RSV_EXODUS_22

    @staticmethod
    def get(PTR:IChapter) -> IVerseTextIterator:
        if PTR.translation == 'NET' and PTR.book == BIBLE.PSALMS and PTR.chapter == 42:          return NET_Psalms_42
        if PTR.translation == 'NRT' and PTR.book == BIBLE.FIRST_CHRONICLES and PTR.chapter == 3: return NRT_1Chronicles_3

        raise Exception('chapter does not exist!')


class RSV_EXODUS_22(IVerseIterator):
    """
    Only (currently known) Chapter that transposes verses
        **verse order:** 1, 4, 2, 3, 5, 6, ...
    """
    def iterate_verses() -> Iterator[verse_num, verse_text]:
        yield 1, "“If a man steals an ox or a sheep, and kills it or sells it, he shall pay five oxen for an ox, and four sheep for a sheep. He shall make restitution; if he has nothing, then he shall be sold for his theft."

        yield 4, "If the stolen beast is found alive in his possession, whether it is an ox or an ass or a sheep, he shall pay double."

        yield 2, "“If a thief is found breaking in, and is struck so that he dies, there shall be no bloodguilt for him;"

        yield 3, "but if the sun has risen upon him, there shall be bloodguilt for him."

        yield 5, "“When a man causes a field or vineyard to be grazed over, or lets his beast loose and it feeds in another man’s field, he shall make restitution from the best in his own field and in his own vineyard."

        yield 6, "“When fire breaks out and catches in thorns so that the stacked grain or the standing grain or the field is consumed, he that kindled the fire shall make full restitution."

        yield 7, "“If a man delivers to his neighbor money or goods to keep, and it is stolen out of the man’s house, then, if the thief is found, he shall pay double."

        yield 8, "If the thief is not found, the owner of the house shall come near to God, to show whether or not he has put his hand to his neighbor’s goods."

        yield 9, "“For every breach of trust, whether it is for ox, for ass, for sheep, for clothing, or for any kind of lost thing, of which one says, ‘This is it,’ the case of both parties shall come before God; he whom God shall condemn shall pay double to his neighbor."

        yield 10, "“If a man delivers to his neighbor an ass or an ox or a sheep or any beast to keep, and it dies or is hurt or is driven away, without any one seeing it,"

        yield 11, "an oath by the Lord shall be between them both to see whether he has not put his hand to his neighbor’s property; and the owner shall accept the oath, and he shall not make restitution."

        yield 12, "But if it is stolen from him, he shall make restitution to its owner."

        yield 13, "If it is torn by beasts, let him bring it as evidence; he shall not make restitution for what has been torn."

        yield 14, "“If a man borrows anything of his neighbor, and it is hurt or dies, the owner not being with it, he shall make full restitution."

        yield 15, "If the owner was with it, he shall not make restitution; if it was hired, it came for its hire."

        yield 16, "“If a man seduces a virgin who is not betrothed, and lies with her, he shall give the marriage present for her, and make her his wife."

        yield 17, "If her father utterly refuses to give her to him, he shall pay money equivalent to the marriage present for virgins."

        yield 18, "“You shall not permit a sorceress to live."

        yield 19, "“Whoever lies with a beast shall be put to death."

        yield 20, "“Whoever sacrifices to any god, save to the Lord only, shall be utterly destroyed."

        yield 21, "“You shall not wrong a stranger or oppress him, for you were strangers in the land of Egypt."

        yield 22, "You shall not afflict any widow or orphan."

        yield 23, "If you do afflict them, and they cry out to me, I will surely hear their cry;"

        yield 24, "and my wrath will burn, and I will kill you with the sword, and your wives shall become widows and your children fatherless."

        yield 25, "“If you lend money to any of my people with you who is poor, you shall not be to him as a creditor, and you shall not exact interest from him."

        yield 26, "If ever you take your neighbor’s garment in pledge, you shall restore it to him before the sun goes down;"

        yield 27, "for that is his only covering, it is his mantle for his body; in what else shall he sleep? And if he cries to me, I will hear, for I am compassionate."

        yield 28, "“You shall not revile God, nor curse a ruler of your people."

        yield 29, "“You shall not delay to offer from the fulness of your harvest and from the outflow of your presses. “The first-born of your sons you shall give to me."

        yield 30, "You shall do likewise with your oxen and with your sheep: seven days it shall be with its dam; on the eighth day you shall give it to me."

        yield 31, "“You shall be men consecrated to me; therefore you shall not eat any flesh that is torn by beasts in the field; you shall cast it to the dogs."


class NET_Psalms_42(IVerseTextIterator):

    def iterate_verse_text() -> Iterator[verse_text]:
        yield 'As a deer longs for streams of water,\nso I long for you, O God!'

        yield 'I thirst for God,\nfor the living God.\nI say, “When will I be able to go and appear in God’s presence?”'

        yield 'I cannot eat; I weep day and night.\nAll day long they say to me, “Where is your God?”'

        yield 'I will remember and weep.\nFor I was once walking along with the great throng to the temple of God,\nshouting and giving thanks along with the crowd as we celebrated the holy festival.'

        yield 'Why are you depressed, O my soul?\nWhy are you upset?\nWait for God!\nFor I will again give thanks\nto my God for his saving intervention.'

        yield 'I am depressed,\nso I will pray to you while in the region of the upper Jordan,\nfrom Hermon, from Mount Mizar.'

        yield 'One deep stream calls out to another at the sound of your waterfalls;\nall your billows and waves overwhelm me.'

        yield 'By day the Lord decrees his loyal love,\nand by night he gives me a song,\na prayer to the God of my life.'

        yield 'I will pray to God, my high ridge:\n“Why do you ignore me?\nWhy must I walk around mourning\nbecause my enemies oppress me?”'

        yield 'My enemies’ taunts cut me to the bone,\nas they say to me all day long, “Where is your God?”'

        yield 'Why are you depressed, O my soul?\nWhy are you upset?\nWait for God!\nFor I will again give thanks\nto my God for his saving intervention.'

class NRT_1Chronicles_3(IVerseTextIterator):

    def iterate_verse_text() -> Iterator[verse_text]:
        yield 'Вот сыновья Давида, которые родились у него в Хевроне:\nпервенец Амнон от изреельтянки Ахиноамь;\nвторой сын – Даниил от кармилитянки Авигайль;'

        yield 'третий – Авессалом, сын Маахи, дочери Талмая, царя Гешура;\nчетвертый – Адония, сын Аггифы;'

        yield 'пятый – Шефатия от Авиталы;\nшестой – Итреам от его жены Эглы.'

        yield 'Шестеро сыновей родилось у Давида в Хевроне, где он правил семь лет и шесть месяцев.\nВ Иерусалиме он правил тридцать три года,'

        yield 'и вот дети, которые родились у него в Иерусалиме:\nШима, Шовав, Нафан и Соломон – четверо от Вирсавии, дочери Аммиила.'

        yield 'Затем: Ивхар, Элишама, Элифелет,'

        yield 'Ногах, Нефег, Иафия,'

        yield 'Элишама, Элиада и Элифелет – девять сыновей.'

        yield 'Все это – сыновья Давида, не считая сыновей от наложниц. А сестрой их была Фамарь.\nЦари Иуды после Давида'

        yield 'Потомки Соломона: Ровоам,\nАвия, его сын,\nАса, его сын,\nИосафат, его сын,'

        yield 'Иорам, его сын,\nОхозия, его сын,\nИоаш, его сын,'

        yield 'Амасия, его сын,\nАзария, его сын,\nИотам, его сын,'

        yield 'Ахаз, его сын,\nЕзекия, его сын,\nМанассия, его сын,'

        yield 'Амон, его сын,\nИосия, его сын.'

        yield 'Сыновья Иосии:\nпервенец Иоханан,\nвторой сын – Иоаким,\nтретий – Цедекия,\nчетвертый – Шаллум.'

        yield 'Потомки Иоакима:\nИехония, его сын,\nЦедекия, его сын.\nЦарская линия после пленения'

        yield 'Потомки Иехонии, который был пленником:\nАсир, Шеалтиил, его сын,'

        yield 'Малкирам, Педая, Шенацар, Иезекия, Гошама, Недавия.'

        yield 'Сыновья Педаи:\nЗоровавель, Шимей.\nСыновья Зоровавеля:\nМешуллам и Ханания;\nсестрой их была Шеломит;'

        yield 'Хашшува, Огел, Берехия, Хасадия, Иушав-Хесед – еще пятеро.'

        yield 'Потомки Ханании:\nПелатия и Исаия, Рефая, его сын, Арнан, его сын, Авдий, его сын, Шекания, его сын.'

        yield 'Сын Шекании:\nШемая.\nСыновья Шемаи:\nХаттуш, Игал, Бариах, Неария, Шафат – шестеро.'

        yield 'Сыновья Неарии:\nЭлиоэнай, Езекия, Азрикам – трое.'

        yield 'Сыновья Элиоэная:\nГодавия, Элиашив, Фелаия, Аккув, Иоханан, Делая и Анани – семеро.'

