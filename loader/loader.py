from flask import Blueprint, render_template

# создаем экземпляр класса блупринт(эскиза)
loader = Blueprint('loader', __name__, template_folder='templates', static_folder='static')


@loader.route('/', methods=['GET', 'POST'])  # генерим страницу для загрузки картинки и текста
def page_main():
    return render_template('post_form.html')
