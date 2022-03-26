import json

def load_posts_list():
    """Функция загружает список словарей постов из json файла"""
    with open('posts.json', 'r', encoding='utf-8') as json_file:
        posts_list = json.load(json_file)
    return posts_list


def add_post(new_pic, new_content):
    """Функция добавляет новый пост в список словарей json"""
    new_dict = dict()
    new_dict['pic'] = new_pic
    new_dict['content'] = new_content

    posts_list = load_posts_list()
    posts_list.append(new_dict)  # добавили в существующий список словарей - постов новый словарь-пост

    with open('posts.json', 'w', encoding='utf-8') as json_file:  # открытие на запись нового json файла
        json_file.write(json.dumps(posts_list))




def posts_search(word, posts_list):
    """функция возвращает список словарей-постов, в описании которых есть word"""
    posts_with_word = []
    for post in posts_list:
        if word.lower() in post['content'].lower():
            posts_with_word.append(post)
    if len(posts_with_word) > 0:
        return posts_with_word
    else:
        return '1'


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # множеество допустимых расширений
def is_filename_allowed(filename):
    """Функция проверки расширений (extension) файла картинки"""
    extension = filename.split(".")[-1]
    if extension in ALLOWED_EXTENSIONS:
        return True
    return False


