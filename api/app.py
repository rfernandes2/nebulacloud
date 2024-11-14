from settings import sql_url, sql_track_mod

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = sql_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = sql_track_mod
