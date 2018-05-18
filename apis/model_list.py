import graphene
from graphql_models import *
import adapters.aurora as a


class ModelsAPI(graphene.ObjectType):

    app_key = [
        {
            'invocation_id': 'peua9209vvyb72',
            'client_secret': 'oyJniEVX2JIPLqtNB1MqhCBOXqOsgZpU'
        },
        {
            'invocation_id': 'bf544daqnr1x9a',
            'client_secret': 'VuhB7K01c7z8jSnSIVnjoHYrXrnAUcoM'
        },
        {
            'invocation_id': 'dcnis13jsfztu7',
            'client_secret': 'GUh79YLuroyES9uQmsDeHCVpuoQx2EIj'
        },
        {
            'invocation_id': 'wajg958fbxttg5',
            'client_secret': 'Xe8RMOeDXUq5jKVGOOJX2kpeduA2c51p'
        },
        {
            'invocation_id': '6cacozrcvjt89g',
            'client_secret': '0I1JeLBLKSUGhRfZjjTIEbFd659Lpgn9'
        },
        {
            'invocation_id': 'l7tczoj4b0mezd',
            'client_secret': 'nK6whquZomzHh5u0ppdDVOIbOo9nKOiz'
        },
        {
            'invocation_id': 'rtzwkpnpx3uayo',
            'client_secret': 'Zrt0UzRikSyssEH0zxqkiojrqq6sVbET'
        },
        {
            'invocation_id': '0pwyszuxbc3h1j',
            'client_secret': 'NDpiEA32KaIwyapjKob5xFBRB8JisroM'
        },
        {
            'invocation_id': 'f62014elhm9f9q',
            'client_secret': 'W28U8UwRzeDMTzWKEISE0OZdYuGVNbuK'
        }
    ]

    models = graphene.List(Model,
                           series=graphene.String(default_value=''),
                           maker=graphene.String(default_value=''),
                           bodyType=graphene.String(default_value=''),
                           price=graphene.Float(default_value=0),
                           priceFrom=graphene.Float(default_value=0),
                           priceTo=graphene.Float(default_value=0),
                           year=graphene.Int(default_value=0),
                           transmissionDriveTrain=graphene.String(default_value=''),
                           transmissionType=graphene.String(default_value=''),
                           seats=graphene.Int(default_value=0),
                           doors=graphene.Int(default_value=0),
                           )
    def resolve_models(self, info,
                                       series,
                                       maker,
                                       bodyType,
                                       price,
                                       priceFrom,
                                       priceTo,
                                       year,
                                       transmissionDriveTrain,
                                       transmissionType,
                                       seats,
                                       doors
                                       ):

        session = info.context.session

        fields = [
            'fullname', 'group_model', 'maker',
            'body_type',
            'transmission_type', 'transmission_driveline_layout',
            'seats', 'doors',
            'avatar',
            'horsepower', 'engine_displacement'
        ]

        conditions = []

        group_by = [a.CarModel.fullname]
        order_by = [a.CarModel.horsepower]

        if series:
            t = session.query(a.CarModel.id).filter(
                a.CarModel.group_model == series
            ).order_by(
                a.CarModel.year.desc(),
                a.CarModel.horsepower.desc(),
                a.CarModel.engine_displacement.desc(),
                a.CarModel.body_type.desc()
            ).subquery()

            conditions.append(
                a.CarModel.id == a.aliased(a.CarModel, t).id
            )
            group_by = [a.CarModel.fullname]
            order_by = [a.CarModel.horsepower, a.CarModel.body_type]
        elif maker:
            t = session.query(a.CarModel.id).filter(
                a.CarModel.maker == maker
            ).order_by(
                a.CarModel.year.desc(),
                a.CarModel.horsepower.desc(),
                a.CarModel.engine_displacement.desc(),
                a.CarModel.body_type.desc()
            ).subquery()

            conditions.append(
                a.CarModel.id == a.aliased(a.CarModel, t).id
            )
            group_by = [a.CarModel.group_model]
            order_by = [a.CarModel.body_type, a.CarModel.horsepower]

        if bodyType:
            t = session.query(a.CarModel.id).filter(
                a.CarModel.body_type == bodyType
            ).order_by(
                a.CarModel.price
            ).subquery()

            conditions.append(
                a.CarModel.id == a.aliased(a.CarModel, t).id
            )
            order_by = [a.CarModel.horsepower]

        if year:
            conditions.append(
                a.CarModel.year == year
            )

        if transmissionDriveTrain:
            drivetrains ={
                'AWD': 'All-wheel drive',
                '4MATIC': '4Matic',
                '4WD': 'Four-wheel drive',
                'RWD': 'Rear-wheel drive',
                '2WD': 'Two-wheel drive',
                'FWD': 'Front-wheel drive',
            }

            conditions.append(
                a.CarModel.transmission_driveline_layout ==
                drivetrains.get(transmissionDriveTrain.upper(), transmissionDriveTrain)
            )

        if transmissionType:
            conditions.append(
                a.CarModel.transmission_type == transmissionType
            )

        if price:
            conditions.extend([
                a.CarModel.instock == 'available',
                a.CarModel.price > price - price * 0.1,
                a.CarModel.price < price + price * 0.07
                ]
            )
            order_by = [a.CarModel.price]
        elif priceFrom and priceTo:
            conditions.extend([
                a.CarModel.instock == 'available',
                a.CarModel.price >= priceFrom,
                a.CarModel.price < priceTo
                ]
            )
            order_by = [a.CarModel.price]
        elif priceFrom:
            conditions.extend([
                a.CarModel.instock == 'available',
                a.CarModel.price >= priceFrom
                ]
            )
            order_by = [a.CarModel.price]
        elif priceTo:
            conditions.extend([
                a.CarModel.instock == 'available',
                a.CarModel.price < priceTo
                ]
            )
            order_by = [a.CarModel.price.desc()]

        if seats:
            conditions.append(
                a.CarModel.seats == seats
            )

        if doors:
            conditions.append(
                a.CarModel.doors == doors
            )

        conditions.extend([
            a.CarModel.status == 'active'
        ])

        items = None
        try:
            items = session.query(*[getattr(a.CarModel, v) for v in fields]).filter(
                *conditions
            ).group_by(*group_by) \
                .order_by(*order_by).limit(50)
        except:
            session.rollback()

        if not items: return None

        return [
            Model(
                fullname=item.fullname,
                series=Series(
                    name=item.group_model,
                    madeBy=Maker(
                        name=item.maker
                    )
                ),
                body=Body(
                    type=get_enum_value(BodyType, item.body_type)
                ),
                transmission=Transmission(
                    type=get_enum_value(TransmissionType, item.transmission_type),
                    drivetrain=get_enum_value(TransmissionDriveTrain, item.transmission_driveline_layout),
                ),
                avatar=Source(
                    url=item.avatar.replace('.png', '_480x270.png')
                ),
                numberOfSeats=item.seats,
                numberOfDoors=item.doors,
                engine=Engine(
                    horsepower=item.horsepower,
                    displacement=item.engine_displacement
                )
            ) for item in items]

