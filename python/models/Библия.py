from dataclasses import dataclass
from enum import Enum

class Книги(Enum):
    БЫТИЕ                  =  1
    ИСХОД                  =  2
    ЛЕВИТ                  =  3
    ЧИСЛА                  =  4
    ВТОРОЗАКОНИЕ           =  5
    ИИСУСA_НАВИНA          =  6
    КНИГА_СУДЕЙ            =  7
    РУФЬ                   =  8
    ПЕРВОЯ_ЦАРСТВA         =  9
    ВТОРОЯ_ЦАРСТВA         =  10
    ТРЕТЬЯ_ЦАРСТВA         =  11
    ЧЕТВЕРТОЯ_ЦАРСТВА      =  12
    ПЕРВОЯ_ПАРАЛИПОМЕНОН   =  13
    ВТОРОЯ_ПАРАЛИПОМЕНОН   =  14
    ЕЗДРА                  =  15
    НЕЕМИЯ                 =  16
    ЕСФИРЬ                 =  17
    ИОВ                    =  18
    ПСАЛТИРЬ               =  19
    ПРИТЧИ_СОЛОМОНОВЫ      =  20
    ЕККЛЕСИАСТ             =  21
    ПЕСНЬ_ПЕСНЕЙ           =  22
    ИСАИЯ                  =  23
    ИЕРЕМИЯ                =  24
    ИЕЗЕКИИЛЬ              =  26
    ПЛАЧ_ИЕРЕМИИ           =  25
    ДАНИИЛ                 =  27
    ОСИЯ                   =  28
    ИОИЛЬ                  =  29
    АМОС                   =  30
    АВДИЙ                  =  31
    ИОНА                   =  32
    МИХЕЙ                  =  33
    НАУМ                   =  34
    АВВАКУМ                =  35
    СОФОНИЯ                =  36
    АГГЕЙ                  =  37
    ЗАХАРИЯ                =  38
    МАЛАХИЯ                =  39
    МАТФЕЯ                 =  40
    МАРКА                  =  41
    ЛУКИ                   =  42
    ИОНАННА                =  43
    ДЕЯНИЯ_АПОСТОЛОВ       =  44
    РИМЛЯНАМ               =  45
    ПЕРВОЕ_КОРИНФЯНАМ      =  46
    ВТОРОЕ_КОРИНФЯНАМ      =  47
    ГАЛАТАМ                =  48
    ЕФЕСЯНАМ               =  49
    ФИЛИППИЙЦАМ            =  50
    КОЛОССЯНАМ             =  51
    ПЕРВОЕ_ФЕССАЛОНИКИЙЦАМ =  52
    ВТОРОЕ_ФЕССАЛОНИКИЙЦАМ =  53
    ПЕРВОЕ_ТИМОФЕЮ         =  54
    ВТОРОЕ_ТИМОФЕЮ         =  55
    ТИТУ                   =  56
    ФИЛИМОНУ               =  57
    ЕВРЕЯМ                 =  58
    ИАКОВА                 =  59
    ПЕРВОЕ_ПЕТРА           =  60
    ВТОРОЕ_ПЕТРА           =  61
    ПЕРВОЕ_ИОАННА          =  62
    ВТОРОЕ_ИОАННА          =  63
    ТРЕТИЕ_ИОАННА          =  64
    ИУДА                   =  65
    ОТКРОВЕНИЕ             =  66

