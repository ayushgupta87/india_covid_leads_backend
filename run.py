from app import app
from db import db

db.init_app(app)


# for creating all tables during first run
@app.before_first_request
def create_tables():
    db.create_all()