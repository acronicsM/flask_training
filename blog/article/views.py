from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

article = Blueprint('article', __name__, static_folder='../static', url_prefix='/articles')

ARTICLES = {
    1: 'Статья №1',
    2: 'Статья №2',
    3: 'Статья №3',
    4: 'Статья №4',
    5: 'Статья №5',
    6: 'Статья №6',
}


@article.route('/article')
def article_list():
    return render_template(
        'article/list.html',
        articles=ARTICLES,
    )


@article.route('/<int:pk>')
def get_article(pk: int):
    try:
        article_name = ARTICLES[pk]
    except KeyError:
        raise NotFound(f'Article id {pk} not found')

    return render_template(
        'article/detail.html',
        article_name=article_name,
    )