def toString(книга: Книги) -> str:
    match книга:
        case Книги.БЫТИЕ:
            return 'БЫТИЕ'
        case Книги.ИСХОД:
            return 'ИСХОД'
        case Книги.ЛЕВИТ:
            return 'ЛЕВИТ'
        case Книги.ЧИСЛА:
            return 'ЧИСЛА'
        case Книги.ВТОРОЗАКОНИЕ:
            return 'ВТОРОЗАКОНИЕ'
        case Книги.ИИСУСA_НАВИНA:
            return 'ИИСУСA НАВИНA'
        case Книги.КНИГА_СУДЕЙ:
            return 'КНИГА СУДЕЙ'
        case Книги.РУФЬ:
            return 'РУФЬ'
        case Книги.ПЕРВОЯ_ЦАРСТВA:
            return '1 ЦАРСТВA'
        case Книги.ВТОРОЯ_ЦАРСТВA:
            return '2 ЦАРСТВA'
        case Книги.ТРЕТЬЯ_ЦАРСТВA:
            return '3 ЦАРСТВA'
        case Книги.ЧЕТВЕРТОЯ_ЦАРСТВА:
            return '4 ЦАРСТВА'
        case Книги.ПЕРВОЯ_ПАРАЛИПОМЕНОН:
            return '1 ПАРАЛИПОМЕНОН'
        case Книги.ВТОРОЯ_ПАРАЛИПОМЕНОН:
            return '2 ПАРАЛИПОМЕНОН'
        case Книги.ЕЗДРА:
            return 'ЕЗДРА'
        case Книги.НЕЕМИЯ:
            return 'НЕЕМИЯ'
        case Книги.ЕСФИРЬ:
            return 'ЕСФИРЬ'
        case Книги.ИОВ:
            return 'ИОВ'
        case Книги.ПСАЛТИРЬ:
            return 'ПСАЛТИРЬ'
        case Книги.ПРИТЧИ_СОЛОМОНОВЫ:
            return 'ПРИТЧИ СОЛОМОНОВЫ'
        case Книги.ЕККЛЕСИАСТ:
            return 'ЕККЛЕСИАСТ'
        case Книги.ПЕСНЬ_ПЕСНЕЙ:
            return 'ПЕСНЬ ПЕСНЕЙ'
        case Книги.ИСАИЯ:
            return 'ИСАИЯ'
        case Книги.ИЕРЕМИЯ:
            return 'ИЕРЕМИЯ'
        case Книги.ПЛАЧ_ИЕРЕМИИ:
            return 'ПЛАЧ ИЕРЕМИИ'
        case Книги.ИЕЗЕКИИЛЬ:
            return 'ИЕЗЕКИИЛЬ'
        case Книги.ДАНИИЛ:
            return 'ДАНИИЛ'
        case Книги.ОСИЯ:
            return 'ОСИЯ'
        case Книги.ИОИЛЬ:
            return 'ИОИЛЬ'
        case Книги.АМОС:
            return 'АМОС'
        case Книги.АВДИЙ:
            return 'АВДИЙ'
        case Книги.ИОНА:
            return 'ИОНА'
        case Книги.МИХЕЙ:
            return 'МИХЕЙ'
        case Книги.НАУМ:
            return 'НАУМ'
        case Книги.АВВАКУМ:
            return 'АВВАКУМ'
        case Книги.СОФОНИЯ:
            return 'СОФОНИЯ'
        case Книги.АГГЕЙ:
            return 'АГГЕЙ'
        case Книги.ЗАХАРИЯ:
            return 'ЗАХАРИЯ'
        case Книги.МАЛАХИЯ:
            return 'МАЛАХИЯ'
        case Книги.МАТФЕЯ:
            return 'МАТФЕЯ'
        case Книги.МАРКА:
            return 'МАРКА'
        case Книги.ЛУКИ:
            return 'ЛУКИ'
        case Книги.ИОНАННА:
            return 'ИОНАННА'
        case Книги.ДЕЯНИЯ_АПОСТОЛОВ:
            return 'ДЕЯНИЯ АПОСТОЛОВ'
        case Книги.РИМЛЯНАМ:
            return 'РИМЛЯНАМ'
        case Книги.ПЕРВОЕ_КОРИНФЯНАМ:
            return '1 КОРИНФЯНАМ'
        case Книги.ВТОРОЕ_КОРИНФЯНАМ:
            return '2 КОРИНФЯНАМ'
        case Книги.ГАЛАТАМ:
            return 'ГАЛАТАМ'
        case Книги.ЕФЕСЯНАМ:
            return 'ЕФЕСЯНАМ'
        case Книги.ФИЛИППИЙЦАМ:
            return 'ФИЛИППИЙЦАМ'
        case Книги.КОЛОССЯНАМ:
            return 'КОЛОССЯНАМ'
        case Книги.ПЕРВОЕ_ФЕССАЛОНИКИЙЦАМ:
            return '1 ФЕССАЛОНИКИЙЦАМ'
        case Книги.ВТОРОЕ_ФЕССАЛОНИКИЙЦАМ:
            return '2 ФЕССАЛОНИКИЙЦАМ'
        case Книги.ПЕРВОЕ_ТИМОФЕЮ:
            return '1 ТИМОФЕЮ'
        case Книги.ВТОРОЕ_ТИМОФЕЮ:
            return '2 ТИМОФЕЮ'
        case Книги.ТИТУ:
            return 'ТИТУ'
        case Книги.ФИЛИМОНУ:
            return 'ФИЛИМОНУ'
        case Книги.ЕВРЕЯМ:
            return 'ЕВРЕЯМ'
        case Книги.ИАКОВА:
            return 'ИАКОВА'
        case Книги.ПЕРВОЕ_ПЕТРА:
            return '1 ПЕТРА'
        case Книги.ВТОРОЕ_ПЕТРА:
            return '2 ПЕТРА'
        case Книги.ПЕРВОЕ_ИОАННА:
            return '1 ИОАННА'
        case Книги.ВТОРОЕ_ИОАННА:
            return '2 ИОАННА'
        case Книги.ТРЕТИЕ_ИОАННА:
            return '3 ИОАННА'
        case Книги.ИУДА:
            return 'ИУДА'
        case Книги.ОТКРОВЕНИЕ:
            return 'ОТКРОВЕНИЕ'
        case _:
            raise RuntimeError('Unreachable path reached. Check Библия.py:toString(книга: Книги)')

