from werkzeug.security import generate_password_hash

from blog.app import db, create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )


@app.cli.command("init-db", help="create all db")
def init_db():
    db.create_all()


@app.cli.command("create-users", help="create users")
def create_users():
    from blog.models import User
    db.session.add(
        User(email="name@email.com", password=generate_password_hash("test"))
    )
    db.session.commit()


COMMANDS = [init_db, create_users]