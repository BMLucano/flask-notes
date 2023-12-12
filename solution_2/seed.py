from app import create_app
from models import db, User

create_app(SQLALCHEMY_ECHO=True)

db.drop_all()
db.create_all()

u = User.register("joel", "password", "Joel", "Burton", "joel@joel.com")

db.session.add(u)
db.session.commit()
