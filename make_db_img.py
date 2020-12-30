from eralchemy import render_er
from flask_sqlalchemy import model

from flask_website import db

render_er(db.Model, "erd_from_sqlalchemy.png")

## Draw from database
render_er("sqlite:///site.db", "erd_from_sqlite.png")