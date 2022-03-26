from flask import Blueprint, render_template

# создаем экземпляр класса блупринт(эскиза)
main = Blueprint('main', __name__, template_folder='templates', static_folder='static')


@main.route('/', methods=['GET', 'POST'])  # генерим страницу для ввода поискового запроса
def page_main():
    return render_template('index.html')
