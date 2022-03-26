from flask import Flask, request, render_template, send_from_directory
from loader.loader import loader  # импортируем переменную loader
from main.main import main  # импортируем переменную main
from functions import load_posts_list, posts_search, add_post, is_filename_allowed, ALLOWED_EXTENSIONS
from json import JSONDecodeError  #только чтобы видеть эту ошибку при перехвате
import logging


POST_PATH = "posts.json"
UPLOAD_FOLDER = "uploads/images"
logging.basicConfig(filename="basic.log")  #создаем файл для хранения записей логов (вся инфа теперь будет идти туда, а не в RUN консоль)


app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


app.register_blueprint(main)  # регистрация блупринт (цепляем модуль main в главное текущее приложение на адрес /)
app.register_blueprint(loader, url_prefix='/loader')  # регистрация блупринт (цепляем бодуль loader в главное текущее на адрес /loader


@app.route("/search", methods=["GET"])  # возвращает страничку с постами, где есть нужное слово
def page_post_list():
    search = request.args.get('s') # получение аргумента 's'
    if search:
        logging.info(f'Получено слово на поиск: {search}') # логируем конкретику
        try: # попытка подгрузить файл постов json и ловля ошибок
            posts_list = load_posts_list()  # подгружаем список словарей - постов (всех)
        except FileNotFoundError:
            logging.error('Не найден файл: posts.json')
            return 'Файл json не найден. Имя должно быть posts.json<br><br><a href="/" class="link">Назад</a>'
        except JSONDecodeError:
            logging.error('posts.json не хочет превращаться в список')
            return 'posts.json не хочет превращаться в список<br><br><a href="/" class="link">Назад</a>'

        posts_with_word = posts_search(search, posts_list)
        return render_template('post_list.html',
                               search=search,
                               posts_list=posts_with_word)
    else:
        logging.error('вы ввели пустое поле на поиск')
        return 'вы ввели пустое поле, вернитесь назад и повторите поиск<br><br><a href="/" class="link">Назад</a>'


@app.route("/uploads", methods=["GET", 'POST'])
def page_upload():
    picture = request.files.get('picture')  # получаем объект класса - картинка ================
    filename = picture.filename  # из поля имени берем имя картинки
    text = request.form.get('content')  # получаем объект класса - текст ======================

    if not picture or not text:  # проверка, содержится ли вообще в request поле картинки и поле текста
        logging.error('Файл или комментарий не загружены')
        return 'Файл или комментарий не загружены<br><br>Вернитесь назад и повторите попытку<br><br><a href="/loader" class="link">Назад</a>'

    if not is_filename_allowed(filename):  #проверка допустимости расширения файла картинки
        logging.error(f'Файл должен иметь расширение {ALLOWED_EXTENSIONS}')
        return f'Файл должен иметь расширение {ALLOWED_EXTENSIONS}, повторите загрузку<br><br><a href="/loader" class="link">Назад</a>'

    # так как return всегда один и если условие выше не выполнится, то код ниже исполнится
    picture.save(f'./uploads/images/{filename}')  # сохраняем картинку в нужной папке с родным именем
    new_pic = f'/uploads/images/' + filename
    new_content = text

    add_post(new_pic, new_content)  # записываем новый пост в файл json. имя файла сразу записываем с путем для возможности дальнейшего извлечения
    return render_template('post_uploaded.html',
                           filename="/uploads/images/" + filename,
                           text=text)


@app.route("/uploads/images/<path:path>")  # это представление поднимает по указанному адресу (в HTML) доступ на ВСЕ содержимое
def static_dir(path):
    return send_from_directory("uploads/images", path)



if __name__ == '__main__':
    app.run(debug=True)
