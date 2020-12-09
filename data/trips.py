import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from . import db_session


class Trip(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'trips'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    traveler_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    traveler = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    city_from = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city_where = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hostel = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hostel_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hostel_coordx = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    hostel_coordy = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    flight_company1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    flight_price1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    flight_time1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    flight_company2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    flight_price2 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    flight_time2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    departure_time_city = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    departure_time_home = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    duration = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relation('User')
