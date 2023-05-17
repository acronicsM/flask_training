from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from blog.models.article import db
from ..models import Author, Article, Tag

from ..forms.article import CreateArticleForm

article = Blueprint('article', __name__, static_folder='../static', url_prefix='/articles')

@article.route("/", methods=["GET"])
@login_required
def article_list():
    articles = Article.query.all()
    return render_template(
        "articles/list.html",
        articles=articles
    )


@article.route("/<int:pk>", methods=["GET"])
@login_required
def get_article(pk: int):
    _article = Article.query.filter_by(id=pk).options(joinedload(Article.tags)).one_or_none()
    if _article is None:
        raise NotFound("Article id:{}, not found".format(pk))
    return render_template(
        "articles/details.html",
        article=_article
    )


@article.route("/create", methods=["GET"])
@login_required
def create_article_form():
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    return render_template("articles/create.html", form=form)


@article.route("/create", methods=["POST"])
@login_required
def create_article():
    form = CreateArticleForm(request.form)

    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]

    if form.validate_on_submit():
        _article = Article(title=form.title.data.strip(), text=form.text.data)

        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                _article.tags.append(tag)

        if current_user.author:
            article.author = current_user.author.id
        else:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.commit()
            _article.author_id = current_user.author.id

        _article.author_id = current_user.author.id

        db.session.add(_article)
        db.session.commit()

        return redirect(url_for("article.get_article", pk=_article.id))

    return render_template("articles/create.html", form=form)
