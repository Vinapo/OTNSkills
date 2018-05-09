#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import graphene

# Enums


def get_enum_value(cls, name):
    d = cls.__dict__
    for k in d.keys():
        if k[0] != '_' and k:
            v = getattr(cls, k)
            if k == name or v.__dict__.get('_value_') == name:
                return v.value
    return None


class BodyType(graphene.Enum):
    sedan = 1
    hatchback = 2
    suv = 3
    mpv = 4
    pickup = 5
    truck = 6
    coupe = 7
    convertible = 8
    crossover = 9
    van = 10
    minivan = 11


class TransmissionType(graphene.Enum):
    MT = 1
    AT = 2
    CVT = 3
    DCT = 4
    PDK = 5


class TransmissionDriveTrain(graphene.Enum):
    # ENUM('All-wheel drive', 'Four-wheel drive', 'Rear-wheel drive', 'Two-wheel drive', 'Front-wheel drive')
    AllWheelDrive = 'AWD'
    FourMatic = '4Matic' # Mercedes
    FourWheelDrive = '4WD'
    RearWheelDrive = 'RWD'
    TwoWheelDrive = '2WD'
    FrontWheelDrive = 'FWD'


class ObjectPosition(graphene.Enum):
    Front = 1
    FrontLeft = 2
    FrontRight = 3
    Driver = 4
    Rear = 5
    RearLeft = 6
    RearRight = 7
    Third = 8
    Back = 9
    Top = 10 # Sun roof


class MaterialType(graphene.Enum):
    Leather = 1
    Fabric = 2


class FuelType(graphene.Enum):
    petrol = 1
    diesel = 2
    electric = 3
    hybrid = 4


# Class

class Source(graphene.ObjectType):
    url = graphene.String()
    description = graphene.String()
    label = graphene.String()


class Organization(graphene.ObjectType):
    name = graphene.String()
    share = graphene.String()


class People(graphene.ObjectType):
    name = graphene.String()
    share = graphene.String()


class Place(graphene.ObjectType):
    name = graphene.String()
    address = graphene.String()
    timezone = graphene.Int()
    countryCode = graphene.Int()
    countryName = graphene.String()
    coordinate = graphene.Field(lambda : Coordinate)


class Coordinate(graphene.ObjectType):
    longitude = graphene.Float()
    latitude = graphene.Float()


class Sales(graphene.ObjectType):
    units = graphene.Int()
    year = graphene.Int()
    rank = graphene.Int()
    yearOverYear = graphene.Int()


class Color(graphene.ObjectType):
    name = graphene.String()
    hexColor = graphene.String() #00aa00
    sample = graphene.Field(lambda : Source)
    fullSample = graphene.List(lambda : Source)


class Maker(graphene.ObjectType):
    '''
    {
        "brand": "Toyota",
        "name": "Toyota Motor Corporation",
        "native_name": "トヨタ自動車株式会社",
        "found": 1937,
        "founder": [
          "Kiichiro Toyoda"
        ],
        "revenue": "202,86 tỷ USD",
        "net_income": "13,93 tỷ USD",
        "description": "Toyota Motor Corporation (トヨタ自動車株式会社 Toyota Jidosha Kabushiki-gaisha?) là một công ty đa quốc gia có trụ sở tại Nhật Bản, và là nhà sản xuất ô tô lớn nhất thế giới vào năm 2015[3]. Về mặt công nhận quốc tế, hãng Toyota là nhà sản xuất xe hơi duy nhất có mặt trong nhóm top 10 xếp hạng công nhận tên BrandZ.",
        "owner": [
          ["Japan Trustee Services Bank", 9.7],
          ["Tyota Industries", 6.73],
          ["The Master Trust Bank of Japan", 5.32],
          ["Denso", 2.59]
        ],
        "divisions": [
          "Lexus",
          "Scion (defunct)",
          "TRD"
        ],
        "subsidiaries": 545,
        "website": "http://www.toyota-global.com/",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Toyota_carlogo.svg/500px-Toyota_carlogo.svg.png",
        "image": {
          "url": "https://vignette.wikia.nocookie.net/tractors/images/5/58/Toyota_Headquarter_Toyota_City.jpg/revision/latest?cb=20110412155137",
          "description": "Trụ sở chính của Toyota tại thành phố Toyota, Nhật Bản"
        }
      },
      '''

    brand = graphene.String()
    name = graphene.String()
    nativeName = graphene.String()
    found = graphene.Int()
    founder = graphene.List(lambda : People)
    revenue = graphene.String()
    netIncome = graphene.String()
    description = graphene.String()
    shareholders = graphene.List(lambda : Organization)
    divisions = graphene.List(lambda : Organization)
    subsidiaries = graphene.Int()
    website = graphene.Field(lambda : Source)
    logo = graphene.Field(lambda : Source)
    image = graphene.Field(lambda : Source)
    sales = graphene.List(lambda : Sales)


