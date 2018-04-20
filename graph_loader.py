#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import json
from graph_models import *


def load_makers():
    result = {}
    with open('data/car_makers.json') as f:
        items = json.load(f)

        for item in items:
            result[item.get('brand').lower()] = Maker(
                brand=item.get('brand'),
                name=item.get('name'),
                native_name=item.get('native_name'),
                found=item.get('found'),
                founder=item.get('founder'),
                revenue=item.get('revenue'),
                net_income=item.get('net_income'),
                description=item.get('description'),
                shareholders=[Organization(name=v[0], share='%s%%' % v[1]) for v in item.get('owner')],
                divisions = item.get('divisions'),
                subsidiaries=item.get('subsidiaries'),
                website=item.get('website'),
                logo=item.get('logo'),
                image=Image(
                    url=item.get('image', {}).get('url'),
                    description=item.get('image', {}).get('description')
                ),
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
