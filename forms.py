from flask_wtf import FlaskForm
from wtforms import IntegerField, HiddenField, SubmitField


class QuestionForm(FlaskForm):
    question = HiddenField('Вопрос')
    right_answer = HiddenField('Правильный ответ')
    answer = IntegerField('Ответ')
    n_right_answers = HiddenField('Количество правильных ответов')
    n_wrong_answers = HiddenField('Количество неправильных ответов')
    submit = SubmitField('Проверить')
