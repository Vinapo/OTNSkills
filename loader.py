#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import json
from models import *
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
                founder=item.get('founder'),
                revenue=item.get('revenue'),
                netIncome=item.get('net_income'),
                description=item.get('description'),
                shareholders=[Organization(name=v[0], share='%s%%' % v[1]) for v in item.get('owner')],
                divisions = item.get('divisions'),
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
                             year_over_year=ite.get('year_over_year')
                             )
                       for ite in item.get('sales', [])]
            )

    return result


def load_models(makers):
    result = {}

    result['mazda 3 hatchback'] = Model(
        id=1,
        name=u'Mazda 3 Hatchback',
        trim=u'Mazda 3 Hatchback 1.5',
        series=Series(
            name='Mazda 3',
            maker=makers.get('mazda')
        )
    )

    return result


def load_car_pricing():
    result = {}
    with open('data/car_pricing.json') as f:
        items = json.load(f)

        for item in items:
            item_ = CarPricing(
                trim=item.get('trim'),
                series=item.get('series'),
                price=item.get('price'),
                rollingPrice=item.get('rolling_price'),
                transmission=Transmission(
                    drivetrain=item.get('transmission', {}).get('drivetrain', ''),
                    type=item.get('transmission', {}).get('type', '')
                )
            )

            trim = item_.trim.lower()
            result[trim] = item_

            series = item_.series.lower()

            if series in result:
                result[series].append(trim)
            else:
                result[series] = [trim]

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
        return self.db[domain].get(key)