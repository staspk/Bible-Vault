from abc import ABC, abstractmethod
from typing import Iterator
from models.Bible import BIBLE
from models.IChapter import IChapter


class IChapterIterator(ABC):
    @abstractmethod
    def iterate_verses() -> Iterator[str]: pass


class chapters:
    """
    Some hard-coded chapters to test functions that read chapters in.
    """
    def all() -> list[IChapterIterator]:
        return [
            NET_Psalms_42,
            NRT_1Chronicles_3
        ]

    def get(PTR:IChapter) -> IChapterIterator:
        if PTR.translation == 'NET' and PTR.book == BIBLE.PSALMS and PTR.chapter == 42: return NET_Psalms_42
        if PTR.translation == 'NRT' and PTR.book == BIBLE.FIRST_CHRONICLES and PTR.chapter == 3: return NRT_1Chronicles_3

        raise Exception('chapter does not exist!')


class NET_Psalms_42(IChapterIterator):

    def iterate_verses() -> Iterator[str]:
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

class NRT_1Chronicles_3(IChapterIterator):

    def iterate_verses() -> Iterator[str]:
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

