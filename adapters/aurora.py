from sqlalchemy import create_engine, event
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.orm import sessionmaker, scoped_session, aliased, deferred, undefer
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, BigInteger, String, Float, JSON, Enum, \
    DateTime, Text, SmallInteger, ForeignKey, desc, asc, CHAR
from sqlalchemy.dialects import mysql

from sqlalchemy import and_, or_, any_, tuple_, func, case
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.pool import NullPool
from sqlalchemy.sql.elements import BooleanClauseList

import re
from sqlalchemy.sql import compiler



def compile_query(query):
    dialect = query.session.bind.dialect
    statement = query.statement
    comp = compiler.SQLCompiler(dialect, statement)
    comp.compile()
    enc = dialect.encoding
    params = {}
    for k, v in comp.params.items():
        if isinstance(v, unicode):
            v = v.encode(enc)
        params[k] = v if not isinstance(v, int) and v.isdigit() else '"%s"' % v
    return (comp.string.encode(enc) % params).decode(enc)


def checkout_listener(connection, con_record, con_proxy):
    try:
        try:
            connection.ping(False)
        except TypeError:
            connection.ping()
    except connection.OperationalError as exc:
        if exc.args[0] in (2006, 2013, 2014, 2045, 2055):
            raise DisconnectionError()
        else:
            raise


def get_class_by_tablename(tablename):
  """Return class reference mapped to table.

  :param tablename: String with name of table.
  :return: Class reference or None.
  """
  for c in Base._decl_class_registry.values():
    if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
      return c


def create_database(host=None):
    engine = create_engine(
        host,
        encoding='utf-8',
        pool_size=100,
        pool_recycle=3600,
        pool_timeout=5,
        echo=False)
    event.listen(engine, 'checkout', checkout_listener)

    Base.metadata.create_all(engine)


def create_session(host=None):
    if not host: return None
    engine = create_engine(
        host,
        encoding='utf-8',
        pool_size=100,
        pool_recycle=3600,
        pool_timeout=5,
        echo=False)
    event.listen(engine, 'checkout', checkout_listener)

    return sessionmaker(bind=engine)


def close_session(host=None):
    db = create_engine(host, poolclass=NullPool)
    db.dispose()


Base = declarative_base()


class BaseMix(object):

    @declared_attr
    def __tablename__(cls):
        return re.sub( '(?<!^)(?=[A-Z])', '_', cls.__name__).lower() # CarModel -> car_model

    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__= {'always_refresh': True}

    id = Column(Integer, primary_key=True, autoincrement=True)

    def to_dict(self, ignores=[]):
        d = (lambda r: {c.name: getattr(r, c.name) for c in r.__table__.columns})(self)
        items = dict()
        for k in d:
            if k not in ignores: items[k] = d[k]
        return items


class Sales(Base, BaseMix):
    name = Column(String(200), index=True) # maker name, car series, car model
    units = Column(BigInteger)
    revenue = Column(BigInteger)
    rank = Column(Integer)
    year_over_year = Column(Float) # percent
    date = Column(DateTime)


class Maker(Base, BaseMix):
    brand = Column(String(200), index=True)
    name = Column(String(200))
    native_name = Column(String(300))
    found = Column(Integer)
    revenue = Column(BigInteger) # USD
    net_income = Column(BigInteger) # USD
    description = Column(String(1000))
    subsidiaries = Column(Integer)
    website = Column(String(300))
    logo = Column(String(300))
    image = Column(String(300))
    image_description = Column(String(300))
    founder = Column(String(300)) # graphene.List(lambda : People)
    shareholders = Column(String(300))  # graphene.List(lambda : Organization)
    divisions = Column(String(300)) # graphene.List(lambda : Organization)
    # graphene.List(lambda : Sales)


