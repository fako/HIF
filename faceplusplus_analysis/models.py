from peewee import *

db = SqliteDatabase('/home/fako/Datascope/datascope/faceplusplus_analysis/faces.db')


class Face(Model):
    filename = TextField()
    fpp_id = TextField()
    fpp_y = IntegerField()
    fpp_x = IntegerField()
    fpp_w = IntegerField()
    fpp_h = IntegerField()

    class Meta:
        database = db

db.create_tables([Face], True)
