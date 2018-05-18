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
            if name and k.lower() == name.lower() or v.__dict__.get('_value_') == name:
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
    AllWheelDrive = 'All-wheel drive'
    FourMatic = '4Matic' # Mercedes
    FourWheelDrive = 'Four-wheel drive'
    RearWheelDrive = 'Rear-wheel drive'
    TwoWheelDrive = 'Two-wheel drive'
    FrontWheelDrive = 'Front-wheel drive'


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


class SuspensionType(graphene.Enum):
    LeafSprings = 'Leaf springs'
    CoilSprings = 'Coil springs'
    AirSprings = 'Air springs'
    TorsionBean = 'Torsion Bean'
    SportTuned = 'Sport-Tuned'
    McPhersonStrut = 'McPherson strut'

    MultiLink = 'Multi-link'
    DoubleWishbone = 'Double Wishbone'


class BrakeType(graphene.Enum):
    disc = 1
    drum = 2


class MediaScreenType(graphene.Enum):
    LCD = 'LCD'
    TouchScreen = 'Touch screen'
    AirTouchScreen = 'Air touch screen'


class SpeakerType(graphene.Enum):
    BOSS = 1
    Burmester = 2
    Pioneer = 3
    BOSE = 4
    Rockford = 5
    Kenwood = 6
    InfinityReference = 7
    Alpine = 8
    JBL = 9
    JVC = 10


class EntertainmentSystem(graphene.Enum):
    Internal = 1
    AppleCarPlay = 2
    AndroidAuto = 3


class CruiseControlType(graphene.Enum):
    Standard = 1
    Adaptive = 2


class CameraType(graphene.Enum):
    Standard = 1
    View360 = 2


class LightType(graphene.Enum):
    Halogen = 1
    Xenon = 2
    LED = 3
    HID = 4
    Projector = 5
    Laser = 6

class DrivingModeType(graphene.Enum):
    Normal = 1
    Eco = 2
    Sport = 3
    Comfort = 4
    SportPlus = 5
    Individual = 6

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
    name = graphene.String()
    id = graphene.Int()
    trim = graphene.String()
    fullname = graphene.String()
    description = graphene.String()
    year = graphene.Int()
    cover = graphene.Field(lambda : Source)
    avatar = graphene.Field(lambda : Source)

    images = graphene.List(lambda : Source) # interior, exterior, engine images

    series = graphene.Field(lambda : Series)
    transmission = graphene.Field(lambda : Transmission)
    engine = graphene.Field(lambda : Engine)
    colors = graphene.List(lambda : Color)
    tires = graphene.Field(lambda : Tire)
    wheels = graphene.Field(lambda : Wheel)
    madeIn = graphene.Field(lambda : Place)
    doors = graphene.List(lambda : Door)
    numberOfDoors = graphene.Int()
    seats = graphene.List(lambda : Seat)
    numberOfSeats = graphene.Int()
    body = graphene.Field(lambda : Body)
    suspensions = graphene.Field(lambda : ChassisAndSuspensions)
    airConditioner = graphene.Field(lambda : AirConditioner)
    entertainment = graphene.Field(lambda : EntertainmentAndComfort)
    lights = graphene.Field(lambda : Light)
    mirrors = graphene.Field(lambda : Mirror)
    fuelTank = graphene.Float()
    trunkCapacity = graphene.Float()
    drivingAssistant = graphene.Field(lambda : DrivingAssistant)
    safety = graphene.Field(lambda : Safety)
    drivingMode = graphene.List(lambda : DrivingModeType)
    fuelConsumption = graphene.Field(lambda : FuelConsumption)
    luggageCompartmentVolume = graphene.Float()
    price = graphene.Float()

class FuelConsumption(graphene.ObjectType):
    city = graphene.Float()
    highway = graphene.Float()
    combined = graphene.Float()


class Body(graphene.ObjectType):
    type = graphene.Field(lambda : BodyType)
    width = graphene.Float()
    height = graphene.Float()
    length = graphene.Float()
    wheelbase = graphene.Float()
    groundClearance = graphene.Float()
    turningCicle = graphene.Float()
    dragCoefficient = graphene.Float()
    unladenWeight = graphene.Float()
    grossWeight = graphene.Float()
    maxLoad = graphene.Float()


class Transmission(graphene.ObjectType):
    driveTrain = graphene.Field(lambda : TransmissionDriveTrain)
    type = graphene.Field(lambda : TransmissionType)
    speedLevel = graphene.Int()


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

    hasStartStopButton = graphene.Boolean()


class ChassisAndSuspensions(graphene.ObjectType):
    front = graphene.List(lambda : SuspensionType)
    rear = graphene.List(lambda : SuspensionType)
    brakes = graphene.Field(lambda : BrakeType)
    hasStability = graphene.Boolean()
    hasSelfLeveling = graphene.Boolean()
    hasHeightAdjustable = graphene.Boolean()


