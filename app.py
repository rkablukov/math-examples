import os
import random
from datetime import datetime
from flask import Flask, render_template, url_for, flash, request, Markup, make_response
from forms import QuestionForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '634a3025bfda715e26133b9fcfbe2b93'
app.config['ENABLE_MULTIPLICATION'] = str(
    os.environ.get('ENABLE_MULTIPLICATION')).lower() == 'true'


def get_new_question():
    # задаём новый вопрос
    random.seed()
    nsign = random.randint(1, 2 + app.config['ENABLE_MULTIPLICATION'])
    sign = '+' if nsign == 1 else '-' if nsign == 2 else '*'
    if sign == '*':
        fint = random.randint(1, 9)
        sint = random.randint(1, 9)
    else:
        fint = random.randint(0, 99)
        sint = random.randint(0, 100 - fint if sign == '+' else fint)
    form = QuestionForm(formdata=None)
    form.question.data = f"{fint} {sign} {sint}"
    form.right_answer.data = eval(form.question.data)
    return form


@app.route('/', methods=['GET', 'POST'])
def home():
    n_right_answers = int(request.cookies.get('n_right_answers', 0))
    n_wrong_answers = int(request.cookies.get('n_wrong_answers', 0))
    last_answer_date = request.cookies.get('last_answer_date')
    n_right_answers_best_result = int(
        request.cookies.get('n_right_answers_best_result', 30))
    now = datetime.now().strftime("%Y-%m-%d")
    if now != last_answer_date:
        if n_right_answers > n_right_answers_best_result:
            n_right_answers_best_result = n_right_answers
        n_right_answers = 0
        n_wrong_answers = 0
    last_answer_date = now

    form = QuestionForm()
    if form.validate_on_submit():
        if form.answer.data == int(form.right_answer.data):
            flash(
                f"Правильно! {form.question.data} = {form.answer.data}", 'success')
            n_right_answers += 1
        else:
            flash(Markup(
                f"Ошибка! {form.question.data} = <strike>{form.answer.data}</strike> {form.right_answer.data}"), 'danger')
            n_wrong_answers += 1
        form = get_new_question()
    elif request.method == 'GET':
        form = get_new_question()
    else:
        flash('В ответе должно быть введено число!', 'danger')

    image_file = None
    if n_right_answers >= n_right_answers_best_result:
        image_file = url_for(
            'static', filename='good_job_pics/' + str(datetime.now().weekday()) + '.jpg')

    response = make_response(render_template('home.html', form=form,
                                             n_right_answers=n_right_answers,
                                             n_wrong_answers=n_wrong_answers,
                                             n_right_answers_best_result=n_right_answers_best_result,
                                             image_file=image_file))
    response.set_cookie('n_right_answers', str(n_right_answers))
    response.set_cookie('n_wrong_answers', str(n_wrong_answers))
    response.set_cookie('last_answer_date', last_answer_date)
    response.set_cookie('n_right_answers_best_result', str(n_right_answers_best_result))
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