@dataclass
class BibleКнига:
    name: str
    chapters: int
    index: int

bible_книги: dict[Книги, BibleКнига] = {
    Книги.БЫТИЕ:                  BibleКнига(name='БЫТИЕ',               chapters=50,     index=1),
    Книги.ИСХОД:                  BibleКнига(name='ИСХОД',               chapters=40,     index=2),
    Книги.ЛЕВИТ:                  BibleКнига(name='ЛЕВИТ',               chapters=27,     index=3),
    Книги.ЧИСЛА:                  BibleКнига(name='ЧИСЛА',               chapters=36,     index=4),
    Книги.ВТОРОЗАКОНИЕ:           BibleКнига(name='ВТОРОЗАКОНИЕ',        chapters=34,     index=5),
    Книги.ИИСУСA_НАВИНA:          BibleКнига(name='ИИСУСA НАВИНA',       chapters=24,     index=6),
    Книги.КНИГА_СУДЕЙ:            BibleКнига(name='КНИГА СУДЕЙ',         chapters=21,     index=7),
    Книги.РУФЬ:                   BibleКнига(name='РУФЬ',                chapters=4,      index=8),
    Книги.ПЕРВОЯ_ЦАРСТВA:         BibleКнига(name='1 ЦАРСТВA',           chapters=31,     index=9),
    Книги.ВТОРОЯ_ЦАРСТВA:         BibleКнига(name='2 ЦАРСТВA',           chapters=24,     index=10),
    Книги.ТРЕТЬЯ_ЦАРСТВA:         BibleКнига(name='3 ЦАРСТВA',           chapters=22,     index=11),
    Книги.ЧЕТВЕРТОЯ_ЦАРСТВА:      BibleКнига(name='4 ЦАРСТВА',           chapters=25,     index=12),
    Книги.ПЕРВОЯ_ПАРАЛИПОМЕНОН:   BibleКнига(name='1 ПАРАЛИПОМЕНОН',     chapters=29,     index=13),
    Книги.ВТОРОЯ_ПАРАЛИПОМЕНОН:   BibleКнига(name='2 ПАРАЛИПОМЕНОН',     chapters=36,     index=14),
    Книги.ЕЗДРА:                  BibleКнига(name='ЕЗДРА',               chapters=10,     index=15),
    Книги.НЕЕМИЯ:                 BibleКнига(name='НЕЕМИЯ',              chapters=13,     index=16),
    Книги.ЕСФИРЬ:                 BibleКнига(name='ЕСФИРЬ',              chapters=10,     index=17),
    Книги.ИОВ:                    BibleКнига(name='ИОВ',                 chapters=42,     index=18),
    Книги.ПСАЛТИРЬ:               BibleКнига(name='ПСАЛТИРЬ',            chapters=150,    index=19),
    Книги.ПРИТЧИ_СОЛОМОНОВЫ:      BibleКнига(name='ПРИТЧИ СОЛОМОНОВЫ',   chapters=31,     index=20),
    Книги.ЕККЛЕСИАСТ:             BibleКнига(name='ЕККЛЕСИАСТ',          chapters=12,     index=21),
    Книги.ПЕСНЬ_ПЕСНЕЙ:           BibleКнига(name='ПЕСНЬ ПЕСНЕЙ',        chapters=8,      index=22),
    Книги.ИСАИЯ:                  BibleКнига(name='ИСАИЯ',               chapters=66,     index=23),
    Книги.ИЕРЕМИЯ:                BibleКнига(name='ИЕРЕМИЯ',             chapters=52,     index=24),
    Книги.ПЛАЧ_ИЕРЕМИИ:           BibleКнига(name='ПЛАЧ ИЕРЕМИИ',        chapters=5,      index=25),
    Книги.ИЕЗЕКИИЛЬ:              BibleКнига(name='ИЕЗЕКИИЛЬ',           chapters=48,     index=26),
    Книги.ДАНИИЛ:                 BibleКнига(name='ДАНИИЛ',              chapters=12,     index=27),
    Книги.ОСИЯ:                   BibleКнига(name='ОСИЯ',                chapters=14,     index=28),
    Книги.ИОИЛЬ:                  BibleКнига(name='ИОИЛЬ',               chapters=3,      index=29),
    Книги.АМОС:                   BibleКнига(name='АМОС',                chapters=9,      index=30),
    Книги.АВДИЙ:                  BibleКнига(name='АВДИЙ',               chapters=1,      index=31),
    Книги.ИОНА:                   BibleКнига(name='ИОНА',                chapters=4,      index=32),
    Книги.МИХЕЙ:                  BibleКнига(name='МИХЕЙ',               chapters=7,      index=33),
    Книги.НАУМ:                   BibleКнига(name='НАУМ',                chapters=3,      index=34),
    Книги.АВВАКУМ:                BibleКнига(name='АВВАКУМ',             chapters=3,      index=35),
    Книги.СОФОНИЯ:                BibleКнига(name='СОФОНИЯ',             chapters=3,      index=36),
    Книги.АГГЕЙ:                  BibleКнига(name='АГГЕЙ',               chapters=2,      index=37),
    Книги.ЗАХАРИЯ:                BibleКнига(name='ЗАХАРИЯ',             chapters=14,     index=38),
    Книги.МАЛАХИЯ:                BibleКнига(name='МАЛАХИЯ',             chapters=4,      index=39),
    Книги.МАТФЕЯ:                 BibleКнига(name='МАТФЕЯ',              chapters=28,     index=40),
    Книги.МАРКА:                  BibleКнига(name='МАРКА',               chapters=16,     index=41),
    Книги.ЛУКИ:                   BibleКнига(name='ЛУКИ',                chapters=24,     index=42),
    Книги.ИОНАННА:                BibleКнига(name='ИОНАННА',             chapters=21,     index=43),
    Книги.ДЕЯНИЯ_АПОСТОЛОВ:       BibleКнига(name='ДЕЯНИЯ АПОСТОЛОВ',    chapters=28,     index=44),
    Книги.РИМЛЯНАМ:               BibleКнига(name='РИМЛЯНАМ',            chapters=16,     index=45),
    Книги.ПЕРВОЕ_КОРИНФЯНАМ:      BibleКнига(name='1 КОРИНФЯНАМ',        chapters=16,     index=46),
    Книги.ВТОРОЕ_КОРИНФЯНАМ:      BibleКнига(name='2 КОРИНФЯНАМ',        chapters=13,     index=47),
    Книги.ГАЛАТАМ:                BibleКнига(name='ГАЛАТАМ',             chapters=6,      index=48),
    Книги.ЕФЕСЯНАМ:               BibleКнига(name='ЕФЕСЯНАМ',            chapters=6,      index=49),
    Книги.ФИЛИППИЙЦАМ:            BibleКнига(name='ФИЛИППИЙЦАМ',         chapters=4,      index=50),
    Книги.КОЛОССЯНАМ:             BibleКнига(name='КОЛОССЯНАМ',          chapters=4,      index=51),
    Книги.ПЕРВОЕ_ФЕССАЛОНИКИЙЦАМ: BibleКнига(name='1 ФЕССАЛОНИКИЙЦАМ',   chapters=5,      index=52),
    Книги.ВТОРОЕ_ФЕССАЛОНИКИЙЦАМ: BibleКнига(name='2 ФЕССАЛОНИКИЙЦАМ',   chapters=3,      index=53),
    Книги.ПЕРВОЕ_ТИМОФЕЮ:         BibleКнига(name='1 ТИМОФЕЮ',           chapters=6,      index=54),
    Книги.ВТОРОЕ_ТИМОФЕЮ:         BibleКнига(name='2 ТИМОФЕЮ',           chapters=4,      index=55),
    Книги.ТИТУ:                   BibleКнига(name='ТИТУ',                chapters=3,      index=56),
    Книги.ФИЛИМОНУ:               BibleКнига(name='ФИЛИМОНУ',            chapters=1,      index=57),
    Книги.ЕВРЕЯМ:                 BibleКнига(name='ЕВРЕЯМ',              chapters=13,     index=58),
    Книги.ИАКОВА:                 BibleКнига(name='ИАКОВА',              chapters=5,      index=59),
    Книги.ПЕРВОЕ_ПЕТРА:           BibleКнига(name='1 ПЕТРА',             chapters=5,      index=60),
    Книги.ВТОРОЕ_ПЕТРА:           BibleКнига(name='2 ПЕТРА',             chapters=3,      index=61),
    Книги.ПЕРВОЕ_ИОАННА:          BibleКнига(name='1 ИОАННА',            chapters=5,      index=62),
    Книги.ВТОРОЕ_ИОАННА:          BibleКнига(name='2 ИОАННА',            chapters=1,      index=63),
    Книги.ТРЕТИЕ_ИОАННА:          BibleКнига(name='3 ИОАННА',            chapters=1,      index=64),
    Книги.ИУДА:                   BibleКнига(name='ИУДА',                chapters=1,      index=65),
    Книги.ОТКРОВЕНИЕ:             BibleКнига(name='ОТКРОВЕНИЕ',          chapters=22,     index=66)
}