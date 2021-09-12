from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange
import os
from threading import Lock


class MessageForm(FlaskForm):
    way = SelectField(
        'Выберите сторону света, в которою желаете отправится',
        coerce=int,
        choices=[
            (0, 'Север'),
            (1, 'Восток'),
            (2, 'Юг'),
            (3, 'Запад'),
        ],
        render_kw={
            'class': 'form-control'
        },
    )
    number_steps = IntegerField(
        'Как далеко планируется продвинуться?',
        validators=[NumberRange(min=1), DataRequired()],
        default=1,
        render_kw={
            'class': 'form-control'
        },
    )
    submit = SubmitField("В путь")


class LevelForm(FlaskForm):
    level = RadioField(
        'Уровень сложности',
        coerce=int,
        validators=[DataRequired()],
        choices=[
            (3, 'Легкий'),
            (2, 'Середний'),
            (1, 'Сложний'),
        ],
        render_kw={
            'class': 'form-control style_type_none'
        }
    )
    submit = SubmitField("Прийнять испытание")


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "@$4n1o4hy32we4wef"
    

class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class House(metaclass=SingletonMeta):
    def __init__(self, ):
        self.x = 0
        self.y = 1
        self.rooms = [
            ['Спальня', 'Холл', 'Кухня'],
            ['Поджемелье', 'Коридор', 'Оружейная'],
        ]
        self.room = self.rooms[self.y][ self.x]
        self.max_y = len(self.rooms)
        self.max_x = len(self.rooms[0])
        self.message_stop = 'Вы не можете идти сюда'
        self.counter = 99

    def restart(self):
        self.x = 0
        self.y = 1
        self.room = self.rooms[self.y][ self.x]
        return None

    def up(self, step):
        if self.x == 1 and self.y - step == -1:
            self.restart()
            return 'Вы победили'
        if self.y - step < 0:
            return self.message_stop
        self.y -= step
        self.room = self.rooms[self.y][ self.x]
        return ''

    def down(self, step):
        if self.y + step >= self.max_y:
            return self.message_stop
        self.y += step    
        self.room = self.rooms[self.y][ self.x]
        return ''
    
    def left(self, step):
        if self.x - step < 0:
            return self.message_stop
        self.x -= step    
        self.room = self.rooms[self.y][ self.x]
        return ''
    
    def right(self, step):
        if self.x + step >= self.max_x:
            return self.message_stop
        self.x += step
        self.room = self.rooms[self.y][ self.x]
        return ''