class Tire(graphene.ObjectType):
    '''
    width/aspectRatio/diameter
    name: P185/75R14 -> width:185, aspectRatio: 75%, diameter: 14
    '''
    name = graphene.String()
    width = graphene.Int() # millimeters
    aspectRatio = graphene.Int() # percent
    diameter = graphene.Int() # inches


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
    isSunRoof = graphene.Boolean()
    isPanoramic = graphene.Boolean()
    curtain = graphene.Field(lambda : WindowCurtain)


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


class AirConditioner(graphene.ObjectType):
    isAutomatic = graphene.Boolean()
    numberOfZones = graphene.Int()
    hasRearSeatsAir = graphene.Boolean()
    hasThirdSeatsAir = graphene.Boolean()
    hasAirFlowsThroughSeat = graphene.Boolean()


class EntertainmentAndComfort(graphene.ObjectType):
    screen = graphene.Field(lambda : MediaScreenType)
    screenSize = graphene.Int() # inches
    hasTouchPad = graphene.Boolean()
    hasVoiceCommand = graphene.Boolean()
    hasHandsFreeCall = graphene.Boolean()
    hasCD = graphene.Boolean()
    hasDVD = graphene.Boolean()
    hasRadio = graphene.Boolean()
    hasBluetooth = graphene.Boolean()
    hasSDCardSlot = graphene.Boolean()
    hasUSBSlot = graphene.Boolean()
    hasHDMISlot = graphene.Boolean()
    hasAUX = graphene.Boolean()
    hasWifi = graphene.Boolean()
    hasWirelessCharger = graphene.Boolean()
    speakers = graphene.Field(lambda : SpeakerType)
    numberOfSpeakers = graphene.Int()
    entertainmentSystems = graphene.List(lambda : EntertainmentSystem)

    rearDashboard = graphene.Boolean()
    rearScreen = graphene.Boolean()


class DrivingAssistant(graphene.ObjectType):
    frontCamera = graphene.Field(lambda : CameraType)
    rearCamera = graphene.Field(lambda : CameraType)

    cruiseControl = graphene.Field(lambda : CruiseControlType)
    hasLaneKeepingAssist = graphene.Boolean()
    hasLaneTurnAssist = graphene.Boolean()
    hasTrafficSignRecognition = graphene.Boolean()

    hasParkAssist = graphene.Boolean()
    hasAttentionAssist = graphene.Boolean()
    hasHeadlampAssist = graphene.Boolean()
    hasParkBrakeAutoHold = graphene.Boolean()
    hasBrakeAdaptive = graphene.Boolean()
    hasHUD = graphene.Boolean() # Head Up Display
    hasBSW = graphene.Boolean() # Blink Spot Warning
    hasEPS = graphene.Boolean() # Electric Power steering
    autopilotLevel = graphene.Int()


class Safety(graphene.ObjectType):
    ABS = graphene.Boolean()
    EBD = graphene.Boolean()
    ESP = graphene.Boolean()
    BA = graphene.Boolean() # Brake Assist
    HSA = graphene.Boolean()
    EPB = graphene.Boolean() # Electric Park Brake
    TPMS = graphene.Boolean() # Tire Pressure Monitoring Systems

    hasFrontSensors = graphene.Boolean()
    hasRearSensors = graphene.Boolean()

    numberOfAirBags = graphene.Int()


class Light(graphene.ObjectType):
    headLight = graphene.Field(lambda : LightType)
    hasAutomaticHeadLight = graphene.Boolean()
    hasHeadLightClean = graphene.Boolean()
    fogLight = graphene.Field(lambda : LightType)
    daytimeRuningLight = graphene.Field(lambda : LightType)
    rearLight = graphene.Field(lambda: LightType)
    highBrakeLight = graphene.Field(lambda: LightType)
    turningLight = graphene.Field(lambda: LightType)


class Mirror(graphene.ObjectType):
    hasPower = graphene.Boolean()
    hasTurnSignal = graphene.Boolean()
    hasHeating = graphene.Boolean()


class CarPricing(graphene.ObjectType):
    fullname = graphene.String()
    trim = graphene.String()
    series = graphene.Field(lambda : Series)
    price = graphene.Float()
    rollingPrice = graphene.Float()
    transmission = graphene.Field(lambda : Transmission)


class CarPricingUpdate(graphene.ObjectType):
    fullname = graphene.String()
    year = graphene.Int()
    price = graphene.Int()
    source = graphene.Field(lambda: Source)
    updatedDate = graphene.String()


class CarSimilar(graphene.ObjectType):
    car1_id = graphene.Int()
    car2_id = graphene.Int()
    weight = graphene.Float()


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
