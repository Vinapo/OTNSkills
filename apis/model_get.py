import graphene
from graphql_models import *
import adapters.aurora as a


class ModelAPI(graphene.ObjectType):

    app_key = [
        {
            'invocation_id': 'ocx3z17z2qyys7',
            'client_secret': '2SfCm4Iy2LN0LpbyxPLjpcJV7ARPPdr4'
        },
        {
            'invocation_id': 'hrlyvcndjd5c81',
            'client_secret': 'dLnuulpWMnYjF69F4Uul8kk7rmJHdl9M'
        },
        ]

    model = graphene.Field(Model,
                           fullname=graphene.String(default_value=''),
                           series=graphene.String(default_value=''),
                           year=graphene.Int(default_value=0),
                           )
    def resolve_model(self, info, fullname, series, year):

        session = info.context.session

        conditions = []

        if fullname:
            conditions.append(
                a.CarModel.fullname == fullname
            )
        else:
            conditions.append(
                a.CarModel.group_model == series
            )

        if year:
            conditions.append(
                a.CarModel.year == year
            )

        try:
            item = session.query(a.CarModel).filter(
               *conditions
            ).order_by(
                a.CarModel.year.desc()
            ).first() or a.CarModel()

            if not item.fullname: return None

        except:
            session.rollback()

        return Model(
            fullname=item.fullname,
            description=item.description,
            series=Series(
                name=item.group_model,
                madeBy=Maker(
                    name=item.maker
                )
            ),
            body=Body(
                type=get_enum_value(BodyType, item.body_type),
                width=item.body_width,
                height=item.body_height,
                wheelbase=item.body_wheelbase,
                length=item.body_length,
                fuelTank=item.fuel_tank,
                trunkCapacity=item.cargo_capacity
            ),
            transmission=Transmission(
                type=get_enum_value(TransmissionType, item.transmission_type),
                drivetrain=get_enum_value(TransmissionDriveTrain, item.transmission_driveline_layout),
            ),
            avatar=Source(
                url=item.avatar.replace('.png', '_480x270.png')
            ),
            cover=Source(
                url=(item.hero_2 or item.hero or '').replace('.jpg', '_800x600.jpg')
            ),
            numberOfSeats=item.seats,
            numberOfDoors=item.doors,
            engine=Engine(
                horsepower=item.horsepower,
                displacement=item.engine_displacement
            )
        )


if __name__ == '__main__':

    from graphql_models import *

    scheme = graphene.Schema(query=ModelAPI)

    query = '''
        query($CAR1_Fullname:String!){
        model(fullname:$CAR1_Fullname){
            fullname
        description
        series {
            name
            madeBy {
                name
            }
        }
        avatar {
            url
        }
        cover {
            url
            description
        }
        numberOfSeats
        body {
            type
        }
        transmission {
            drivetrain
            type
        }
        engine {
            horsepower
            displacement
        }
        }
    }
    '''
    variables = {
        'CAR1_Fullname': 'Mazda CX-5 2.5L AT AWD'
    }

    # print(query, variables)

    class QueryAPIContext(object):
        def __init__(self):
            self.session = a.scoped_session(a.create_session(
                host='mysql+pymysql://root:@localhost:3306/chappie-apis?charset=utf8')
            )


    result = scheme.execute(query,
                            variable_values=variables,
                            context_value=QueryAPIContext()
                            )

    print(result.data)

