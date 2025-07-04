from dataclasses import dataclass


@dataclass
class Книга:
    name:str
    chapters: int
    index: int

class Библия:
    БЫТИЕ                  = Книга(name="Бытие",                   chapters=50,   index=1),
    ИСХОД                  = Книга(name="Исход",                   chapters=40,   index=2),
    ЛЕВИТ                  = Книга(name="Левит",                   chapters=27,   index=3),
    ЧИСЛА                  = Книга(name="Числа",                   chapters=36,   index=4),
    ВТОРОЗАКОНИЕ           = Книга(name="Второзаконие",            chapters=34,   index=5),
    ИИСУСA_НАВИНA          = Книга(name="Иисуса Навина",           chapters=24,   index=6),
    КНИГА_СУДЕЙ            = Книга(name="Книга Судей",             chapters=21,   index=7),
    РУФЬ                   = Книга(name="Руфь",                    chapters=4,    index=8),
    ПЕРВОЯ_ЦАРСТВA         = Книга(name="1 Царства",               chapters=31,   index=9),
    ВТОРОЯ_ЦАРСТВA         = Книга(name="2 Царства",               chapters=24,   index=10),
    ТРЕТЬЯ_ЦАРСТВA         = Книга(name="3 Царства",               chapters=22,   index=11),
    ЧЕТВЕРТОЯ_ЦАРСТВА      = Книга(name="4 Царства",               chapters=25,   index=12),
    ПЕРВОЯ_ПАРАЛИПОМЕНОН   = Книга(name="1 Паралипоменон",         chapters=29,   index=13),
    ВТОРОЯ_ПАРАЛИПОМЕНОН   = Книга(name="2 Паралипоменон",         chapters=36,   index=14),
    ЕЗДРА                  = Книга(name="Ездра",                   chapters=10,   index=15),
    НЕЕМИЯ                 = Книга(name="Неемия",                  chapters=13,   index=16),
    ЕСФИРЬ                 = Книга(name="Есфирь",                  chapters=10,   index=17),
    ИОВ                    = Книга(name="Иов",                     chapters=42,   index=18),
    ПСАЛТИРЬ               = Книга(name="Псалтирь",                chapters=150,  index=19),
    ПРИТЧИ_СОЛОМОНОВЫ      = Книга(name="Притчи Соломоновы",       chapters=31,   index=20),
    ЕККЛЕСИАСТ             = Книга(name="Екклесиаст",              chapters=12,   index=21),
    ПЕСНЬ_ПЕСНЕЙ           = Книга(name="Песнь Песней",            chapters=8,    index=22),
    ИСАИЯ                  = Книга(name="Исаия",                   chapters=66,   index=23),
    ИЕРЕМИЯ                = Книга(name="Иеремия",                 chapters=52,   index=24),
    ПЛАЧ_ИЕРЕМИИ           = Книга(name="Плач Иеремии",            chapters=5,    index=25),
    ИЕЗЕКИИЛЬ              = Книга(name="Иезекииль",               chapters=48,   index=26),
    ДАНИИЛ                 = Книга(name="Даниил",                  chapters=12,   index=27),
    ОСИЯ                   = Книга(name="Осия",                    chapters=14,   index=28),
    ИОИЛЬ                  = Книга(name="Иоиль",                   chapters=3,    index=29),
    АМОС                   = Книга(name="Амос",                    chapters=9,    index=30),
    АВДИЙ                  = Книга(name="Авдий",                   chapters=1,    index=31),
    ИОНА                   = Книга(name="Иона",                    chapters=4,    index=32),
    МИХЕЙ                  = Книга(name="Михей",                   chapters=7,    index=33),
    НАУМ                   = Книга(name="Наум",                    chapters=3,    index=34),
    АВВАКУМ                = Книга(name="Аввакум",                 chapters=3,    index=35),
    СОФОНИЯ                = Книга(name="Софония",                 chapters=3,    index=36),
    АГГЕЙ                  = Книга(name="Аггей",                   chapters=2,    index=37),
    ЗАХАРИЯ                = Книга(name="Захария",                 chapters=14,   index=38),
    МАЛАХИЯ                = Книга(name="Малахия",                 chapters=4,    index=39),
    МАТФЕЯ                 = Книга(name="Матфея",                  chapters=28,   index=40),
    МАРКА                  = Книга(name="Марка",                   chapters=16,   index=41),
    ЛУКИ                   = Книга(name="Луки",                    chapters=24,   index=42),
    ИОНАННА                = Книга(name="Иоанна",                  chapters=21,   index=43),
    ДЕЯНИЯ_АПОСТОЛОВ       = Книга(name="Деяния Апостолов",        chapters=28,   index=44),
    РИМЛЯНАМ               = Книга(name="Римлянам",                chapters=16,   index=45),
    ПЕРВОЕ_КОРИНФЯНАМ      = Книга(name="1 Коринфянам",            chapters=16,   index=46),
    ВТОРОЕ_КОРИНФЯНАМ      = Книга(name="2 Коринфянам",            chapters=13,   index=47),
    ГАЛАТАМ                = Книга(name="Галатам",                 chapters=6,    index=48),
    ЕФЕСЯНАМ               = Книга(name="Ефесянам",                chapters=6,    index=49),
    ФИЛИППИЙЦАМ            = Книга(name="Филиппийцам",             chapters=4,    index=50),
    КОЛОССЯНАМ             = Книга(name="Колоссянам",              chapters=4,    index=51),
    ПЕРВОЕ_ФЕССАЛОНИКИЙЦАМ = Книга(name="1 Фессалоникийцам",       chapters=5,    index=52),
    ВТОРОЕ_ФЕССАЛОНИКИЙЦАМ = Книга(name="2 Фессалоникийцам",       chapters=3,    index=53),
    ПЕРВОЕ_ТИМОФЕЮ         = Книга(name="1 Тимофею",               chapters=6,    index=54),
    ВТОРОЕ_ТИМОФЕЮ         = Книга(name="2 Тимофею",               chapters=4,    index=55),
    ТИТУ                   = Книга(name="Титу",                    chapters=3,    index=56),
    ФИЛИМОНУ               = Книга(name="Филимону",                chapters=1,    index=57),
    ЕВРЕЯМ                 = Книга(name="Евреям",                  chapters=13,   index=58),
    ИАКОВА                 = Книга(name="Иакова",                  chapters=5,    index=59),
    ПЕРВОЕ_ПЕТРА           = Книга(name="1 Петра",                 chapters=5,    index=60),
    ВТОРОЕ_ПЕТРА           = Книга(name="2 Петра",                 chapters=3,    index=61),
    ПЕРВОЕ_ИОАННА          = Книга(name="1 Иоанна",                chapters=5,    index=62),
    ВТОРОЕ_ИОАННА          = Книга(name="2 Иоанна",                chapters=1,    index=63),
    ТРЕТИЕ_ИОАННА          = Книга(name="3 Иоанна",                chapters=1,    index=64),
    ИУДА                   = Книга(name="Иуда",                    chapters=1,    index=65),
    ОТКРОВЕНИЕ             = Книга(name="Откровение",              chapters=22,   index=66)
