import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from . import db_session


class Trip(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'trips'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    traveler_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"))
    traveler = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city_from = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city_where = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hostel = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hostel_price = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hostel_coordx = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hostel_coordy = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    flight_company1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    flight_price1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    flight_time1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    flight_company2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    flight_price2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    flight_time2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    departure_date_city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    departure_date_home = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    duration = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relation('User')