class Series(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    madeBy = graphene.Field(lambda : Maker)


class Model(graphene.ObjectType):

    trim = graphene.String()
    fullname = graphene.String()
    description = graphene.String()
    series = graphene.Field(lambda : Series)
    avatar = graphene.Field(lambda : Source)
    transmission = graphene.Field(lambda : Transmission)
    engine = graphene.Field(lambda : Engine)
    colors = graphene.List(lambda : Color)
    bodyType = graphene.Field(lambda : BodyType)
    cover = graphene.Field(lambda : Source)
    fuelTank = graphene.Float()
    tire = graphene.Field(lambda : Tire)
    wheel = graphene.Field(lambda : Wheel)
    madeIn = graphene.Field(lambda : Place)
    doors = graphene.List(lambda : Door)
    numberOfDoors = graphene.Int()
    seats = graphene.List(lambda : Seat)
    numberOfSeats = graphene.Int()


class Transmission(graphene.ObjectType):
    drivetrain = graphene.Field(lambda : TransmissionDriveTrain)
    type = graphene.Field(lambda : TransmissionType)


class Engine(graphene.ObjectType):
    displacement = graphene.Float() # cm3
    type = graphene.String()
    fuel = graphene.Field(lambda : FuelType)
    hasTurbo = graphene.Boolean()
    zeroTo60mph = graphene.Float()
    topTrackSpeed = graphene.Int()

    horsepower = graphene.Int()
    horsepowerAtRpm = graphene.List(lambda : graphene.Int) # [min, max] r/min

    torque = graphene.Int() # Max. tourque (Nm)
    torqueAtRpm = graphene.List(lambda : graphene.Int) # [min, max] r/min
    numberOfCylinders = graphene.Int()


class ChassisAndSuspension(graphene.ObjectType):
    pass


class Tire(graphene.ObjectType):
    '''
    width/aspectRatio/diameter
    name: P185/75R14 -> width:185, aspectRatio: 75%, diameter: 14
    '''
    name = graphene.String()
    width = graphene.Int() # millimeters
    aspectRatio = graphene.Int() # percent
    diameter = graphene.Int() # inches
    color = graphene.Field(lambda : Color)


class Wheel(graphene.ObjectType):
    name = graphene.String()
    diameter = graphene.Int() # inches
    color = graphene.Field(lambda : Color)


class Door(graphene.ObjectType):
    position = graphene.Field(lambda : ObjectPosition)
    hasSoftClose = graphene.Boolean()
    hasPower = graphene.Boolean()
    hasHandsFree = graphene.Boolean()
    hasHeightAdjustability = graphene.Boolean()
    isPanoramic = graphene.Boolean()
    curtains = graphene.List(lambda : WindowCurtain)


class WindowCurtain(graphene.ObjectType):
    position = graphene.Field(lambda : ObjectPosition)
    hasPower = graphene.Boolean()


class Seat(graphene.ObjectType):
    position = graphene.Field(lambda : ObjectPosition)
    material = graphene.Field(lambda : MaterialType)
    isPremiumMaterial = graphene.Boolean()
    hasPower = graphene.Boolean()
    hasHeating = graphene.Boolean()
    hasMassage= graphene.Boolean()
    adjustable = graphene.Int() # number of way adjustable
    memory = graphene.Int() # memory of way adjustable
    isFolding = graphene.Boolean()
    isIsofix = graphene.Boolean()
    color = graphene.Field(lambda : Color)


class CarPricing(graphene.ObjectType):
    fullname = graphene.String()
    trim = graphene.String()
    series = graphene.Field(lambda : Series)
    price = graphene.Float()
    rollingPrice = graphene.Float()
    transmission = graphene.Field(lambda : Transmission)


class Definitions(graphene.ObjectType):
    '''
    {
    "name": "suv",
    "title": "SUV",
    "content": "Bản chất SUV là Sport Utility Vehicle, xe thể thao đa dụng, với đặc trưng gầm cao, hệ dẫn động 4 bánh toàn thời gian hoặc bán thời gian. Kích thước dòng xe này thường từ cỡ trung đến lớn, với trang bị thiên về khả năng chạy đường dài, off-road nhiều hơn là di chuyển phố. Cũng vì thế, SUV thường có thiết kế vuông vức, đường nét đơn giản, nam tính. "
    "source": {
      "name": "VnExpress",
      "url": "http://vnexpress.net/tin-tuc/oto-xe-may/phan-biet-cac-dong-oto-tai-viet-nam-3263772.html"
    },
    "image": {
      "url": "https://i-vnexpress.vnecdn.net/2015/08/14/Honda-CR-V-3-8746-1422334185-6379-1439542960.jpg",
      "description": "Honda CR-V xếp vào nhóm crossover."
    }
  }
    '''
    name = graphene.String()
    title = graphene.String()
    content = graphene.String()
    source = graphene.Field(lambda : Source)
    image = graphene.Field(lambda: Source)
