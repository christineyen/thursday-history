"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from thursdays.model import meta

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=engine)
    meta.engine = engine


## Non-reflected tables may be defined and mapped at module level
#foo_table = sa.Table("Foo", meta.metadata,
#    sa.Column("id", sa.types.Integer, primary_key=True),
#    sa.Column("bar", sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)


t_venues = sa.Table("venues", meta.metadata,
    sa.Column("id", sa.types.Integer, primary_key=True),
    sa.Column("name", sa.types.String(255), nullable=False),
    sa.Column("address", sa.types.String(255), nullable=False),
    sa.Column("date", sa.types.Date, nullable=False),
    sa.Column("latitude", sa.types.Float),
    sa.Column("longitude", sa.types.Float),
    )

class Venue(object):
    def to_s(self):
        print "name: " + self.name + ", addr: " + self.address + ", date: " + str(self.date)
    def list(self):
        return meta.Session.query(Venue).all()
    def pretty_date(self):
        return self.date.strftime('%B %d, %Y')

orm.mapper(Venue, t_venues)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass
