from rapid_ct_app import app

app.config.update(
    SECRET_KEY='8e791c70866d596a66fa98e9daca396684514915',
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
)