class CarModel(Base, BaseMix):

    name = Column(String)
    fullname = Column(String)
    group_model = Column(String)
    subtitle = Column(String)
    description = Column(String)
    body_type = Column(Enum('sedan', 'hatchback', 'coupe', 'convertible', 'crossover', 'suv', 'mpv', 'pickup', 'van', 'minivan', 'truck'))
    body_length = Column(Float)
    body_width = Column(Float)
    body_wheelbase = Column(Float)
    body_height = Column(Float)
    body_weight = Column(Float)
    body_width_mirrors_folded = Column(Float)
    body_drag_coefficient = Column(Float)
    body_ground_clearance = Column(Float)
    body_turning_circle = Column(Float)
    seats = Column(Integer)
    doors = Column(Integer)
    colors = Column(String)
    colors_hex = Column(String)
    horsepower = Column(Integer)
    hp_rpm = Column(Integer)
    engine_torque = Column(Integer)
    torque_rpm = Column(Integer)
    year = Column(Integer)
    msrp = Column(BigInteger)
    price = Column(BigInteger)
    list_price = Column(BigInteger)
    registration_price = Column(BigInteger)
    price_updated_date = Column(DateTime)
    avatar = Column(String)
    hero = Column(String)
    hero_viewbox = Column(String)
    hero_sizebox = Column(String)
    hero_2 = Column(String)
    hero_3 = Column(String)
    zero_to_60mph = Column(Float)
    top_track_speed = Column(Float)
    fuel_tank = Column(Float)

    driving_mode = Column(mysql.SET(['normal', 'eco', 'comfort', 'sport', 'sport+', 'racing', 'individual']))
    transmission_driveline_layout = Column(Enum('All-wheel drive', 'Four-wheel drive', 'Rear-wheel drive', 'Two-wheel drive', 'Front-wheel drive'))
    transmission_type = Column(Enum('mt', 'at', 'cvt', 'dct', 'pdk'))
    transmission_speed_level = Column(Integer)

    # suspension_front = Column(Enum('torsion beam', 'twist beam', 'mcpherson', 'double wishbone' ,'multi-link'))
    # suspension_rear = Column(Enum('torsion beam', 'twist beam', 'mcpherson', 'double wishbone' ,'multi-link'))
    # suspension_front_spring_type = Column(Enum('leaf springs', 'coil springs', 'air springs'))
    # suspension_rear_spring_type = Column(Enum('coil springs', 'air springs'))
    # suspension_advanced = Column(mysql.SET(['active', 'self leveling', 'height adjustable'])) #

    fuel_consumption_city = Column(Float)
    fuel_consumption_highway = Column(Float)
    fuel_consumption_combined = Column(Float)
    luggage_compartment_volume = Column(Float)
    engine_type = Column(Enum('i3', 'i4', 'i5', 'i6', 'v4', 'v6', 'v8', 'v12', 'h4', 'h6', 'boxer', 'electric'))
    engine_cylinder_layout = Column(Integer)
    engine_fuel = Column(Enum('petrol', 'diesel', 'electric', 'hybrid'))
    engine_displacement = Column(Float)
    engine_compression_ratio = Column(Float)
    engine_turbo = Column(Enum('yes', 'no'))
    tyre_sizes = Column(String)
    wheel_sizes = Column(SmallInteger)
    # keyless_start_stop_button = Column(Enum('yes', 'no'))

    safety_airbags = Column(Integer)
    safety_parking_sensor = Column(Enum('360', 'front and rear', 'yes', 'no'))
    safety_rear_camera = Column(Enum('360', 'yes', 'no'))
    safety_abs = Column(Enum('yes', 'no'))
    safety_ebd = Column(Enum('yes', 'no'))
    safety_esp = Column(Enum('yes', 'no'))
    safety_ba = Column(Enum('yes', 'no'))
    safety_hsa = Column(Enum('yes', 'no'))
    safety_epb = Column(Enum('with autohold', 'yes', 'no'))
    safety_hud = Column(Enum('yes', 'no'))
    safety_self_parking = Column(Enum('yes', 'no'))
    safety_cruise_control = Column(Enum('adaptive', 'yes', 'no'))
    safety_front_brakes = Column(Enum('disc', 'drum'))
    safety_rear_brakes = Column(Enum('disc', 'drum'))
    safety_ldw = Column(Enum('yes', 'no'))
    safety_fcw = Column(Enum('yes', 'no'))
    safety_aeb = Column(Enum('yes', 'no'))
    safety_bsw = Column(Enum('yes', 'no'))
    safety_eps = Column(Enum('yes', 'no'))
    safety_isofix = Column(Enum('yes', 'no'))
    safety_tpms =  Column(Enum('yes', 'no')) # Tire Pressure Monitoring Systems

    head_light = Column(Enum('xenon', 'led', 'halogen', 'projector', 'laser'))
    automatic_head_light = Column(Enum('yes', 'no'))
    daytime_running_light = Column(Enum('yes', 'no'))
    fog_lamps = Column(Enum('yes', 'no'))
    roof_rack = Column(Enum('yes', 'no'))
    sun_roof = Column(Enum('panoramic', 'yes', 'no'))
    leather_steering_wheel = Column(Enum('heated', 'yes', 'no'))
    steering_wheel_controls_for_audio = Column(Enum('yes', 'no'))
    seat_height_adjustment = Column(Integer)
    power_seat_height_adjustment = Column(Enum('4 level memory', '3 level memory', '2 level memory', '1 level memory', 'yes', 'no'))
    audio_system = Column(Integer)
    radio = Column(Enum('yes', 'no'))
    multimedia_screen = Column(Enum('airscreen', 'touchscreen', 'lcd', 'no'))
    center_armrest = Column(Enum('yes', 'no'))
    air_conditioner = Column(Enum('automatic', 'manual', 'no'))
    rear_air_conditioner = Column(Enum('automatic', 'manual', 'no'))
    leather_seats = Column(Enum('yes', 'no'))
    folding_rear_seats = Column(Enum('yes', 'no'))
    source_url = Column(String)
    maker = Column(String)
    brand = Column(String)
    made_in = Column(String)
    purposes = Column(mysql.SET(['family', 'service', 'long-road', 'city', 'off-road', 'executive', 'commercial', 'special']))
    styles = Column(mysql.SET(['sport', 'luxury', 'super', 'micro', 'regular']))
    car_class = Column(Enum('a', 'b', 'c', 'd', 'e', 'f', 's', 'j', 'm'))
    rank = Column(Float)
    trending = Column(Integer)
    instock = Column(Enum('available', 'out of stock', 'not available'))
    cargo_capacity = Column(Integer)
    power_rear_door = Column(Enum('with hands-free', 'with height adjustability', 'yes', 'no'))
    power_soft_closing_door = Column(Enum('yes', 'no'))
    # door_curtains = Column(Enum('yes', 'no', 'power'))

    media = Column(String)
    released_date = Column(DateTime)
    updated_date = Column(DateTime)
    created_date = Column(DateTime)
    top_features_in_class = Column(String(250))

    car_connect = Column(Enum('apple airplay and android auto', 'apple airplay', 'android auto', 'internal', 'no'))
    rear_seats_adjustment = Column(Enum('yes', 'no'))

    state = Column(Enum('initial', 'submit for review', 'in review', 'approved', 'rejected', 'request for stop'))
    status = Column(Enum('draft', 'archive', 'active', 'stopped'))
    state_changed_date = Column(DateTime)
    creator = Column(String)
    reviewer = Column(String)
    origin_car_model_id = Column(Integer)

    def __repr__(self):
        return u'%d %s' % (self.id, self.fullname)

if __name__ == '__main__':
    # host = 'mysql+pymysql://root:@localhost:3306/hello1?charset=utf8'
    host = 'mysql+pymysql://root:@localhost:3306/chappie-apis?charset=utf8'
    # host = 'mysql+pymysql://root:?5fTGUCx+yZt&]y9@chappie-dev-2-cluster.cluster-cy1d9y8kv8ra.us-east-1.rds.amazonaws.com:3306/chappie-apis?charset=utf8'
    create_database(host)
