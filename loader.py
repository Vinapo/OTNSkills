#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import json
from graphql_models import *
import csv


def load_makers():
    result = {}
    with open('data/car_makers.json') as f:
        items = json.load(f)

        for item in items:
            result[item.get('brand').lower()] = Maker(
                brand=item.get('brand'),
                name=item.get('name'),
                nativeName=item.get('native_name'),
                found=item.get('found'),
                founder=[People(name=v) for v in item.get('founder')],
                revenue=item.get('revenue'),
                netIncome=item.get('net_income'),
                description=item.get('description'),
                shareholders=[Organization(name=v[0], share='%s%%' % v[1]) for v in item.get('owner')],
                divisions=[Organization(name=v) for v in item.get('divisions')],
                subsidiaries=item.get('subsidiaries'),
                website=item.get('website'),
                logo=Source(url=item.get('logo')),
                image=Source(
                    url=item.get('image', {}).get('url'),
                    description=item.get('image', {}).get('description')
                ),
                sales=[Sales(year=ite.get('year'),
                             units=ite.get('units'),
                             rank=ite.get('rank'),
                             yearOverYear=ite.get('year_over_year')
                             )
                       for ite in item.get('sales', [])]
            )

    return result


def load_models(makers):
    result = {}
    with open('data/car_models.json') as f:
        items = json.load(f)

        for item in items:
            model = Model(
                trim=item.get('trim'),
                fullname=item.get('fullname'),
                series=Series(
                    name=item.get('series'),
                    madeBy=Maker(
                        name=item.get('maker')
                    )
                ),
                avatar=Source(
                    url=item.get('avatar')
                ),
                cover=Source(
                    url=item.get('cover').get('url'),
                    description=item.get('cover').get('description'),
                ),
                description=item.get('description'),
                transmission=Transmission(
                    drivetrain=get_enum_value(TransmissionDriveTrain, item.get('transmission', {}).get('drivetrain')),
                    type=get_enum_value(TransmissionType, item.get('transmission', {}).get('type'))
                ),
                engine=Engine(
                    horsepower=item.get('engine', {}).get('horsepower'),
                    displacement=item.get('engine', {}).get('displacement')
                ),
                numberOfSeats=item.get('seats'),
                body=Body(
                    type=get_enum_value(BodyType, item.get('body_type').lower())
                ),
            )

            fullname = item.get('fullname').lower()
            result[fullname] = model

            maker = item.get('maker').lower()
            if maker in result:
                result[maker].append(model)
            else:
                result[maker] = [model]

            series = item.get('series').lower()
            if series in result:
                result[series].append(model)
            else:
                result[series] = [model]
    return result


def load_car_pricing():
    result = {}
    with open('data/car_pricing.json') as f:
        items = json.load(f)

        for item in items:
            item_ = CarPricing(
                fullname=item.get('fullname'),
                trim=item.get('trim'),
                series=item.get('series'),
                price=item.get('price'),
                rollingPrice=item.get('rolling_price'),
                transmission=Transmission(
                    drivetrain=item.get('transmission', {}).get('drivetrain', ''),
                    type=item.get('transmission', {}).get('type', '')
                )
            )

            fullname = item_.fullname.lower()
            result[fullname] = item_

            series = item_.series.lower()

            if series in result:
                result[series].append(fullname)
            else:
                result[series] = [fullname]

    return result


def load_definitions():
    '''
    Load CSV: Title,Content,Content_english,Images,Icon,Source,Source_URL
    :return:
    '''

    result = {}
    with open('data/definition_dictionary.csv') as f:
        reader = csv.DictReader(f)
        for item in reader:
            title = item.get('Title').strip()
            item_ = Definitions(
                name=title.lower(),
                title=title,
                content=item.get('Content'),
                source=Source(
                    url=item.get('Source'),
                    description=item.get('Source_URL')
                )
            )

            result[item_.name] = item_

    return result


class Storage(object):
    db = {
        'makers': {},
        'models': {},
        'pricing': {},
        'definitions': {}
    }

    def get(self, domain, key):
        if not key: return None
        if not self.db.get(domain):
            if domain == 'makers':
                self.db[domain] = load_makers()
            elif domain == 'pricing':
                self.db[domain] = load_car_pricing()
            elif domain == 'definitions':
                self.db[domain] = load_definitions()
            elif domain == 'models':
                makers = self.db.get('makers')
                if not makers:
                    self.db['makers'] = load_makers()
                self.db[domain] = load_models(makers)
        return self.db[domain].get(key.lower())
