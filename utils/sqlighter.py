"""Набор методов для управления базой данных"""
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

from other.states import ALL_STATES


class DataBase:
    """Управляет строками пользователей в базе данных"""

    def __init__(self, abs_path):
        """Создает таблицу users"""
        self.engine = create_engine('sqlite:///' + abs_path)
        self.mtd = MetaData(self.engine)
        self.table = Table('users', self.mtd,
                           Column('id', Integer, primary_key=True),
                           *(Column(state.name, String) for state in ALL_STATES),
                           )
        self.mtd.create_all()

    def select_user(self, user_id: int):
        table = self.table
        cmd = table.select(table.c.id == user_id)
        result = self.engine.execute(cmd)
        return result.fetchone()

    def insert_user(self, values: dict):
        table = self.table
        cmd = table.insert(values=values)
        self.engine.execute(cmd)

    def update_user(self, user_id: int, values: dict):
        table = self.table
        cmd = table.update(values=values, whereclause=table.c.id == user_id)
        self.engine.execute(cmd)

    def delete_user(self, user_id: int):
        table = self.table
        cmd = table.delete(whereclause=table.c.id == user_id)
        self.engine.execute(cmd)

    def get_next_state(self, user_id, get_previous=False):
        """Определяет следующее или последнее состояние по ближайшему пустому полю"""
        fields = self.select_user(user_id)
        previous = None

        for state, field in zip(ALL_STATES, fields[1:]):
            if field is None or field == '':
                return previous if get_previous else state
            previous = state
        else:
            return ALL_STATES[-1] if get_previous else None
