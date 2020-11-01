"""Набор состояний бота"""


class State:
    """Состояние бота: название и вопрос и ответы
    ! ответы должны быть уже итерируемыми объектами, либо функцией
    ! каждый ответ - кортеж: (текст, данные)"""
    instances = []

    def __init__(self, name: str, question: str):
        self.name = name
        self.question = question
        self.answers = None
        State.instances.append(self)

    def __str__(self):
        return f'State({self.name}, {self.question})'


country = State('country', 'Выберите страну')
city = State('city', 'Выберите курорт')
From = State('from', 'Выберите город вылета')

checkIn = State('checkIn', 'Дата вылета ОТ')
checkTo = State('checkTo', 'Теперь дата вылета ДО')

nights = State('nights', 'Количество ночей ОТ')
nightsTo = State('nightsTo', 'Теперь количество ночей ДО')

adults = State('adults', 'Количество взрослых')
kid1 = State('kid1', 'Если в туре есть дети, укажите возраст ПЕРВОГО ребенка, иначе выберите "нет ребенка"')
kid2 = State('kid2', 'Возраст ВТОРОГО ребенка')
kid3 = State('kid3', 'Возраст ТРЕТЬЕГО ребенка')

food = State('food', 'Категория питания ОТ')
foodTo = State('foodTo', 'Категория питания ДО')

stars = State('stars', 'Категория отеля ОТ')
starsTo = State('starsTo', 'Категория отеля ДО')

beach_line = State('beach_line', 'Выберите линию пляжа')

price = State('price', 'Стоимость тура ОТ')
priceTo = State('priceTo', 'Стоимость тура ДО')

ALL_STATES = State.instances
