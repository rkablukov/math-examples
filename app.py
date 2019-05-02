import random
from flask import Flask, render_template, url_for, flash, request, Markup
from forms import QuestionForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '634a3025bfda715e26133b9fcfbe2b93'


def get_new_question():
    # задаём новый вопрос
    random.seed()
    sign = '+' if random.randint(1,2) == 1 else '-'
    fint = random.randint(0, 20)
    sint = random.randint(0, 20 if sign == '+' else fint)
    form = QuestionForm(formdata=None)
    form.question.data = f"{fint} {sign} {sint}"
    form.right_answer.data = eval(form.question.data)
    return form


@app.route('/', methods=['GET', 'POST'])
def home():
    form = QuestionForm()
    if form.validate_on_submit():
        if form.answer.data == int(form.right_answer.data):
            flash(f"Правильно! {form.question.data} = {form.answer.data}", 'success')
        else:
            flash(Markup(f"Ошибка! {form.question.data} = <strike>{form.answer.data}</strike> {form.right_answer.data}"), 'danger')
        form = get_new_question()
    elif request.method == 'GET':
        form = get_new_question()
    else:
        flash('В ответе должно быть введено число!', 'danger')
    
    return render_template('home.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)