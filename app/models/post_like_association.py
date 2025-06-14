from app.database import database
from sqlalchemy import Integer, ForeignKey, Table, Column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


#Junction table between users and posts
post_liker = Table(
    "post_liker",
    database.Base.metadata,
    Column('user_id',Integer, ForeignKey('users.user_id'), primary_key = True),
    Column('post_id',Integer, ForeignKey('posts.post_id'), primary_key = True),
    Column('created_at', TIMESTAMP(timezone= True), server_default=text('now()'), nullable = False)
)
    